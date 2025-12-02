#!/usr/bin/env python3
"""
Export Epilot Journeys

Retrieves journey configurations from Epilot API and exports them to JSON files for analysis.
Journeys are customer-facing forms and portals.

Usage:
    python scripts/journeys/export_journeys.py
    python scripts/journeys/export_journeys.py --output data/output/journeys
"""

import sys
import asyncio
import argparse
import json
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any, Optional

# Add lib to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from lib.auth import load_env
from lib.api_client import EpilotClient

JOURNEY_API_BASE = "https://journey-config.sls.epilot.io"

async def fetch_all_journeys(client: EpilotClient) -> List[Dict[str, Any]]:
    """
    Fetch all journey configurations from Epilot.
    
    Returns:
        List of journey objects
    """
    print("🗺️  Fetching journey configurations...")
    
    try:
        # Use v1 search endpoint
        url = f"{JOURNEY_API_BASE}/v1/journey/configuration/search"
        result = await client.post(url, data={"query": "*"})
        
        # Handle different response formats
        if isinstance(result, list):
            journeys = result
        else:
            journeys = result.get('results', result.get('journeys', result.get('data', [])))
        
        print(f"✅ Found {len(journeys)} journey(s)")
        return journeys
        
    except Exception as e:
        print(f"❌ Error fetching journeys: {e}")
        return []

async def fetch_journey_details(client: EpilotClient, journey_id: str) -> Optional[Dict[str, Any]]:
    """
    Fetch detailed information for a specific journey.
    
    Args:
        journey_id: The ID of the journey to fetch
    
    Returns:
        Journey object with full details
    """
    try:
        url = f"{JOURNEY_API_BASE}/v1/journey/configuration/{journey_id}"
        journey = await client.get(url)
        return journey
        
    except Exception as e:
        print(f"❌ Error fetching journey {journey_id}: {e}")
        return None

async def export_journeys(client: EpilotClient, output_dir: Path):
    """
    Export all journeys to JSON files.
    """
    journeys = await fetch_all_journeys(client)
    
    if not journeys:
        print("⚠️  No journeys found.")
        return
    
    output_dir.mkdir(parents=True, exist_ok=True)
    
    summary = {
        "exported_at": datetime.now().isoformat(),
        "total_journeys": len(journeys),
        "journeys": []
    }
    
    print(f"\n💾 Exporting {len(journeys)} journey(s)...\n")
    
    for i, journey in enumerate(journeys, 1):
        # Note: search results have both _id (entity ID) and journey_id (config ID)
        # Use journey_id for fetching the actual journey configuration
        config_id = journey.get('journey_id')  # This is the journey configuration ID
        entity_id = journey.get('id', journey.get('_id', f'unknown_{i}'))  # This is the entity ID
        journey_name = journey.get('name', journey.get('title', journey.get('journey_name', 'Untitled')))
        
        # Fetch full details using the journey_id (configuration ID)
        if config_id:
            full_journey = await fetch_journey_details(client, config_id)
            if full_journey:
                journey = full_journey
        
        # Save individual journey file using entity_id for filename
        filename = f"journey_{entity_id}.json"
        filepath = output_dir / filename
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(journey, f, indent=2, ensure_ascii=False)
        
        print(f"   [{i}/{len(journeys)}] {journey_name} → {filename}")
        
        # Analyze journey structure
        steps = journey.get('steps', [])
        blocks = []
        for step in steps:
            if isinstance(step, dict):
                blocks.extend(step.get('blocks', []))
        
        # Add to summary
        summary["journeys"].append({
            "id": entity_id,
            "name": journey_name,
            "filename": filename,
            "created_at": journey.get('_created_at', journey.get('created_at')),
            "updated_at": journey.get('_updated_at', journey.get('updated_at')),
            "design_id": journey.get('design_id'),
            "step_count": len(steps) if isinstance(steps, list) else 0,
            "block_count": len(blocks),
            "block_types": list(set([b.get('type') for b in blocks if isinstance(b, dict) and b.get('type')])),
            "published": journey.get('published'),
            "logics": len(journey.get('logics', [])) if isinstance(journey.get('logics'), list) else 0
        })
    
    # Save summary file
    summary_path = output_dir / "journeys_summary.json"
    with open(summary_path, 'w', encoding='utf-8') as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ Journeys exported to {output_dir}")
    print(f"📊 Summary saved to {summary_path}")

async def analyze_structure(output_dir: Path):
    """
    Analyze the structure of exported journeys.
    """
    print("\n🔍 Analyzing exported journeys...\n")
    
    journey_files = list(output_dir.glob("journey_*.json"))
    if journey_files:
        print(f"🗺️  Journey Structure ({len(journey_files)} files):")
        with open(journey_files[0], 'r') as f:
            sample = json.load(f)
        print(f"   Top-level keys: {', '.join(list(sample.keys())[:10])}")
        
        # Analyze steps
        if 'steps' in sample:
            steps = sample.get('steps', [])
            print(f"   Contains 'steps' field: {len(steps)} step(s)")
            
            # Analyze blocks
            all_blocks = []
            for step in steps:
                if isinstance(step, dict):
                    all_blocks.extend(step.get('blocks', []))
            
            if all_blocks:
                block_types = set([b.get('type') for b in all_blocks if isinstance(b, dict) and b.get('type')])
                print(f"   Total blocks across steps: {len(all_blocks)}")
                print(f"   Block types: {', '.join(sorted(block_types))}")
        
        # Check for logic
        if 'logics' in sample:
            logics = sample.get('logics', [])
            print(f"   Contains 'logics' field: {len(logics)} logic rule(s)")
        
        # Check for design
        if 'design_id' in sample:
            print(f"   Linked to design: {sample.get('design_id')}")

async def main(output_dir: str):
    """
    Main function to export journeys.
    """
    load_env()
    client = EpilotClient()
    
    print("🔄 Starting journey export...\n")
    
    output_path = Path(output_dir)
    
    try:
        await export_journeys(client, output_path)
        await analyze_structure(output_path)
        
        print(f"\n🎉 Export complete! Files saved to: {output_path}")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Export Epilot journeys")
    parser.add_argument(
        "--output",
        default="data/output/journeys",
        help="Output directory for JSON files"
    )
    
    args = parser.parse_args()
    
    # Add timestamp to directory if using default
    if args.output == "data/output/journeys":
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        args.output = f"data/output/journeys_{timestamp}"
    
    asyncio.run(main(args.output))
