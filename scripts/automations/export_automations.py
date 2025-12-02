#!/usr/bin/env python3
"""
Export Epilot Automation Flows

Retrieves automation flows from Epilot API and exports them to JSON files for analysis.

Usage:
    python scripts/automations/export_automations.py
    python scripts/automations/export_automations.py --output data/output/automations
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

AUTOMATION_API_BASE = "https://automation.sls.epilot.io"

async def fetch_all_automations(client: EpilotClient) -> List[Dict[str, Any]]:
    """
    Fetch all automation flows from Epilot.
    
    Returns:
        List of automation flow objects
    """
    print("🤖 Fetching automation flows...")
    
    try:
        # Use search endpoint to get all flows
        url = f"{AUTOMATION_API_BASE}/v1/automation/flows"
        result = await client.get(url)
        
        # Handle different response formats
        if isinstance(result, list):
            automations = result
        else:
            automations = result.get('results', result.get('flows', result.get('data', [])))
        
        print(f"✅ Found {len(automations)} automation flow(s)")
        return automations
        
    except Exception as e:
        print(f"❌ Error fetching automations: {e}")
        return []

async def fetch_automation_details(client: EpilotClient, flow_id: str) -> Optional[Dict[str, Any]]:
    """
    Fetch detailed information for a specific automation flow.
    
    Args:
        flow_id: The ID of the automation flow to fetch
    
    Returns:
        Automation flow object with full details
    """
    try:
        url = f"{AUTOMATION_API_BASE}/v1/automation/flows/{flow_id}"
        automation = await client.get(url)
        return automation
        
    except Exception as e:
        print(f"❌ Error fetching automation {flow_id}: {e}")
        return None

async def export_automations(client: EpilotClient, output_dir: Path):
    """
    Export all automation flows to JSON files.
    """
    automations = await fetch_all_automations(client)
    
    if not automations:
        print("⚠️  No automation flows found.")
        return
    
    output_dir.mkdir(parents=True, exist_ok=True)
    
    summary = {
        "exported_at": datetime.now().isoformat(),
        "total_automations": len(automations),
        "automations": []
    }
    
    print(f"\n💾 Exporting {len(automations)} automation flow(s)...\n")
    
    for i, automation in enumerate(automations, 1):
        flow_id = automation.get('id', automation.get('_id', f'unknown_{i}'))
        flow_name = automation.get('name', automation.get('title', 'Untitled'))
        
        # Fetch full details if we only have summary
        if not flow_id.startswith('unknown'):
            full_automation = await fetch_automation_details(client, flow_id)
            if full_automation:
                automation = full_automation
        
        # Save individual automation file
        filename = f"automation_{flow_id}.json"
        filepath = output_dir / filename
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(automation, f, indent=2, ensure_ascii=False)
        
        print(f"   [{i}/{len(automations)}] {flow_name} → {filename}")
        
        # Analyze automation structure
        triggers = automation.get('triggers', [])
        actions = automation.get('actions', [])
        
        # Add to summary
        summary["automations"].append({
            "id": flow_id,
            "name": flow_name,
            "filename": filename,
            "created_at": automation.get('_created_at', automation.get('created_at')),
            "updated_at": automation.get('_updated_at', automation.get('updated_at')),
            "enabled": automation.get('enabled'),
            "trigger_count": len(triggers) if isinstance(triggers, list) else 0,
            "action_count": len(actions) if isinstance(actions, list) else 0,
            "trigger_types": list(set([t.get('type') for t in triggers if isinstance(t, dict) and t.get('type')])),
            "action_types": list(set([a.get('type') for a in actions if isinstance(a, dict) and a.get('type')]))
        })
    
    # Save summary file
    summary_path = output_dir / "automations_summary.json"
    with open(summary_path, 'w', encoding='utf-8') as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ Automations exported to {output_dir}")
    print(f"📊 Summary saved to {summary_path}")

async def analyze_structure(output_dir: Path):
    """
    Analyze the structure of exported automation flows.
    """
    print("\n🔍 Analyzing exported automations...\n")
    
    automation_files = list(output_dir.glob("automation_*.json"))
    if automation_files:
        print(f"🤖 Automation Flow Structure ({len(automation_files)} files):")
        with open(automation_files[0], 'r') as f:
            sample = json.load(f)
        print(f"   Top-level keys: {', '.join(list(sample.keys())[:10])}")
        
        # Analyze triggers
        if 'triggers' in sample:
            triggers = sample.get('triggers', [])
            print(f"   Contains 'triggers' field: {len(triggers)} trigger(s)")
            if triggers and isinstance(triggers, list):
                trigger_types = set([t.get('type') for t in triggers if isinstance(t, dict) and t.get('type')])
                print(f"   Trigger types: {', '.join(sorted(trigger_types))}")
        
        # Analyze actions
        if 'actions' in sample:
            actions = sample.get('actions', [])
            print(f"   Contains 'actions' field: {len(actions)} action(s)")
            if actions and isinstance(actions, list):
                action_types = set([a.get('type') for a in actions if isinstance(a, dict) and a.get('type')])
                print(f"   Action types: {', '.join(sorted(action_types))}")
        
        # Check for conditions
        if 'conditions' in sample:
            print(f"   Contains 'conditions' field")

async def main(output_dir: str):
    """
    Main function to export automation flows.
    """
    load_env()
    client = EpilotClient()
    
    print("🔄 Starting automation export...\n")
    
    output_path = Path(output_dir)
    
    try:
        await export_automations(client, output_path)
        await analyze_structure(output_path)
        
        print(f"\n🎉 Export complete! Files saved to: {output_path}")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Export Epilot automation flows")
    parser.add_argument(
        "--output",
        default="data/output/automations",
        help="Output directory for JSON files"
    )
    
    args = parser.parse_args()
    
    # Add timestamp to directory if using default
    if args.output == "data/output/automations":
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        args.output = f"data/output/automations_{timestamp}"
    
    asyncio.run(main(args.output))
