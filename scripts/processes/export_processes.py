#!/usr/bin/env python3
"""
Export Epilot Workflows and Blueprints

Retrieves workflow definitions and blueprint manifests from Epilot APIs
and exports them to JSON files for analysis.

Usage:
    python scripts/processes/export_processes.py
    python scripts/processes/export_processes.py --workflows-only
    python scripts/processes/export_processes.py --blueprints-only
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
BLUEPRINT_API_BASE = "https://blueprint-manifest.sls.epilot.io"

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

async def export_workflows(client: EpilotClient, output_dir: Path):
    """
    Export all workflows to JSON files.
    """
    workflows = await fetch_all_workflows(client)
    
    if not workflows:
        print("⚠️  No workflows found.")
        return
    
    workflow_dir = output_dir / "workflows"
    workflow_dir.mkdir(parents=True, exist_ok=True)
    
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
        filepath = workflow_dir / filename
        
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
    summary_path = workflow_dir / "workflows_summary.json"
    with open(summary_path, 'w', encoding='utf-8') as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ Workflows exported to {workflow_dir}")
    print(f"📊 Summary saved to {summary_path}")

async def export_blueprints(client: EpilotClient, output_dir: Path):
    """
    Export all blueprints to JSON files.
    """
    blueprints = await fetch_all_blueprints(client)
    
    if not blueprints:
        print("⚠️  No blueprints found.")
        return
    
    blueprint_dir = output_dir / "blueprints"
    blueprint_dir.mkdir(parents=True, exist_ok=True)
    
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
        filepath = blueprint_dir / filename
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(blueprint, f, indent=2, ensure_ascii=False)
        
        print(f"   [{i}/{len(blueprints)}] {blueprint_name} → {filename}")
        
        # Add to summary
        resources = blueprint.get('resources', [])
        summary["blueprints"].append({
            "id": blueprint_id,
            "name": blueprint_name,
            "filename": filename,
            "created_at": blueprint.get('_created_at', blueprint.get('created_at')),
            "updated_at": blueprint.get('_updated_at', blueprint.get('updated_at')),
            "version": blueprint.get('version'),
            "resource_count": len(resources) if isinstance(resources, list) else 0,
            "resource_types": list(set([r.get('type') for r in resources if isinstance(r, dict) and r.get('type')]))
        })
    
    # Save summary file
    summary_path = blueprint_dir / "blueprints_summary.json"
    with open(summary_path, 'w', encoding='utf-8') as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ Blueprints exported to {blueprint_dir}")
    print(f"📊 Summary saved to {summary_path}")

async def analyze_structure(output_dir: Path):
    """
    Analyze the structure of exported workflows and blueprints.
    """
    print("\n🔍 Analyzing exported data...\n")
    
    # Analyze workflows
    workflow_dir = output_dir / "workflows"
    if workflow_dir.exists():
        workflow_files = list(workflow_dir.glob("workflow_*.json"))
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
    
    # Analyze blueprints
    blueprint_dir = output_dir / "blueprints"
    if blueprint_dir.exists():
        blueprint_files = list(blueprint_dir.glob("blueprint_*.json"))
        if blueprint_files:
            print(f"\n📘 Blueprint Structure ({len(blueprint_files)} files):")
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

async def main(workflows_only: bool, blueprints_only: bool, output_dir: str):
    """
    Main function to export workflows and blueprints.
    """
    load_env()
    client = EpilotClient()
    
    print("🔄 Starting process export...\n")
    
    output_path = Path(output_dir)
    
    try:
        if not blueprints_only:
            await export_workflows(client, output_path)
        
        if not workflows_only:
            await export_blueprints(client, output_path)
        
        await analyze_structure(output_path)
        
        print(f"\n🎉 Export complete! Files saved to: {output_path}")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Export Epilot workflows and blueprints")
    parser.add_argument(
        "--output",
        default="data/output/processes",
        help="Output directory for JSON files"
    )
    parser.add_argument(
        "--workflows-only",
        action="store_true",
        help="Export only workflows"
    )
    parser.add_argument(
        "--blueprints-only",
        action="store_true",
        help="Export only blueprints"
    )
    
    args = parser.parse_args()
    
    # Add timestamp to directory if using default
    if args.output == "data/output/processes":
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        args.output = f"data/output/processes_{timestamp}"
    
    asyncio.run(main(args.workflows_only, args.blueprints_only, args.output))
