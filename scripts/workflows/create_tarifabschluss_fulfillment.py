#!/usr/bin/env python3
"""
Create Tarifabschluss Fulfillment Workflow and Automation

Creates a complete fulfillment workflow for tariff contracts that includes:
1. Contract processing
2. Technical setup
3. Service activation
4. Customer onboarding

Also updates the Tarifabschluss automation to trigger this workflow.

Usage:
    python scripts/workflows/create_tarifabschluss_fulfillment.py
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

WORKFLOW_API_BASE = "https://workflows-definition.sls.epilot.io"
AUTOMATION_API_BASE = "https://automation.sls.epilot.io"

def create_tarifabschluss_fulfillment_workflow() -> Dict[str, Any]:
    """
    Create comprehensive fulfillment workflow for tariff contracts.
    
    This workflow guides Stadtwerke staff through the complete process from
    contract submission to activated customer.
    """
    return {
        "name": "Tarifabschluss - Vertragserfüllung",
        "description": """
Kompletter Erfüllungsprozess für Tarifabschlüsse (Strom, Gas, Wasser, Fernwärme, Glasfaser).

Führt Stadtwerke-Mitarbeiter durch alle notwendigen Schritte vom eingegangenen 
Vertragsabschluss bis zum aktivierten Kunden mit funktionierendem Anschluss.

Schmerzpunkte die adressiert werden:
- Klare Aufgabenverteilung zwischen Abteilungen
- Keine vergessenen Schritte (Freigaben, Prüfungen, Aktivierungen)
- Automatische Kundenbenachrichtigungen
- Nachverfolgbarkeit des Bearbeitungsstands
        """.strip(),
        "enabled": True,
        "flow": [
            # Phase 1: Vertragsbearbeitung (Contract Processing)
            {
                "id": "phase-contract-processing",
                "name": "Phase 1: Vertragsbearbeitung",
                "type": "SECTION",
                "order": 1,
                "steps": [
                    {
                        "id": "step-contract-received",
                        "name": "Vertrag eingegangen - Vollständigkeit prüfen",
                        "type": "STEP",
                        "order": 2,
                        "assignedTo": [],
                        "userIds": [],
                        "ecp": {"enabled": False},
                        "installer": {"enabled": False}
                    },
                    {
                        "id": "step-credit-check",
                        "name": "Bonitätsprüfung durchführen",
                        "type": "STEP",
                        "order": 3,
                        "assignedTo": [],
                        "userIds": [],
                        "ecp": {"enabled": False},
                        "installer": {"enabled": False}
                    },
                    {
                        "id": "step-contract-review",
                        "name": "Vertragsdaten im System anlegen",
                        "type": "STEP",
                        "order": 4,
                        "assignedTo": [],
                        "userIds": [],
                        "ecp": {"enabled": False},
                        "installer": {"enabled": False}
                    },
                    {
                        "id": "step-approval-contract",
                        "name": "🔒 FREIGABE: Vertrag genehmigt",
                        "type": "STEP",
                        "order": 5,
                        "assignedTo": [],
                        "userIds": [],
                        "ecp": {"enabled": False},
                        "installer": {"enabled": False}
                    }
                ]
            },
            
            # Phase 2: Technische Prüfung (Technical Assessment)
            {
                "id": "phase-technical-check",
                "name": "Phase 2: Technische Prüfung",
                "type": "SECTION",
                "order": 6,
                "steps": [
                    {
                        "id": "step-address-verification",
                        "name": "Adresse im Versorgungsgebiet prüfen",
                        "type": "STEP",
                        "order": 7,
                        "assignedTo": [],
                        "userIds": [],
                        "ecp": {"enabled": False},
                        "installer": {"enabled": False}
                    },
                    {
                        "id": "step-grid-connection-check",
                        "name": "Netzanschluss prüfen (Strom/Gas/Wasser)",
                        "type": "STEP",
                        "order": 8,
                        "assignedTo": [],
                        "userIds": [],
                        "ecp": {"enabled": False},
                        "installer": {"enabled": False}
                    },
                    {
                        "id": "step-fiber-availability",
                        "name": "Glasfaser-Verfügbarkeit prüfen (nur Glasfaser)",
                        "type": "STEP",
                        "order": 9,
                        "assignedTo": [],
                        "userIds": [],
                        "ecp": {"enabled": False},
                        "installer": {"enabled": False}
                    },
                    {
                        "id": "step-approval-technical",
                        "name": "🔒 FREIGABE: Technisch umsetzbar",
                        "type": "STEP",
                        "order": 10,
                        "assignedTo": [],
                        "userIds": [],
                        "ecp": {"enabled": False},
                        "installer": {"enabled": False}
                    }
                ]
            },
            
            # Phase 3: Lieferantenwechsel (Supplier Switch)
            {
                "id": "phase-supplier-switch",
                "name": "Phase 3: Lieferantenwechsel (bei Wechsel)",
                "type": "SECTION",
                "order": 11,
                "steps": [
                    {
                        "id": "step-previous-supplier",
                        "name": "Bisherigen Lieferanten ermitteln",
                        "type": "STEP",
                        "order": 12,
                        "assignedTo": [],
                        "userIds": [],
                        "ecp": {"enabled": False},
                        "installer": {"enabled": False}
                    },
                    {
                        "id": "step-cancellation-notice",
                        "name": "Kündigung beim Altanbieter einreichen",
                        "type": "STEP",
                        "order": 13,
                        "assignedTo": [],
                        "userIds": [],
                        "ecp": {"enabled": False},
                        "installer": {"enabled": False}
                    },
                    {
                        "id": "step-metering-point-registration",
                        "name": "Marktlokation/Zählpunkt anmelden",
                        "type": "STEP",
                        "order": 14,
                        "assignedTo": [],
                        "userIds": [],
                        "ecp": {"enabled": False},
                        "installer": {"enabled": False}
                    },
                    {
                        "id": "step-approval-switch",
                        "name": "🔒 FREIGABE: Wechsel abgeschlossen",
                        "type": "STEP",
                        "order": 15,
                        "assignedTo": [],
                        "userIds": [],
                        "ecp": {"enabled": False},
                        "installer": {"enabled": False}
                    }
                ]
            },
            
            # Phase 4: Installation & Inbetriebnahme (Installation & Commissioning)
            {
                "id": "phase-installation",
                "name": "Phase 4: Installation & Inbetriebnahme",
                "type": "SECTION",
                "order": 16,
                "steps": [
                    {
                        "id": "step-meter-installation",
                        "name": "Zähler einbauen (falls erforderlich)",
                        "type": "STEP",
                        "order": 17,
                        "assignedTo": [],
                        "userIds": [],
                        "ecp": {"enabled": False},
                        "installer": {"enabled": True}  # Mobile for meter installation
                    },
                    {
                        "id": "step-fiber-installation",
                        "name": "📱 Glasfaser-Modem installieren (nur Glasfaser)",
                        "type": "STEP",
                        "order": 18,
                        "assignedTo": [],
                        "userIds": [],
                        "ecp": {"enabled": False},
                        "installer": {"enabled": True}  # Mobile installation
                    },
                    {
                        "id": "step-service-activation",
                        "name": "Dienst aktivieren und testen",
                        "type": "STEP",
                        "order": 19,
                        "assignedTo": [],
                        "userIds": [],
                        "ecp": {"enabled": False},
                        "installer": {"enabled": False}
                    },
                    {
                        "id": "step-approval-activation",
                        "name": "🔒 FREIGABE: Service aktiviert",
                        "type": "STEP",
                        "order": 20,
                        "assignedTo": [],
                        "userIds": [],
                        "ecp": {"enabled": False},
                        "installer": {"enabled": False}
                    }
                ]
            },
            
            # Phase 5: Kundenbetreuung & Abschluss (Customer Care & Completion)
            {
                "id": "phase-customer-care",
                "name": "Phase 5: Kundenbetreuung & Abschluss",
                "type": "SECTION",
                "order": 21,
                "steps": [
                    {
                        "id": "step-welcome-package",
                        "name": "Willkommenspaket versenden",
                        "type": "STEP",
                        "order": 22,
                        "assignedTo": [],
                        "userIds": [],
                        "ecp": {"enabled": False},
                        "installer": {"enabled": False}
                    },
                    {
                        "id": "step-first-invoice",
                        "name": "Erste Rechnung erstellen",
                        "type": "STEP",
                        "order": 23,
                        "assignedTo": [],
                        "userIds": [],
                        "ecp": {"enabled": False},
                        "installer": {"enabled": False}
                    },
                    {
                        "id": "step-customer-satisfaction",
                        "name": "Kundenzufriedenheit erfassen",
                        "type": "STEP",
                        "order": 24,
                        "assignedTo": [],
                        "userIds": [],
                        "ecp": {"enabled": False},
                        "installer": {"enabled": False}
                    },
                    {
                        "id": "step-final-approval",
                        "name": "🔒 FREIGABE: Vertragserfüllung abgeschlossen",
                        "type": "STEP",
                        "order": 25,
                        "assignedTo": [],
                        "userIds": [],
                        "ecp": {"enabled": False},
                        "installer": {"enabled": False}
                    }
                ]
            }
        ]
    }

async def create_workflow(client: EpilotClient):
    """Create the fulfillment workflow via API."""
    
    workflow_def = create_tarifabschluss_fulfillment_workflow()
    
    print("=" * 80)
    print("🔄 CREATING TARIFABSCHLUSS FULFILLMENT WORKFLOW")
    print("=" * 80)
    print()
    print(f"Name: {workflow_def['name']}")
    print(f"Phases: 5")
    print(f"Steps: 24")
    print(f"Mobile Steps: 2 (Meter + Fiber installation)")
    print(f"Approval Gates: 5")
    print()
    
    try:
        url = f"{WORKFLOW_API_BASE}/v1/workflows/definitions"
        result = await client.post(url, data=workflow_def)
        
        workflow_id = result.get('id', 'N/A')
        
        print("✅ Workflow created successfully!")
        print(f"   ID: {workflow_id}")
        print()
        
        # Save workflow
        output_file = Path(f"scripts/workflows/output/workflow_tarifabschluss_{workflow_id}.json")
        output_file.parent.mkdir(parents=True, exist_ok=True)
        with open(output_file, 'w') as f:
            json.dump(result, f, indent=2)
        print(f"💾 Saved: {output_file}")
        print()
        
        return result
        
    except Exception as e:
        print(f"❌ Error creating workflow: {e}")
        return None

async def update_tarifabschluss_automation(client: EpilotClient, workflow_id: str):
    """
    Find and update the Tarifabschluss automation to trigger the new workflow.
    """
    
    print("=" * 80)
    print("🔄 UPDATING TARIFABSCHLUSS AUTOMATION")
    print("=" * 80)
    print()
    
    # Find existing automation
    print("📋 Searching for 'Journey Automation: Tarifabschluss'...")
    try:
        url = f"{AUTOMATION_API_BASE}/v1/automation/flows"
        automations = await client.get(url)
        
        tarifabschluss_automation = None
        for auto in automations:
            if "Tarifabschluss" in auto.get('flow_name', ''):
                tarifabschluss_automation = auto
                break
        
        if not tarifabschluss_automation:
            print("❌ Could not find Tarifabschluss automation")
            return None
        
        auto_id = tarifabschluss_automation['id']
        print(f"✅ Found automation: {auto_id}")
        print(f"   Current actions: {len(tarifabschluss_automation.get('actions', []))}")
        print()
        
        # Add trigger-workflow action
        print("➕ Adding trigger-workflow action...")
        
        actions = tarifabschluss_automation.get('actions', [])
        
        # Add new action to trigger workflow on order
        new_action = {
            "id": "action-trigger-fulfillment-workflow",
            "name": "Start Vertragserfüllungs-Workflow",
            "type": "trigger-workflow",
            "allow_failure": False,
            "config": {
                "target_workflow": workflow_id,
                "filter_with_purposes": False
            }
        }
        
        actions.append(new_action)
        
        # Update automation
        update_payload = {
            "flow_name": tarifabschluss_automation['flow_name'],
            "entity_schema": tarifabschluss_automation['entity_schema'],
            "enabled": tarifabschluss_automation['enabled'],
            "triggers": tarifabschluss_automation['triggers'],
            "conditions": tarifabschluss_automation.get('conditions', []),
            "actions": actions
        }
        
        update_url = f"{AUTOMATION_API_BASE}/v1/automation/flows/{auto_id}"
        result = await client.put(update_url, data=update_payload)
        
        print("✅ Automation updated!")
        print(f"   New action count: {len(result.get('actions', []))}")
        print()
        
        # Save updated automation
        output_file = Path(f"scripts/automations/output/automation_tarifabschluss_{auto_id}_updated.json")
        output_file.parent.mkdir(parents=True, exist_ok=True)
        with open(output_file, 'w') as f:
            json.dump(result, f, indent=2)
        print(f"💾 Saved: {output_file}")
        print()
        
        return result
        
    except Exception as e:
        print(f"❌ Error updating automation: {e}")
        import traceback
        traceback.print_exc()
        return None

async def create_notification_automations(client: EpilotClient, workflow_id: str):
    """
    Create supporting automations for the fulfillment workflow.
    """
    
    print("=" * 80)
    print("🔄 CREATING SUPPORTING AUTOMATIONS")
    print("=" * 80)
    print()
    
    automations = []
    
    # Automation 1: Customer activation notification
    auto1 = {
        "flow_name": "Tarifabschluss: Kunde über Aktivierung benachrichtigen",
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
                "id": "cond-activation-step",
                "statements": [{
                    "operation": "equals",
                    "source": {
                        "schema": "automation_step",
                        "attribute": "id"
                    },
                    "values": ["step-service-activation"]
                }]
            },
            {
                "id": "cond-done",
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
            "id": "action-notify-customer",
            "name": "Kunde über Aktivierung informieren",
            "type": "send-email",
            "condition_id": "cond-done",
            "config": {
                "to": ["{{order._relations.contacts.email}}"],
                "subject": "Ihr Tarif ist jetzt aktiv!",
                "body_html": """
                    <h2>Willkommen bei Stadtwerke Wülfrath!</h2>
                    <p>Ihr Tarif wurde erfolgreich aktiviert.</p>
                    <p><strong>Vertragsnummer:</strong> {{order._title}}</p>
                    <p><strong>Tarif:</strong> {{order.products.name}}</p>
                    <p><strong>Lieferbeginn:</strong> {{order.delivery_date}}</p>
                    <p>Sie können jetzt Ihr Online-Kundenportal nutzen:</p>
                    <p><a href='https://portal.stadtwerke-wuelfrath.de'>Zum Kundenportal</a></p>
                    <p>Bei Fragen erreichen Sie uns unter: service@stadtwerke-wuelfrath.de</p>
                """,
                "language_code": "de"
            }
        }]
    }
    
    # Automation 2: Staff notification on bottlenecks
    auto2 = {
        "flow_name": "Tarifabschluss: Team bei Freigabe benachrichtigen",
        "entity_schema": "automation_step",
        "enabled": True,
        "triggers": [{
            "type": "entity_manual"
        }],
        "conditions": [{
            "id": "cond-approval-step",
            "statements": [{
                "operation": "contains",
                "source": {
                    "schema": "automation_step",
                    "attribute": "name"
                },
                "values": ["FREIGABE"]
            }]
        }],
        "actions": [{
            "id": "action-notify-team",
            "name": "Erinnerung an zuständigen Mitarbeiter",
            "type": "send-email",
            "condition_id": "cond-approval-step",
            "config": {
                "to": ["{{automation_step.assigned_to.email}}"],
                "subject": "Freigabe erforderlich: {{automation_step.name}}",
                "body_html": """
                    <h2>Freigabe erforderlich</h2>
                    <p>Workflow: Tarifabschluss - Vertragserfüllung</p>
                    <p><strong>Step:</strong> {{automation_step.name}}</p>
                    <p><strong>Auftrag:</strong> {{order._title}}</p>
                    <p><a href='https://portal.epilot.cloud/app/orders/{{order._id}}'>Auftrag öffnen</a></p>
                """,
                "language_code": "de"
            }
        }]
    }
    
    for i, auto_config in enumerate([auto1, auto2], 1):
        print(f"Creating automation {i}/2: {auto_config['flow_name']}")
        try:
            url = f"{AUTOMATION_API_BASE}/v1/automation/flows"
            result = await client.post(url, data=auto_config)
            automations.append(result)
            
            auto_id = result.get('id')
            print(f"  ✅ Created: {auto_id}")
            
            # Save
            output_file = Path(f"scripts/automations/output/automation_tarifabschluss_support_{auto_id}.json")
            output_file.parent.mkdir(parents=True, exist_ok=True)
            with open(output_file, 'w') as f:
                json.dump(result, f, indent=2)
            print(f"  💾 Saved: {output_file}")
            
        except Exception as e:
            print(f"  ❌ Error: {e}")
        
        print()
    
    return automations

async def main():
    """Main function."""
    load_env()
    client = EpilotClient()
    
    print()
    print("=" * 80)
    print("🎯 TARIFABSCHLUSS FULFILLMENT WORKFLOW SETUP")
    print("=" * 80)
    print()
    print("This script will:")
    print("  1. Create comprehensive fulfillment workflow (5 phases, 24 steps)")
    print("  2. Update Tarifabschluss automation to trigger workflow")
    print("  3. Create 2 supporting automations (notifications)")
    print()
    print("=" * 80)
    print()
    
    # Step 1: Create workflow
    workflow_result = await create_workflow(client)
    
    if not workflow_result:
        print("\n❌ Failed to create workflow. Exiting.")
        return
    
    workflow_id = workflow_result['id']
    
    # Step 2: Update automation
    automation_result = await update_tarifabschluss_automation(client, workflow_id)
    
    # Step 3: Create support automations
    support_automations = await create_notification_automations(client, workflow_id)
    
    # Summary
    print()
    print("=" * 80)
    print("✅ SETUP COMPLETE!")
    print("=" * 80)
    print()
    print(f"📋 Workflow Created: {workflow_id}")
    print(f"   Name: Tarifabschluss - Vertragserfüllung")
    print(f"   Phases: 5")
    print(f"   Steps: 24")
    print(f"   Status: Enabled")
    print()
    print("🔗 Automation Updated:")
    if automation_result:
        print(f"   Journey Automation: Tarifabschluss")
        print(f"   Now triggers workflow on order creation")
    else:
        print("   ⚠️  Manual update required")
    print()
    print(f"🤖 Support Automations: {len(support_automations)}")
    print("   1. Customer activation notification")
    print("   2. Team approval reminders")
    print()
    print("🎯 Next Time a Customer Completes Tarifabschluss Journey:")
    print("   ✅ Submission created")
    print("   ✅ Contacts created")
    print("   ✅ Order created")
    print("   ✅ Opportunity created")
    print("   ✅ Workflow started on Order! ← NEW!")
    print()
    print("📊 View in Portal:")
    print("   Workflows: https://portal.epilot.cloud/app/workflows")
    print("   Automations: https://portal.epilot.cloud/app/automations")
    print()

if __name__ == "__main__":
    asyncio.run(main())
