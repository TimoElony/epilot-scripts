#!/usr/bin/env python3
"""
Create Automations for Ausbau Glasfaser Workflow

Creates useful automations to support the workflow:
1. Notify team when workflow step is completed
2. Send reminders for pending approval steps
3. Update opportunity status based on workflow phase
4. Notify customers when product becomes available

Usage:
    python scripts/automations/create_ausbau_automations.py
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
WORKFLOW_ID = "wfQpwhJF6J"

def create_automation_step_completed_notification() -> Dict[str, Any]:
    """
    Automation: Send email notification when workflow step is completed.
    Trigger: entity_operation on automation_step (workflow step completion)
    """
    return {
        "flow_name": "Ausbau Glasfaser: Step abgeschlossen - Team benachrichtigen",
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
                "id": "cond-workflow-id",
                "type": "expression",
                "config": {
                    "expression": f"automation_step.workflow_id == '{WORKFLOW_ID}'"
                }
            },
            {
                "id": "cond-status-done",
                "type": "expression",
                "config": {
                    "expression": "automation_step.status == 'DONE'"
                }
            }
        ],
        "actions": [
            {
                "id": "action-notify-team",
                "name": "Team Email senden",
                "type": "send-email",
                "allow_failure": True,
                "condition_id": "cond-status-done",
                "config": {
                    "to": ["team@stadtwerke-wuelfrath.de"],
                    "subject": "Workflow Step abgeschlossen: {{automation_step.name}}",
                    "body_html": """
                    <h2>Workflow Step abgeschlossen</h2>
                    <p><strong>Workflow:</strong> Ausbau Glasfaser</p>
                    <p><strong>Step:</strong> {{automation_step.name}}</p>
                    <p><strong>Abgeschlossen von:</strong> {{automation_step.completed_by}}</p>
                    <p><strong>Zeit:</strong> {{automation_step.completed_at}}</p>
                    <p><a href='https://portal.epilot.cloud/app/workflows/{{automation_step.workflow_id}}'>Workflow öffnen</a></p>
                    """,
                    "language_code": "de"
                }
            }
        ]
    }

def create_automation_approval_reminder() -> Dict[str, Any]:
    """
    Automation: Send reminder for pending approval steps (manual trigger).
    """
    return {
        "flow_name": "Ausbau Glasfaser: Freigabe-Erinnerung senden",
        "entity_schema": "automation_step",
        "enabled": True,
        "triggers": [{
            "type": "entity_manual",
            "configuration": {
                "schema": "automation_step"
            }
        }],
        "conditions": [
            {
                "id": "cond-is-approval-step",
                "type": "expression",
                "config": {
                    "expression": "automation_step.name.contains('FREIGABE')"
                }
            },
            {
                "id": "cond-status-open",
                "type": "expression",
                "config": {
                    "expression": "automation_step.status == 'OPEN'"
                }
            }
        ],
        "actions": [
            {
                "id": "action-send-reminder",
                "name": "Erinnerung an Sachbearbeiter",
                "type": "send-email",
                "allow_failure": False,
                "condition_id": "cond-status-open",
                "config": {
                    "to": ["{{automation_step.assigned_to.email}}"],
                    "subject": "Erinnerung: Freigabe erforderlich - {{automation_step.name}}",
                    "body_html": """
                    <h2>Freigabe erforderlich</h2>
                    <p>Dieser Workflow-Step wartet auf Ihre Freigabe:</p>
                    <p><strong>Workflow:</strong> Ausbau Glasfaser</p>
                    <p><strong>Step:</strong> {{automation_step.name}}</p>
                    <p><strong>Geöffnet seit:</strong> {{automation_step.created_at}}</p>
                    <p><a href='https://portal.epilot.cloud/app/workflows/{{automation_step.workflow_id}}'>Workflow öffnen und freigeben</a></p>
                    """,
                    "language_code": "de"
                }
            }
        ]
    }

def create_automation_update_opportunity_phase() -> Dict[str, Any]:
    """
    Automation: Update opportunity custom field based on workflow phase.
    Trigger: When entering a new workflow phase (section)
    """
    return {
        "flow_name": "Ausbau Glasfaser: Opportunity Phase aktualisieren",
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
                "id": "cond-workflow-match",
                "type": "expression",
                "config": {
                    "expression": f"automation_step.workflow_id == '{WORKFLOW_ID}'"
                }
            },
            {
                "id": "cond-step-done",
                "type": "expression",
                "config": {
                    "expression": "automation_step.status == 'DONE'"
                }
            }
        ],
        "actions": [
            {
                "id": "action-update-opportunity",
                "name": "Opportunity aktualisieren",
                "type": "map-entity",
                "allow_failure": True,
                "config": {
                    "target_schema": "opportunity",
                    "mapping_attributes": [
                        {
                            "id": "map-phase",
                            "target": "ausbau_phase",
                            "operation": {
                                "_copy": "automation_step.section_name"
                            }
                        },
                        {
                            "id": "map-last-update",
                            "target": "ausbau_last_update",
                            "operation": {
                                "_copy": "{{automation_step.completed_at}}"
                            }
                        },
                        {
                            "id": "map-tags",
                            "target": "_tags",
                            "operation": {
                                "_append": ["ausbau-in-progress"],
                                "_uniq": True
                            }
                        }
                    ],
                    "target_unique": ["_id"]
                }
            }
        ]
    }

def create_automation_notify_customer_availability() -> Dict[str, Any]:
    """
    Automation: Notify customers when product activation step is completed.
    Trigger: When "Produkte aktivieren" step is done
    """
    return {
        "flow_name": "Ausbau Glasfaser: Kunde über Verfügbarkeit benachrichtigen",
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
                "type": "expression",
                "config": {
                    "expression": "automation_step.id == 'step-product-activation'"
                }
            },
            {
                "id": "cond-done",
                "type": "expression",
                "config": {
                    "expression": "automation_step.status == 'DONE'"
                }
            }
        ],
        "actions": [
            {
                "id": "action-get-contacts",
                "name": "Interessierte Kontakte aus Opportunity laden",
                "type": "map-entity",
                "allow_failure": False,
                "config": {
                    "target_schema": "contact",
                    "mapping_attributes": []
                }
            },
            {
                "id": "action-notify-customers",
                "name": "Kunden Email senden",
                "type": "send-email",
                "allow_failure": True,
                "config": {
                    "to": ["{{opportunity._relations.contacts.email}}"],
                    "subject": "Gute Neuigkeiten! Glasfaser ist jetzt verfügbar",
                    "body_html": """
                    <h2>Glasfaser ist jetzt verfügbar!</h2>
                    <p>Sehr geehrte Damen und Herren,</p>
                    <p>wir freuen uns, Ihnen mitteilen zu können, dass in Ihrer Region nun Glasfaser-Internet verfügbar ist!</p>
                    <p><strong>Ihre Adresse:</strong> {{opportunity.address.street}} {{opportunity.address.street_number}}, {{opportunity.address.postal_code}} {{opportunity.address.city}}</p>
                    <p>Sie können jetzt einen Glasfaser-Tarif buchen:</p>
                    <p><a href='https://portal.epilot.cloud/app/journeys/879e1f89-426b-4dde-8e0a-8955f459220b' style='display:inline-block;padding:12px 24px;background:#0066cc;color:white;text-decoration:none;border-radius:4px;'>Jetzt Tarif auswählen</a></p>
                    <p>Mit freundlichen Grüßen,<br>Ihr Stadtwerke Wülfrath Team</p>
                    """,
                    "language_code": "de"
                }
            },
            {
                "id": "action-update-opportunity-available",
                "name": "Opportunity Status aktualisieren",
                "type": "map-entity",
                "allow_failure": True,
                "config": {
                    "target_schema": "opportunity",
                    "mapping_attributes": [
                        {
                            "id": "map-status",
                            "target": "status",
                            "operation": {
                                "_set": "geschlossen"
                            }
                        },
                        {
                            "id": "map-tags",
                            "target": "_tags",
                            "operation": {
                                "_append": ["glasfaser-verfuegbar", "kunden-benachrichtigt"],
                                "_uniq": True
                            }
                        }
                    ]
                }
            }
        ]
    }

async def create_automation(client: EpilotClient, automation_config: Dict[str, Any]):
    """Create an automation via API."""
    
    print(f"Creating: {automation_config['flow_name']}")
    
    # Use /flows (plural) endpoint for POST
    url = f"{AUTOMATION_API_BASE}/v1/automation/flows"
    
    try:
        result = await client.post(url, data=automation_config)
        automation_id = result.get('id', result.get('_id'))
        print(f"  ✅ Created: {automation_id}")
        return result
    except Exception as e:
        print(f"  ❌ Error: {str(e)}")
        if hasattr(e, 'response'):
            try:
                error_detail = await e.response.json()
                print(f"  📋 Details: {json.dumps(error_detail, indent=2)}")
            except:
                pass
        return None

async def main():
    """Main function."""
    load_env()
    client = EpilotClient()
    
    print("=" * 70)
    print("🤖 CREATE AUTOMATIONS FOR AUSBAU GLASFASER WORKFLOW")
    print("=" * 70)
    print()
    
    automations = [
        ("Step Completed Notification", create_automation_step_completed_notification()),
        ("Approval Reminder", create_automation_approval_reminder()),
        ("Update Opportunity Phase", create_automation_update_opportunity_phase()),
        ("Notify Customer Availability", create_automation_notify_customer_availability())
    ]
    
    created = []
    
    for name, config in automations:
        print(f"\n📝 {name}")
        print(f"   Trigger: {config['triggers'][0]['type']}")
        print(f"   Actions: {len(config['actions'])}")
        
        result = await create_automation(client, config)
        if result:
            created.append(result)
            
            # Save to file
            automation_id = result.get('id', result.get('_id'))
            output_file = Path(f"scripts/automations/output/automation_ausbau_{automation_id}.json")
            output_file.parent.mkdir(parents=True, exist_ok=True)
            with open(output_file, 'w') as f:
                json.dump(result, f, indent=2)
            print(f"  💾 Saved: {output_file}")
    
    print()
    print("=" * 70)
    print(f"✅ Created {len(created)} / {len(automations)} automations")
    print("=" * 70)
    print()
    print("Next steps:")
    print("1. Check automations in UI: https://portal.epilot.cloud/app/automations")
    print("2. Test workflow with real data")
    print("3. Adjust email templates as needed")
    print("4. Configure email addresses")

if __name__ == "__main__":
    asyncio.run(main())
