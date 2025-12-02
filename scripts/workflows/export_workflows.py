#!/usr/bin/env python3
"""
Export Epilot Workflows

Retrieves workflow definitions from Epilot API and exports them to JSON files for analysis.

Usage:
    python scripts/workflows/export_workflows.py
    python scripts/workflows/export_workflows.py --output data/output/workflows
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

WORKFLOW_API_BASE = "https://workflows-definition.sls.epilot.io"

async def fetch_all_workflows(client: EpilotClient) -> List[Dict[str, Any]]:
    """
    Fetch all workflow definitions from Epilot.
    
    Returns:
        List of workflow definition objects
    """
    print("📋 Fetching workflow definitions...")
    
    try:
        url = f"{WORKFLOW_API_BASE}/v1/workflows/definitions"
        result = await client.get(url)
        
        # Handle different response formats
        if isinstance(result, list):
            workflows = result
        else:
            workflows = result.get('results', result.get('definitions', result.get('data', [])))
        
        print(f"✅ Found {len(workflows)} workflow(s)")
        return workflows
        
    except Exception as e:
        print(f"❌ Error fetching workflows: {e}")
        return []

async def fetch_workflow_details(client: EpilotClient, workflow_id: str) -> Optional[Dict[str, Any]]:
    """
    Fetch detailed information for a specific workflow.
    
    Args:
        workflow_id: The ID of the workflow to fetch
    
    Returns:
        Workflow object with full details
    """
    try:
        url = f"{WORKFLOW_API_BASE}/v1/workflows/definitions/{workflow_id}"
        workflow = await client.get(url)
        return workflow
        
    except Exception as e:
        print(f"❌ Error fetching workflow {workflow_id}: {e}")
        return None

async def export_workflows(client: EpilotClient, output_dir: Path):
    """
    Export all workflows to JSON files.
    """
    workflows = await fetch_all_workflows(client)
    
    if not workflows:
        print("⚠️  No workflows found.")
        return
    
    output_dir.mkdir(parents=True, exist_ok=True)
    
    summary = {
        "exported_at": datetime.now().isoformat(),
        "total_workflows": len(workflows),
        "workflows": []
    }
    
    print(f"\n💾 Exporting {len(workflows)} workflow(s)...\n")
    
    for i, workflow in enumerate(workflows, 1):
        workflow_id = workflow.get('id', workflow.get('_id', f'unknown_{i}'))
        workflow_name = workflow.get('name', workflow.get('title', 'Untitled'))
        
        # Fetch full details
        if not workflow_id.startswith('unknown'):
            full_workflow = await fetch_workflow_details(client, workflow_id)
            if full_workflow:
                workflow = full_workflow
        
        # Save individual workflow file
        filename = f"workflow_{workflow_id}.json"
        filepath = output_dir / filename
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(workflow, f, indent=2, ensure_ascii=False)
        
        print(f"   [{i}/{len(workflows)}] {workflow_name} → {filename}")
        
        # Add to summary
        summary["workflows"].append({
            "id": workflow_id,
            "name": workflow_name,
            "filename": filename,
            "created_at": workflow.get('_created_at', workflow.get('created_at')),
            "updated_at": workflow.get('_updated_at', workflow.get('updated_at')),
            "status": workflow.get('status'),
            "description": workflow.get('description', '')[:100] if workflow.get('description') else None
        })
    
    # Save summary file
    summary_path = output_dir / "workflows_summary.json"
    with open(summary_path, 'w', encoding='utf-8') as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ Workflows exported to {output_dir}")
    print(f"📊 Summary saved to {summary_path}")

async def analyze_structure(output_dir: Path):
    """
    Analyze the structure of exported workflows.
    """
    print("\n🔍 Analyzing exported workflows...\n")
    
    workflow_files = list(output_dir.glob("workflow_*.json"))
    if workflow_files:
        print(f"📋 Workflow Structure ({len(workflow_files)} files):")
        with open(workflow_files[0], 'r') as f:
            sample = json.load(f)
        print(f"   Top-level keys: {', '.join(list(sample.keys())[:10])}")
        
        # Check for steps/stages
        if 'steps' in sample:
            print(f"   Contains 'steps' field")
        if 'stages' in sample:
            print(f"   Contains 'stages' field")
        if 'flow' in sample:
            print(f"   Contains 'flow' field")
            # Analyze flow structure
            flow = sample.get('flow', [])
            if flow:
                sections = [item for item in flow if item.get('type') == 'SECTION']
                print(f"   Sections: {len(sections)}")
                total_steps = sum(len(section.get('steps', [])) for section in sections)
                print(f"   Total steps: {total_steps}")

async def main(output_dir: str):
    """
    Main function to export workflows.
    """
    load_env()
    client = EpilotClient()
    
    print("🔄 Starting workflow export...\n")
    
    output_path = Path(output_dir)
    
    try:
        await export_workflows(client, output_path)
        await analyze_structure(output_path)
        
        print(f"\n🎉 Export complete! Files saved to: {output_path}")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Export Epilot workflows")
    parser.add_argument(
        "--output",
        default="data/output/workflows",
        help="Output directory for JSON files"
    )
    
    args = parser.parse_args()
    
    # Add timestamp to directory if using default
    if args.output == "data/output/workflows":
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        args.output = f"data/output/workflows_{timestamp}"
    
    asyncio.run(main(args.output))
