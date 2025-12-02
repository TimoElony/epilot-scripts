#!/usr/bin/env python3
"""
List All Epilot APIs

Fetches and displays all available Epilot API endpoints from the discovery URL.
This is useful to see what APIs are available and their base URLs.

Usage:
    python scripts/utilities/list_all_apis.py
"""

import sys
import asyncio
from pathlib import Path

# Add lib to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from lib.auth import load_env
from lib.api_client import EpilotClient

DISCOVERY_URL = "https://docs.epilot.io/openapi-specs/apis.json"

async def list_apis():
    """Fetch and display all Epilot APIs."""
    print("🔍 Fetching Epilot APIs...\n")
    
    # Note: This endpoint doesn't require authentication
    async with httpx.AsyncClient() as client:
        response = await client.get(DISCOVERY_URL)
        data = response.json()
    
    apis = data.get('apis', [])
    
    print(f"✅ Found {len(apis)} Epilot APIs:\n")
    print("=" * 100)
    
    for i, api in enumerate(apis, 1):
        name = api.get('name', 'Unknown')
        base_url = api.get('baseURL', '')
        
        # Get OpenAPI spec URL
        spec_url = ''
        for prop in api.get('properties', []):
            if prop.get('type') == 'Swagger':
                spec_url = prop.get('url', '')
                break
        
        print(f"\n{i:2}. {name}")
        print(f"    Base URL: {base_url}")
        if spec_url:
            print(f"    OpenAPI:  {spec_url}")
    
    print("\n" + "=" * 100)
    print(f"\n💡 You can use these base URLs in your scripts to interact with Epilot services.")
    print(f"   Example: python scripts/entities/list_entities.py\n")

if __name__ == "__main__":
    import httpx
    asyncio.run(list_apis())
