#!/usr/bin/env python3
"""
Export Epilot Designs

Retrieves all designs from the Epilot Design Builder API and exports them to JSON files
for analysis and modification.

Usage:
    python scripts/designs/export_designs.py
    python scripts/designs/export_designs.py --output data/output/designs
    python scripts/designs/export_designs.py --design-id abc123  # Export specific design
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

DESIGN_API_BASE = "https://design-builder-api.sls.epilot.io"

async def fetch_all_designs(client: EpilotClient) -> List[Dict[str, Any]]:
    """
    Fetch all designs from Epilot.
    
    Args:
        client: EpilotClient instance
    
    Returns:
        List of design objects
    """
    print("📥 Fetching designs from Epilot...")
    
    try:
        url = f"{DESIGN_API_BASE}/v1/designs"
        result = await client.get(url)
        
        # The API returns an array of designs
        if isinstance(result, list):
            designs = result
        else:
            designs = result.get('designs', result.get('data', []))
        
        print(f"✅ Found {len(designs)} designs")
        return designs
        
    except Exception as e:
        print(f"❌ Error fetching designs: {e}")
        return []

async def fetch_design_details(client: EpilotClient, design_id: str) -> Optional[Dict[str, Any]]:
    """
    Fetch detailed information for a specific design.
    
    Args:
        client: EpilotClient instance
        design_id: The ID of the design to fetch
    
    Returns:
        Design object with full details
    """
    try:
        url = f"{DESIGN_API_BASE}/v1/designs/{design_id}"
        design = await client.get(url)
        return design
        
    except Exception as e:
        print(f"❌ Error fetching design {design_id}: {e}")
        return None

async def export_designs_to_json(output_dir: str, design_id: Optional[str] = None):
    """
    Export all designs or a specific design to JSON files.
    
    Args:
        output_dir: Directory to save JSON files
        design_id: Optional specific design ID to export
    """
    load_env()
    client = EpilotClient()
    
    print("🔄 Starting design export...\n")
    
    try:
        if design_id:
            # Export specific design
            print(f"📋 Fetching design: {design_id}")
            design = await fetch_design_details(client, design_id)
            
            if not design:
                print("⚠️  Design not found.")
                return
            
            designs = [design]
        else:
            # Export all designs
            designs = await fetch_all_designs(client)
        
        if not designs:
            print("⚠️  No designs found.")
            return
        
        # Create output directory
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        # Export summary
        summary = {
            "exported_at": datetime.now().isoformat(),
            "total_designs": len(designs),
            "designs": []
        }
        
        print(f"\n💾 Exporting {len(designs)} design(s)...\n")
        
        for i, design in enumerate(designs, 1):
            design_id = design.get('_id', design.get('id', f'unknown_{i}'))
            design_name = design.get('name', design.get('title', 'Untitled'))
            
            # Fetch full details if we only have summary
            if not design_id.startswith('unknown'):
                full_design = await fetch_design_details(client, design_id)
                if full_design:
                    design = full_design
            
            # Save individual design file
            filename = f"design_{design_id}.json"
            filepath = output_path / filename
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(design, f, indent=2, ensure_ascii=False)
            
            print(f"   [{i}/{len(designs)}] {design_name} → {filename}")
            
            # Add to summary
            summary["designs"].append({
                "id": design_id,
                "name": design_name,
                "filename": filename,
                "created_at": design.get('_created_at', design.get('created_at')),
                "updated_at": design.get('_updated_at', design.get('updated_at')),
                "status": design.get('status'),
                "application": design.get('application'),
            })
        
        # Save summary file
        summary_path = output_path / "designs_summary.json"
        with open(summary_path, 'w', encoding='utf-8') as f:
            json.dump(summary, f, indent=2, ensure_ascii=False)
        
        print(f"\n✅ Successfully exported {len(designs)} design(s) to {output_dir}")
        print(f"📊 Summary saved to {summary_path}")
        
        # Print structure overview
        print("\n📋 Design Structure Overview:")
        if designs:
            first_design = designs[0]
            print(f"   Keys found: {', '.join(list(first_design.keys())[:10])}...")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

async def analyze_design_structure(output_dir: str):
    """
    Analyze the structure of exported designs.
    
    Args:
        output_dir: Directory containing exported design JSON files
    """
    output_path = Path(output_dir)
    
    if not output_path.exists():
        print(f"❌ Directory not found: {output_dir}")
        return
    
    design_files = list(output_path.glob("design_*.json"))
    
    if not design_files:
        print("⚠️  No design files found.")
        return
    
    print(f"\n🔍 Analyzing {len(design_files)} design file(s)...\n")
    
    all_keys = set()
    nested_structures = {}
    
    for design_file in design_files:
        with open(design_file, 'r', encoding='utf-8') as f:
            design = json.load(f)
        
        # Collect all top-level keys
        all_keys.update(design.keys())
        
        # Analyze nested structures
        for key, value in design.items():
            if isinstance(value, dict):
                nested_structures[key] = nested_structures.get(key, set())
                nested_structures[key].update(value.keys())
            elif isinstance(value, list) and value and isinstance(value[0], dict):
                nested_structures[key] = nested_structures.get(key, set())
                nested_structures[key].update(value[0].keys())
    
    print("📊 Top-level fields:")
    for key in sorted(all_keys):
        print(f"   - {key}")
    
    if nested_structures:
        print("\n📦 Nested structures:")
        for key, subkeys in sorted(nested_structures.items()):
            print(f"   - {key}:")
            for subkey in sorted(subkeys):
                print(f"      • {subkey}")
    
    print(f"\n💡 Files are ready for analysis in: {output_dir}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Export Epilot designs to JSON")
    parser.add_argument(
        "--output", 
        default="data/output/designs",
        help="Output directory for JSON files"
    )
    parser.add_argument(
        "--design-id",
        help="Specific design ID to export (optional)"
    )
    parser.add_argument(
        "--analyze",
        action="store_true",
        help="Analyze structure of already exported designs"
    )
    
    args = parser.parse_args()
    
    # Add timestamp to directory if using default
    if args.output == "data/output/designs" and not args.analyze:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        args.output = f"data/output/designs_{timestamp}"
    
    if args.analyze:
        asyncio.run(analyze_design_structure(args.output))
    else:
        asyncio.run(export_designs_to_json(args.output, args.design_id))
