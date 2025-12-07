#!/usr/bin/env python3
"""
Add First Invoice Automation to Tarifabschluss Workflow

Creates an automation that:
- Triggers when "Erste Rechnung erstellen" step is completed
- Automatically generates and sends invoice email to customer
- Includes one month's charges for the product

Usage:
    python scripts/automations/create_invoice_automation.py
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
WORKFLOW_ID = "wfc5jpYf0r"  # Tarifabschluss - Vertragserfüllung

def create_first_invoice_automation() -> Dict[str, Any]:
    """
    Automation: Send invoice email when first invoice step is completed.
    
    Triggers on: "Erste Rechnung erstellen" step completion
    Action: Sends email with invoice details for first month
    """
    return {
        "flow_name": "Tarifabschluss: Erste Rechnung automatisch versenden",
        "entity_schema": "automation_step",
        "enabled": True,
        "triggers": [{
            "type": "entity_operation",
            "configuration": {
                "schema": "automation_step",
                "operation": ["update"],
                "attributes": ["status"]
            }
        }],
        "conditions": [
            {
                "id": "cond-first-invoice-step",
                "statements": [{
                    "operation": "equals",
                    "source": {
                        "schema": "automation_step",
                        "attribute": "id"
                    },
                    "values": ["step-first-invoice"]
                }]
            },
            {
                "id": "cond-step-done",
                "statements": [{
                    "operation": "equals",
                    "source": {
                        "schema": "automation_step",
                        "attribute": "status"
                    },
                    "values": ["DONE"]
                }]
            }
        ],
        "actions": [{
            "id": "action-send-invoice-email",
            "name": "Rechnung per E-Mail versenden",
            "type": "send-email",
            "condition_id": "cond-step-done",
            "config": {
                "to": ["{{order._relations.contacts.email}}"],
                "cc": ["buchhaltung@stadtwerke-wuelfrath.de"],
                "subject": "Ihre Rechnung von Stadtwerke Wülfrath - {{order._title}}",
                "body_html": """
                    <html>
                    <head>
                        <style>
                            body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; }
                            .header { background-color: #0066cc; color: white; padding: 20px; text-align: center; }
                            .content { padding: 20px; }
                            .invoice-box { border: 1px solid #ddd; padding: 15px; margin: 20px 0; background-color: #f9f9f9; }
                            .invoice-details { margin: 15px 0; }
                            .invoice-details table { width: 100%; border-collapse: collapse; }
                            .invoice-details th, .invoice-details td { padding: 10px; text-align: left; border-bottom: 1px solid #ddd; }
                            .invoice-details th { background-color: #f0f0f0; font-weight: bold; }
                            .total { font-size: 1.2em; font-weight: bold; margin-top: 15px; text-align: right; }
                            .footer { margin-top: 30px; padding-top: 20px; border-top: 1px solid #ddd; font-size: 0.9em; color: #666; }
                            .button { display: inline-block; padding: 12px 24px; background-color: #0066cc; color: white; text-decoration: none; border-radius: 4px; margin: 15px 0; }
                        </style>
                    </head>
                    <body>
                        <div class="header">
                            <h1>Stadtwerke Wülfrath</h1>
                            <p>Ihre Rechnung für {{order.products.name}}</p>
                        </div>
                        
                        <div class="content">
                            <h2>Sehr geehrte Damen und Herren,</h2>
                            
                            <p>vielen Dank für Ihr Vertrauen in die Stadtwerke Wülfrath. Anbei erhalten Sie Ihre erste Rechnung für den von Ihnen gewählten Tarif.</p>
                            
                            <div class="invoice-box">
                                <h3>Rechnungsdetails</h3>
                                <p><strong>Rechnungsnummer:</strong> R-{{order._id}}-001</p>
                                <p><strong>Rechnungsdatum:</strong> {{_now | date: 'DD.MM.YYYY'}}</p>
                                <p><strong>Kundennummer:</strong> {{order._relations.contacts._id}}</p>
                                <p><strong>Vertragsnummer:</strong> {{order._title}}</p>
                                <p><strong>Lieferzeitraum:</strong> {{order.delivery_date | date: 'DD.MM.YYYY'}} - {{order.delivery_date | date_add: 1, 'month' | date: 'DD.MM.YYYY'}}</p>
                            </div>
                            
                            <div class="invoice-details">
                                <h3>Leistungsübersicht</h3>
                                <table>
                                    <thead>
                                        <tr>
                                            <th>Position</th>
                                            <th>Beschreibung</th>
                                            <th>Menge</th>
                                            <th>Einzelpreis</th>
                                            <th>Gesamt</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        <tr>
                                            <td>1</td>
                                            <td>{{order.products.name}}<br><small>Tarif für {{order.products.category}}</small></td>
                                            <td>1 Monat</td>
                                            <td>{{order.products.price_amount}} {{order.products.price_currency}}</td>
                                            <td>{{order.products.price_amount}} {{order.products.price_currency}}</td>
                                        </tr>
                                        <tr>
                                            <td>2</td>
                                            <td>Grundgebühr</td>
                                            <td>1 Monat</td>
                                            <td>{{order.base_fee | default: '9.90'}} EUR</td>
                                            <td>{{order.base_fee | default: '9.90'}} EUR</td>
                                        </tr>
                                    </tbody>
                                </table>
                                
                                <div class="total">
                                    <p>Zwischensumme: {{order.total_amount | default: order.products.price_amount}} EUR</p>
                                    <p>MwSt. (19%): {{order.total_amount | default: order.products.price_amount | multiply: 0.19 | round: 2}} EUR</p>
                                    <p style="font-size: 1.3em; color: #0066cc;">
                                        <strong>Gesamtbetrag: {{order.total_amount | default: order.products.price_amount | multiply: 1.19 | round: 2}} EUR</strong>
                                    </p>
                                </div>
                            </div>
                            
                            <div style="margin: 30px 0;">
                                <h3>💳 Zahlungsinformationen</h3>
                                <p><strong>Zahlungsart:</strong> SEPA-Lastschrift</p>
                                <p><strong>Fälligkeitsdatum:</strong> {{_now | date_add: 14, 'days' | date: 'DD.MM.YYYY'}}</p>
                                <p>Der Betrag wird automatisch von Ihrem hinterlegten Konto eingezogen.</p>
                            </div>
                            
                            <div style="background-color: #e8f4f8; padding: 15px; border-left: 4px solid #0066cc; margin: 20px 0;">
                                <h4>📱 Online-Kundenportal</h4>
                                <p>Verwalten Sie Ihre Rechnungen und Verträge bequem online:</p>
                                <a href="https://portal.stadtwerke-wuelfrath.de/invoices/{{order._id}}" class="button">
                                    Rechnung im Portal ansehen
                                </a>
                            </div>
                            
                            <div class="footer">
                                <h4>Kontakt & Support</h4>
                                <p>
                                    <strong>Stadtwerke Wülfrath</strong><br>
                                    Wilhelmstraße 60, 42489 Wülfrath<br>
                                    Telefon: 02058 / 89 00<br>
                                    E-Mail: <a href="mailto:service@stadtwerke-wuelfrath.de">service@stadtwerke-wuelfrath.de</a><br>
                                    Web: <a href="https://www.stadtwerke-wuelfrath.de">www.stadtwerke-wuelfrath.de</a>
                                </p>
                                
                                <p style="margin-top: 20px; font-size: 0.85em; color: #888;">
                                    <strong>Geschäftsführung:</strong> Max Mustermann<br>
                                    <strong>Handelsregister:</strong> HRB 12345, Amtsgericht Wuppertal<br>
                                    <strong>USt-IdNr.:</strong> DE123456789<br>
                                    <strong>Steuer-Nr.:</strong> 123/4567/8901
                                </p>
                                
                                <p style="margin-top: 20px; font-size: 0.8em; color: #999;">
                                    Dies ist eine automatisch generierte E-Mail. Bei Fragen zu Ihrer Rechnung 
                                    kontaktieren Sie bitte unseren Kundenservice.
                                </p>
                            </div>
                        </div>
                    </body>
                    </html>
                """,
                "language_code": "de",
                "attach_documents": True
            }
        }]
    }

async def create_automation(client: EpilotClient, automation_config: Dict[str, Any]):
    """Create automation via API."""
    url = f"{AUTOMATION_API_BASE}/v1/automation/flows"
    
    try:
        result = await client.post(url, data=automation_config)
        return result
        
    except Exception as e:
        print(f"❌ Error creating automation: {e}")
        if hasattr(e, 'response'):
            try:
                error_detail = await e.response.json()
                print(f"   Details: {json.dumps(error_detail, indent=2)}")
            except:
                pass
        raise

async def main():
    """Main execution."""
    load_env()
    
    print("=" * 80)
    print("🧾 CREATING FIRST INVOICE AUTOMATION")
    print("=" * 80)
    print()
    print(f"Workflow ID: {WORKFLOW_ID}")
    print(f"Workflow: Tarifabschluss - Vertragserfüllung")
    print(f"Step: step-first-invoice (Erste Rechnung erstellen)")
    print()
    
    client = EpilotClient()
    
    # Create the automation
    automation_config = create_first_invoice_automation()
    
    print(f"Creating automation: {automation_config['flow_name']}")
    print(f"  Trigger: Step completion (step-first-invoice)")
    print(f"  Action: Send invoice email to customer")
    print()
    
    try:
        result = await create_automation(client, automation_config)
        auto_id = result.get('id')
        
        print(f"✅ Successfully created automation!")
        print(f"  ID: {auto_id}")
        print(f"  Name: {result.get('flow_name')}")
        print(f"  Status: {'✓ Enabled' if result.get('enabled') else '✗ Disabled'}")
        print()
        
        # Save to file
        output_file = Path(f"scripts/automations/output/automation_invoice_{auto_id}.json")
        output_file.parent.mkdir(parents=True, exist_ok=True)
        with open(output_file, 'w') as f:
            json.dump(result, f, indent=2)
        
        print(f"💾 Saved to: {output_file}")
        print()
        
        print("=" * 80)
        print("📧 INVOICE EMAIL AUTOMATION")
        print("=" * 80)
        print()
        print("✅ When: 'Erste Rechnung erstellen' step is marked as DONE")
        print("✅ Then: Automatically send invoice email to customer")
        print()
        print("Email includes:")
        print("  • Invoice details and billing period")
        print("  • Itemized charges (tariff + base fee)")
        print("  • Total amount with VAT")
        print("  • Payment information (SEPA direct debit)")
        print("  • Link to customer portal")
        print("  • Contact information")
        print()
        print("Recipients:")
        print("  • To: Customer email from order")
        print("  • CC: buchhaltung@stadtwerke-wuelfrath.de")
        print()
        print("🎉 Automation is now active and ready to use!")
        
    except Exception as e:
        print(f"❌ Failed to create automation: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
