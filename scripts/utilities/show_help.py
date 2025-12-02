#!/usr/bin/env python3
"""
Project Overview Generator

Creates a summary of all available scripts in the repository.

Usage:
    python scripts/utilities/show_help.py
"""

from pathlib import Path

def show_help():
    print("=" * 80)
    print("🚀 EPILOT API SCRIPTS - PROJECT OVERVIEW")
    print("=" * 80)
    print()
    
    print("📂 PROJECT STRUCTURE:")
    print()
    print("  config/              → API configuration")
    print("  lib/                 → Reusable library code")
    print("  scripts/")
    print("    ├── entities/      → Entity management")
    print("    ├── customers/     → Customer operations")
    print("    ├── orders/        → Order management")
    print("    └── utilities/     → Helper scripts")
    print("  data/")
    print("    ├── input/         → Your CSV/input files")
    print("    └── output/        → Script results")
    print()
    
    print("🔧 AVAILABLE SCRIPTS:")
    print()
    print("  UTILITIES:")
    print("    python scripts/utilities/list_all_apis.py")
    print("      → List all 37 Epilot APIs")
    print()
    print("    python scripts/utilities/test_connection.py")
    print("      → Test your API authentication")
    print()
    print("    python scripts/utilities/create_example_csv.py")
    print("      → Create example CSV files for testing")
    print()
    
    print("  ENTITIES:")
    print("    python scripts/entities/list_entities.py [--schema TYPE] [--limit N]")
    print("      → List entities from Epilot")
    print()
    print("    python scripts/entities/create_entity.py --schema TYPE --title NAME")
    print("      → Create a new entity")
    print()
    
    print("  CUSTOMERS:")
    print("    python scripts/customers/import_customers_csv.py FILE.csv")
    print("      → Import customers from CSV file")
    print()
    
    print("  ORDERS:")
    print("    python scripts/orders/create_order.py --customer-id ID --title NAME")
    print("      → Create a new order")
    print()
    
    print("=" * 80)
    print("📚 DOCUMENTATION:")
    print("=" * 80)
    print()
    print("  README.md       → Full documentation")
    print("  QUICKSTART.md   → Quick setup guide")
    print("  .env.example    → Environment configuration template")
    print()
    
    print("🎯 NEXT STEPS:")
    print()
    print("  1. Copy .env.example to .env and add your API token")
    print("  2. Run: python scripts/utilities/test_connection.py")
    print("  3. Run: python scripts/utilities/list_all_apis.py")
    print("  4. Start using the scripts or create your own!")
    print()
    print("💡 TIP: Ask GitHub Copilot to help create custom scripts!")
    print()
    print("=" * 80)

if __name__ == "__main__":
    show_help()
