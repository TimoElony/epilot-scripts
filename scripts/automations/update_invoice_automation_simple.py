#!/usr/bin/env python3
"""
Update Invoice Automation - Use Simpler Email Format

If the HTML email isn't working, this creates a simpler text-based version
that's more likely to work with Epilot's email system.

Usage:
    python scripts/automations/update_invoice_automation_simple.py
"""

import sys
import asyncio
import json
from pathlib import Path
from typing import Dict, Any

# Add lib to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from lib.auth import load_env
from lib.api_client import EpilotClient

AUTOMATION_API_BASE = "https://automation.sls.epilot.io"
AUTOMATION_ID = "76918838-eedd-48ef-8990-ff813a8db4a4"

def create_simple_invoice_email_config() -> Dict[str, Any]:
    """
    Simpler email configuration without complex HTML.
    """
    return {
        "to": ["{{order._relations.contacts.email}}"],
        "cc": ["buchhaltung@stadtwerke-wuelfrath.de"],
        "subject": "Ihre Rechnung - Stadtwerke Wülfrath",
        "body": """Sehr geehrte Damen und Herren,

vielen Dank für Ihr Vertrauen in die Stadtwerke Wülfrath.

Ihre Rechnung für {{order.products.name}}:

Rechnungsnummer: R-{{order._id}}-001
Rechnungsdatum: {{_now | date: 'DD.MM.YYYY'}}
Vertragsnummer: {{order._title}}

Leistungsübersicht:
- {{order.products.name}}: {{order.products.price_amount}} EUR
- Grundgebühr: 9.90 EUR
- MwSt. (19%): {{order.products.price_amount | multiply: 1.19 | minus: order.products.price_amount | round: 2}} EUR

Gesamtbetrag: {{order.products.price_amount | multiply: 1.19 | round: 2}} EUR

Zahlungsart: SEPA-Lastschrift
Fällig am: {{_now | date_add: 14, 'days' | date: 'DD.MM.YYYY'}}

Bei Fragen erreichen Sie uns:
Telefon: 02058 / 89 00
E-Mail: service@stadtwerke-wuelfrath.de

Mit freundlichen Grüßen
Stadtwerke Wülfrath
""",
        "language_code": "de"
    }

async def update_automation(client: EpilotClient):
    """Update the automation with simpler email."""
    url = f"{AUTOMATION_API_BASE}/v1/automation/flows/{AUTOMATION_ID}"
    
    # Get current automation
    current = await client.get(url)
    
    print(f"Current automation: {current.get('flow_name')}")
    print(f"Status: {'✓ Enabled' if current.get('enabled') else '✗ Disabled'}")
    print()
    
    # Update the email action
    actions = current.get('actions', [])
    if actions:
        actions[0]['config'] = create_simple_invoice_email_config()
    
    # Update
    update_payload = {
        "flow_name": current['flow_name'],
        "entity_schema": current['entity_schema'],
        "enabled": current['enabled'],
        "triggers": current['triggers'],
        "conditions": current['conditions'],
        "actions": actions
    }
    
    result = await client.put(url, data=update_payload)
    return result

async def main():
    """Main execution."""
    load_env()
    
    print("=" * 80)
    print("🔄 UPDATING INVOICE AUTOMATION TO SIMPLE FORMAT")
    print("=" * 80)
    print()
    
    client = EpilotClient()
    
    try:
        result = await update_automation(client)
        
        print("✅ Successfully updated automation!")
        print(f"  ID: {result.get('id')}")
        print(f"  Name: {result.get('flow_name')}")
        print()
        print("Changed to simpler text-based email format")
        print("This should work better with Epilot's email system")
        
        # Save
        output_file = Path(f"scripts/automations/output/automation_invoice_{result.get('id')}_simple.json")
        with open(output_file, 'w') as f:
            json.dump(result, f, indent=2)
        print(f"\n💾 Saved to: {output_file}")
        
    except Exception as e:
        print(f"❌ Failed: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
