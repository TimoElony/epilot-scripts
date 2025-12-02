#!/usr/bin/env python3
"""
Import Customers from CSV

Reads a CSV file and creates customer entities in Epilot.

CSV Format:
    first_name,last_name,email,phone
    John,Doe,john@example.com,555-0100
    Jane,Smith,jane@example.com,555-0200

Usage:
    python scripts/customers/import_customers_csv.py input_file.csv
    python scripts/customers/import_customers_csv.py data/input/customers.csv
"""

import sys
import asyncio
import csv
from pathlib import Path

# Add lib to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from lib.auth import load_env
from lib.api_client import EpilotClient

ENTITY_API_BASE = "https://entity.sls.epilot.io"

async def import_customers(csv_file: str):
    """
    Import customers from CSV file.
    
    Args:
        csv_file: Path to CSV file
    """
    load_env()
    client = EpilotClient()
    
    csv_path = Path(csv_file)
    if not csv_path.exists():
        print(f"❌ Error: File not found: {csv_file}")
        sys.exit(1)
    
    print(f"📂 Reading customers from: {csv_file}\n")
    
    customers = []
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        customers = list(reader)
    
    print(f"✅ Found {len(customers)} customers to import\n")
    print("=" * 80)
    
    success_count = 0
    error_count = 0
    
    for i, customer in enumerate(customers, 1):
        first_name = customer.get('first_name', '')
        last_name = customer.get('last_name', '')
        email = customer.get('email', '')
        phone = customer.get('phone', '')
        
        title = f"{first_name} {last_name}".strip()
        
        print(f"\n{i}. Creating: {title}")
        
        # Build entity data
        entity_data = {
            "_schema": "contact",
            "_title": title,
            "first_name": first_name,
            "last_name": last_name,
            "email": [{"_email": email}] if email else [],
            "phone": [{"_phone": phone}] if phone else []
        }
        
        try:
            url = f"{ENTITY_API_BASE}/v1/entities"
            result = await client.post(url, data=entity_data)
            entity_id = result.get('_id', 'N/A')
            print(f"   ✅ Created - ID: {entity_id}")
            success_count += 1
            
        except Exception as e:
            print(f"   ❌ Error: {e}")
            error_count += 1
    
    print("\n" + "=" * 80)
    print(f"\n📊 Import Summary:")
    print(f"   Success: {success_count}")
    print(f"   Errors:  {error_count}")
    print(f"   Total:   {len(customers)}\n")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python scripts/customers/import_customers_csv.py <csv_file>")
        print("\nExample CSV format:")
        print("first_name,last_name,email,phone")
        print("John,Doe,john@example.com,555-0100")
        sys.exit(1)
    
    csv_file = sys.argv[1]
    asyncio.run(import_customers(csv_file))
