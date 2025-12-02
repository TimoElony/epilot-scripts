#!/usr/bin/env python3
"""
List Epilot Entities

Retrieves and displays entities from the Epilot Entity API.

Usage:
    python scripts/entities/list_entities.py
    python scripts/entities/list_entities.py --schema contact
    python scripts/entities/list_entities.py --limit 10
"""

import sys
import asyncio
import argparse
from pathlib import Path

# Add lib to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from lib.auth import load_env
from lib.api_client import EpilotClient

ENTITY_API_BASE = "https://entity.sls.epilot.io"

async def list_entities(schema: str = None, limit: int = 20):
    """
    List entities from Epilot.
    
    Args:
        schema: Optional schema to filter by (e.g., 'contact', 'product')
        limit: Maximum number of entities to return
    """
    load_env()
    client = EpilotClient()
    
    print("📋 Fetching entities from Epilot...\n")
    
    # Build query parameters
    params = {"limit": limit}
    if schema:
        params["schema"] = schema
        print(f"🔍 Filtering by schema: {schema}")
    
    try:
        # Call the API
        url = f"{ENTITY_API_BASE}/v1/entities"
        result = await client.get(url, params=params)
        
        entities = result.get('results', [])
        total = result.get('total', 0)
        
        print(f"✅ Found {total} entities (showing {len(entities)}):\n")
        print("=" * 80)
        
        for i, entity in enumerate(entities, 1):
            entity_id = entity.get('_id', 'N/A')
            entity_schema = entity.get('_schema', 'N/A')
            title = entity.get('_title', entity.get('title', 'Untitled'))
            
            print(f"\n{i}. {title}")
            print(f"   ID:     {entity_id}")
            print(f"   Schema: {entity_schema}")
        
        print("\n" + "=" * 80)
        
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="List Epilot entities")
    parser.add_argument("--schema", help="Filter by schema (e.g., contact, product)")
    parser.add_argument("--limit", type=int, default=20, help="Maximum number to return")
    
    args = parser.parse_args()
    
    asyncio.run(list_entities(schema=args.schema, limit=args.limit))
