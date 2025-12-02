#!/usr/bin/env python3
"""
Example CSV Template Generator

Creates example CSV files for testing imports.

Usage:
    python scripts/utilities/create_example_csv.py
"""

import csv
from pathlib import Path

def create_customers_example():
    """Create an example customers CSV file."""
    output_dir = Path(__file__).parent.parent.parent / "data" / "input"
    output_file = output_dir / "customers_example.csv"
    
    # Example customer data
    customers = [
        {
            "first_name": "John",
            "last_name": "Doe",
            "email": "john.doe@example.com",
            "phone": "+49 123 456789"
        },
        {
            "first_name": "Jane",
            "last_name": "Smith",
            "email": "jane.smith@example.com",
            "phone": "+49 987 654321"
        },
        {
            "first_name": "Bob",
            "last_name": "Johnson",
            "email": "bob.johnson@example.com",
            "phone": "+49 555 123456"
        }
    ]
    
    # Write to CSV
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=["first_name", "last_name", "email", "phone"])
        writer.writeheader()
        writer.writerows(customers)
    
    return output_file

if __name__ == "__main__":
    print("📝 Creating example CSV files...\n")
    
    # Create customers example
    customers_file = create_customers_example()
    print(f"✅ Created: {customers_file}")
    print(f"\nYou can now import this file:")
    print(f"   python scripts/customers/import_customers_csv.py {customers_file}")
    
    print("\n💡 Edit this file to create your own customer data, then import it!")
