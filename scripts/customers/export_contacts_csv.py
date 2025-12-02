#!/usr/bin/env python3
"""
Export Epilot Contacts to CSV

Retrieves all contacts from the Epilot Entity API and exports them to a CSV file.

Usage:
    python scripts/customers/export_contacts_csv.py
    python scripts/customers/export_contacts_csv.py --output data/output/contacts.csv
    python scripts/customers/export_contacts_csv.py --limit 100
"""

import sys
import asyncio
import argparse
import csv
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any

# Add lib to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from lib.auth import load_env
from lib.api_client import EpilotClient

ENTITY_API_BASE = "https://entity.sls.epilot.io"

async def fetch_all_contacts(client: EpilotClient, limit: int = None) -> List[Dict[str, Any]]:
    """
    Fetch all contacts from Epilot with pagination.
    
    Args:
        client: EpilotClient instance
        limit: Optional limit for total contacts to fetch
    
    Returns:
        List of contact entities
    """
    all_contacts = []
    from_offset = 0
    page_size = 100
    
    print("📥 Fetching contacts from Epilot...")
    
    while True:
        payload = {
            "q": "_schema:contact",
            "from": from_offset,
            "size": page_size,
            "hydrate": True
        }
        
        try:
            url = f"{ENTITY_API_BASE}/v1/entity:search"
            result = await client.post(url, data=payload)
            
            entities = result.get('results', [])
            total = result.get('total', 0)
            
            if not entities:
                break
            
            all_contacts.extend(entities)
            print(f"   Fetched {len(all_contacts)}/{total} contacts...")
            
            # Check if we've reached the limit or end
            if limit and len(all_contacts) >= limit:
                all_contacts = all_contacts[:limit]
                break
            
            if len(all_contacts) >= total:
                break
            
            from_offset += page_size
            
        except Exception as e:
            print(f"❌ Error fetching contacts: {e}")
            break
    
    return all_contacts

def flatten_contact(contact: Dict[str, Any]) -> Dict[str, str]:
    """
    Flatten contact entity into CSV-friendly format.
    
    Args:
        contact: Contact entity from API
    
    Returns:
        Flattened dictionary with string values
    """
    flattened = {
        'id': contact.get('_id', ''),
        'title': contact.get('_title', ''),
        'schema': contact.get('_schema', ''),
        'created_at': contact.get('_created_at', ''),
        'updated_at': contact.get('_updated_at', ''),
    }
    
    # Extract common contact fields
    fields_to_extract = [
        'first_name', 'last_name', 'email', 'phone',
        'salutation', 'company', 'street', 'city',
        'postal_code', 'country', 'status'
    ]
    
    for field in fields_to_extract:
        value = contact.get(field)
        if value is not None:
            # Handle lists (like email arrays)
            if isinstance(value, list):
                if len(value) > 0:
                    # For email/phone arrays, get the first one
                    if isinstance(value[0], dict):
                        flattened[field] = value[0].get('email', value[0].get('phone', str(value[0])))
                    else:
                        flattened[field] = str(value[0])
                else:
                    flattened[field] = ''
            else:
                flattened[field] = str(value)
        else:
            flattened[field] = ''
    
    return flattened

async def export_contacts_to_csv(output_path: str, limit: int = None):
    """
    Export all contacts to CSV file.
    
    Args:
        output_path: Path to output CSV file
        limit: Optional limit for number of contacts to export
    """
    load_env()
    client = EpilotClient()
    
    print("🔄 Starting contact export...\n")
    
    try:
        # Fetch all contacts
        contacts = await fetch_all_contacts(client, limit)
        
        if not contacts:
            print("⚠️  No contacts found.")
            return
        
        print(f"\n✅ Retrieved {len(contacts)} contacts")
        
        # Flatten contacts for CSV
        flattened_contacts = [flatten_contact(contact) for contact in contacts]
        
        # Get all unique field names
        all_fields = set()
        for contact in flattened_contacts:
            all_fields.update(contact.keys())
        
        # Sort fields for consistent ordering
        fieldnames = sorted(all_fields)
        
        # Ensure key fields come first
        priority_fields = ['id', 'title', 'first_name', 'last_name', 'email', 'phone']
        for field in reversed(priority_fields):
            if field in fieldnames:
                fieldnames.remove(field)
                fieldnames.insert(0, field)
        
        # Create output directory if it doesn't exist
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        # Write to CSV
        print(f"\n💾 Writing to {output_path}...")
        with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(flattened_contacts)
        
        print(f"✅ Successfully exported {len(contacts)} contacts to {output_path}")
        print(f"📊 Columns: {', '.join(fieldnames[:5])}{'...' if len(fieldnames) > 5 else ''}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Export Epilot contacts to CSV")
    parser.add_argument(
        "--output", 
        default="data/output/contacts_export.csv",
        help="Output CSV file path"
    )
    parser.add_argument(
        "--limit", 
        type=int,
        help="Limit number of contacts to export (for testing)"
    )
    
    args = parser.parse_args()
    
    # Add timestamp to filename if using default
    if args.output == "data/output/contacts_export.csv":
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        args.output = f"data/output/contacts_export_{timestamp}.csv"
    
    asyncio.run(export_contacts_to_csv(args.output, args.limit))
