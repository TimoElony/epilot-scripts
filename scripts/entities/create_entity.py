#!/usr/bin/env python3
"""
Create Epilot Entity

Creates a new entity in Epilot.

Usage:
    python scripts/entities/create_entity.py --schema contact --title "John Doe"
    python scripts/entities/create_entity.py --schema product --title "Premium Plan" --data '{"price": 99.99}'
"""

import sys
import asyncio
import argparse
import json
from pathlib import Path

# Add lib to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from lib.auth import load_env
from lib.api_client import EpilotClient

ENTITY_API_BASE = "https://entity.sls.epilot.io"

async def create_entity(schema: str, title: str, data: dict = None):
    """
    Create a new entity in Epilot.
    
    Args:
        schema: Entity schema (e.g., 'contact', 'product', 'order')
        title: Title of the entity
        data: Additional entity data as dictionary
    """
    load_env()
    client = EpilotClient()
    
    print(f"🔨 Creating {schema} entity: {title}\n")
    
    # Build entity payload
    entity_data = {
        "_schema": schema,
        "_title": title,
        **(data or {})
    }
    
    try:
        # Call the API
        url = f"{ENTITY_API_BASE}/v1/entities"
        result = await client.post(url, data=entity_data)
        
        entity_id = result.get('_id', 'N/A')
        
        print("✅ Entity created successfully!")
        print(f"   ID:     {entity_id}")
        print(f"   Schema: {schema}")
        print(f"   Title:  {title}")
        
        if data:
            print(f"\n📄 Additional data:")
            print(json.dumps(data, indent=2))
        
    except Exception as e:
        print(f"❌ Error creating entity: {e}")
        sys.exit(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create an Epilot entity")
    parser.add_argument("--schema", required=True, help="Entity schema (e.g., contact, product)")
    parser.add_argument("--title", required=True, help="Entity title")
    parser.add_argument("--data", help="Additional entity data as JSON string")
    
    args = parser.parse_args()
    
    # Parse additional data if provided
    additional_data = None
    if args.data:
        try:
            additional_data = json.loads(args.data)
        except json.JSONDecodeError:
            print("❌ Error: --data must be valid JSON")
            sys.exit(1)
    
    asyncio.run(create_entity(args.schema, args.title, additional_data))
