#!/usr/bin/env python3
"""
Create Order in Epilot

Creates a new order entity in Epilot.

Usage:
    python scripts/orders/create_order.py --customer-id 12345 --title "New Order"
    python scripts/orders/create_order.py --customer-id 12345 --title "Order #001" --amount 299.99
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

async def create_order(customer_id: str, title: str, amount: float = None):
    """
    Create a new order in Epilot.
    
    Args:
        customer_id: ID of the customer entity
        title: Order title
        amount: Optional order amount
    """
    load_env()
    client = EpilotClient()
    
    print(f"🛒 Creating order: {title}\n")
    
    # Build order data
    order_data = {
        "_schema": "order",
        "_title": title,
        "customer": [{"$relation": [{"entity_id": customer_id}]}]
    }
    
    if amount is not None:
        order_data["amount_total"] = amount
    
    try:
        url = f"{ENTITY_API_BASE}/v1/entities"
        result = await client.post(url, data=order_data)
        
        order_id = result.get('_id', 'N/A')
        
        print("✅ Order created successfully!")
        print(f"   Order ID:    {order_id}")
        print(f"   Title:       {title}")
        print(f"   Customer ID: {customer_id}")
        if amount is not None:
            print(f"   Amount:      ${amount:.2f}")
        
    except Exception as e:
        print(f"❌ Error creating order: {e}")
        sys.exit(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create an order in Epilot")
    parser.add_argument("--customer-id", required=True, help="Customer entity ID")
    parser.add_argument("--title", required=True, help="Order title")
    parser.add_argument("--amount", type=float, help="Order amount")
    
    args = parser.parse_args()
    
    asyncio.run(create_order(args.customer_id, args.title, args.amount))
