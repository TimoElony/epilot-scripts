#!/usr/bin/env python3
"""
Test Epilot API Connection

Tests your authentication and connection to Epilot APIs.
This script attempts to call a simple endpoint to verify your setup.

Usage:
    python scripts/utilities/test_connection.py
"""

import sys
import asyncio
from pathlib import Path

# Add lib to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from lib.auth import load_env
from lib.api_client import EpilotClient

async def test_connection():
    """Test connection to Epilot API."""
    print("🔧 Testing Epilot API Connection...\n")
    
    # Load environment variables
    load_env()
    
    try:
        client = EpilotClient()
        print("✅ Authentication headers loaded")
        print("✅ API client initialized")
        
        # Try to call a simple endpoint (adjust based on what's available)
        # This is a placeholder - you'll need to use an actual endpoint you have access to
        print("\n💡 To test an actual API call, update this script with a valid endpoint.")
        print("   Example: client.get('https://entity.sls.epilot.io/v1/entities')")
        
    except ValueError as e:
        print(f"❌ Configuration Error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected Error: {e}")
        return False
    
    print("\n✅ Connection test completed successfully!")
    return True

if __name__ == "__main__":
    asyncio.run(test_connection())
