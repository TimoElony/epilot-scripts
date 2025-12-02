#!/usr/bin/env python3
"""
Export Epilot Blueprints

Retrieves blueprint manifests from Epilot API and exports them to JSON files for analysis.
Blueprints are packages that contain workflows and other resources.

Usage:
    python scripts/blueprints/export_blueprints.py
    python scripts/blueprints/export_blueprints.py --output data/output/blueprints
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

BLUEPRINT_API_BASE = "https://blueprint-manifest.sls.epilot.io"

async def fetch_all_blueprints(client: EpilotClient) -> List[Dict[str, Any]]:
    """
    Fetch all blueprints from Epilot.
    
    Returns:
        List of blueprint objects
    """
    print("📘 Fetching blueprints...")
    
    try:
        url = f"{BLUEPRINT_API_BASE}/v2/blueprint-manifest/blueprints"
        result = await client.get(url)
        
        # Handle different response formats
        if isinstance(result, list):
            blueprints = result
        else:
            blueprints = result.get('results', result.get('blueprints', result.get('data', [])))
        
        print(f"✅ Found {len(blueprints)} blueprint(s)")
        return blueprints
        
    except Exception as e:
        print(f"❌ Error fetching blueprints: {e}")
        return []

async def fetch_blueprint_details(client: EpilotClient, blueprint_id: str) -> Optional[Dict[str, Any]]:
    """
    Fetch detailed information for a specific blueprint.
    
    Args:
        blueprint_id: The ID of the blueprint to fetch
    
    Returns:
        Blueprint object with full details including resources
    """
    try:
        url = f"{BLUEPRINT_API_BASE}/v2/blueprint-manifest/blueprints/{blueprint_id}"
        blueprint = await client.get(url)
        return blueprint
        
    except Exception as e:
        print(f"❌ Error fetching blueprint {blueprint_id}: {e}")
        return None

async def export_blueprints(client: EpilotClient, output_dir: Path):
    """
    Export all blueprints to JSON files.
    """
    blueprints = await fetch_all_blueprints(client)
    
    if not blueprints:
        print("⚠️  No blueprints found.")
        return
    
    output_dir.mkdir(parents=True, exist_ok=True)
    
    summary = {
        "exported_at": datetime.now().isoformat(),
        "total_blueprints": len(blueprints),
        "blueprints": []
    }
    
    print(f"\n💾 Exporting {len(blueprints)} blueprint(s)...\n")
    
    for i, blueprint in enumerate(blueprints, 1):
        blueprint_id = blueprint.get('id', blueprint.get('_id', f'unknown_{i}'))
        blueprint_name = blueprint.get('name', blueprint.get('title', 'Untitled'))
        
        # Fetch full details including resources
        if not blueprint_id.startswith('unknown'):
            full_blueprint = await fetch_blueprint_details(client, blueprint_id)
            if full_blueprint:
                blueprint = full_blueprint
        
        # Save individual blueprint file
        filename = f"blueprint_{blueprint_id}.json"
        filepath = output_dir / filename
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(blueprint, f, indent=2, ensure_ascii=False)
        
        print(f"   [{i}/{len(blueprints)}] {blueprint_name} → {filename}")
        
        # Add to summary
        resources = blueprint.get('resources', [])
        resource_types = [r.get('type') for r in resources if isinstance(r, dict) and r.get('type')]
        workflow_count = sum(1 for r in resources if isinstance(r, dict) and r.get('type') == 'workflow_definition')
        
        summary["blueprints"].append({
            "id": blueprint_id,
            "name": blueprint_name,
            "filename": filename,
            "created_at": blueprint.get('_created_at', blueprint.get('created_at')),
            "updated_at": blueprint.get('_updated_at', blueprint.get('updated_at')),
            "version": blueprint.get('version'),
            "resource_count": len(resources) if isinstance(resources, list) else 0,
            "workflow_count": workflow_count,
            "resource_types": list(set(resource_types))
        })
    
    # Save summary file
    summary_path = output_dir / "blueprints_summary.json"
    with open(summary_path, 'w', encoding='utf-8') as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ Blueprints exported to {output_dir}")
    print(f"📊 Summary saved to {summary_path}")

async def analyze_structure(output_dir: Path):
    """
    Analyze the structure of exported blueprints.
    """
    print("\n🔍 Analyzing exported blueprints...\n")
    
    blueprint_files = list(output_dir.glob("blueprint_*.json"))
    if blueprint_files:
        print(f"📘 Blueprint Structure ({len(blueprint_files)} files):")
        with open(blueprint_files[0], 'r') as f:
            sample = json.load(f)
        print(f"   Top-level keys: {', '.join(list(sample.keys())[:10])}")
        
        # Check for resources
        if 'resources' in sample:
            resources = sample['resources']
            if isinstance(resources, list) and resources:
                print(f"   Resources count: {len(resources)}")
                resource_types = set([r.get('type') for r in resources if isinstance(r, dict) and r.get('type')])
                print(f"   Resource types: {', '.join(sorted(resource_types))}")
                
                # Count workflows in blueprint
                workflow_count = sum(1 for r in resources if isinstance(r, dict) and r.get('type') == 'workflow_definition')
                print(f"   Workflows packaged: {workflow_count}")

async def main(output_dir: str):
    """
    Main function to export blueprints.
    """
    load_env()
    client = EpilotClient()
    
    print("🔄 Starting blueprint export...\n")
    
    output_path = Path(output_dir)
    
    try:
        await export_blueprints(client, output_path)
        await analyze_structure(output_path)
        
        print(f"\n🎉 Export complete! Files saved to: {output_path}")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Export Epilot blueprints")
    parser.add_argument(
        "--output",
        default="data/output/blueprints",
        help="Output directory for JSON files"
    )
    
    args = parser.parse_args()
    
    # Add timestamp to directory if using default
    if args.output == "data/output/blueprints":
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        args.output = f"data/output/blueprints_{timestamp}"
    
    asyncio.run(main(args.output))
