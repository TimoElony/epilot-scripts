#!/usr/bin/env python3
"""
Start Ausbau Glasfaser Workflow on Demo Opportunity

Demonstrates how to manually start a workflow via API.

Usage:
    python scripts/demo/start_workflow_on_opportunity.py
    python scripts/demo/start_workflow_on_opportunity.py --opportunity-id abc123
"""

import sys
import asyncio
import argparse
from pathlib import Path
from datetime import datetime

# Add lib to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from lib.auth import load_env
from lib.api_client import EpilotClient

ENTITY_API_BASE = "https://entity.sls.epilot.io"
WORKFLOW_EXECUTION_API = "https://workflows-execution.sls.epilot.io"
WORKFLOW_DEFINITION_ID = "wfQpwhJF6J"  # Ausbau Glasfaser

async def list_opportunities(client: EpilotClient):
    """List available opportunities."""
    url = f"{ENTITY_API_BASE}/v1/entity/opportunity"
    params = {"limit": 20}
    
    result = await client.get(url, params=params)
    opportunities = result.get('results', [])
    
    return opportunities

async def start_workflow_on_opportunity(client: EpilotClient, opportunity_id: str):
    """
    Start Ausbau Glasfaser workflow on a specific opportunity.
    
    Args:
        opportunity_id: ID of the opportunity entity
    
    Returns:
        Workflow execution details
    """
    print(f"🚀 Starting workflow on opportunity: {opportunity_id}")
    print()
    
    # Get opportunity details first
    try:
        opp_url = f"{ENTITY_API_BASE}/v1/entity/opportunity/{opportunity_id}"
        opportunity = await client.get(opp_url)
        
        print(f"📋 Opportunity Details:")
        print(f"   Title: {opportunity.get('_title', 'N/A')}")
        print(f"   Status: {opportunity.get('status', 'N/A')}")
        print(f"   Tags: {', '.join(opportunity.get('_tags', []))}")
        print()
        
    except Exception as e:
        print(f"❌ Error fetching opportunity: {e}")
        return None
    
    # Start workflow execution
    payload = {
        "definitionId": WORKFLOW_DEFINITION_ID,
        "entityId": opportunity_id,
        "entitySchema": "opportunity"
    }
    
    try:
        url = f"{WORKFLOW_EXECUTION_API}/v1/workflows/executions"
        result = await client.post(url, data=payload)
        
        execution_id = result.get('id', 'N/A')
        status = result.get('status', 'N/A')
        
        print("✅ Workflow started successfully!")
        print()
        print(f"🔗 Workflow Execution Details:")
        print(f"   Execution ID: {execution_id}")
        print(f"   Status: {status}")
        print(f"   Workflow: Ausbau Glasfaser (wfQpwhJF6J)")
        print()
        print(f"🌐 View in Portal:")
        print(f"   {opportunity_id.replace('epilot-opportunity-', '')}")
        print(f"   https://portal.epilot.cloud/app/opportunities/{opportunity_id}")
        print()
        print("📝 Next Steps:")
        print("   1. Open opportunity in Epilot portal")
        print("   2. Click 'Workflows' tab to see active workflow")
        print("   3. Work through workflow steps:")
        print("      - Phase 1: Planung und Vorbereitung (4 steps)")
        print("      - Phase 2: Dienstleister Management (4 steps)")
        print("      - Phase 3: Produktverfügbarkeit (4 steps)")
        print("      - Phase 4: Bauausführung (5 steps, 4 mobile)")
        print("      - Phase 5: Abnahme und Inbetriebnahme (5 steps)")
        print("   4. Complete approval steps (marked with 🔒)")
        print("   5. Use mobile app for construction steps (marked with 📱)")
        
        return result
        
    except Exception as e:
        print(f"❌ Error starting workflow: {e}")
        return None

async def interactive_select_opportunity(client: EpilotClient):
    """
    Show opportunities and let user select one.
    
    Returns:
        Selected opportunity ID
    """
    print("📋 Fetching opportunities...")
    opportunities = await list_opportunities(client)
    
    if not opportunities:
        print("❌ No opportunities found")
        return None
    
    print()
    print("=" * 80)
    print("AVAILABLE OPPORTUNITIES")
    print("=" * 80)
    
    for i, opp in enumerate(opportunities, 1):
        title = opp.get('_title', 'Untitled')
        status = opp.get('status', 'N/A')
        opp_id = opp.get('_id', 'N/A')
        tags = ', '.join(opp.get('_tags', []))
        
        print(f"\n{i}. {title}")
        print(f"   ID: {opp_id}")
        print(f"   Status: {status}")
        if tags:
            print(f"   Tags: {tags}")
    
    print()
    print("=" * 80)
    
    while True:
        try:
            choice = input(f"Select opportunity (1-{len(opportunities)}) or 'q' to quit: ").strip()
            
            if choice.lower() == 'q':
                return None
            
            idx = int(choice) - 1
            if 0 <= idx < len(opportunities):
                return opportunities[idx]['_id']
            else:
                print(f"❌ Please enter a number between 1 and {len(opportunities)}")
        except ValueError:
            print("❌ Please enter a valid number or 'q'")
        except KeyboardInterrupt:
            print("\n\n❌ Cancelled")
            return None

async def main(opportunity_id: str = None):
    """Main function."""
    load_env()
    client = EpilotClient()
    
    print("=" * 80)
    print("🏗️  START AUSBAU GLASFASER WORKFLOW")
    print("=" * 80)
    print()
    
    # If no ID provided, let user select
    if not opportunity_id:
        opportunity_id = await interactive_select_opportunity(client)
        
        if not opportunity_id:
            print("\n👋 No opportunity selected. Exiting.")
            return
    
    print()
    print("=" * 80)
    
    # Start workflow
    result = await start_workflow_on_opportunity(client, opportunity_id)
    
    if result:
        print()
        print("=" * 80)
        print("✅ SUCCESS - Workflow is now active!")
        print("=" * 80)
    else:
        print()
        print("=" * 80)
        print("❌ FAILED - Could not start workflow")
        print("=" * 80)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Start Ausbau Glasfaser workflow on an opportunity"
    )
    parser.add_argument(
        '--opportunity-id',
        type=str,
        help='Specific opportunity ID to start workflow on (optional, will prompt if not provided)'
    )
    
    args = parser.parse_args()
    asyncio.run(main(args.opportunity_id))
