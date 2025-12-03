#!/usr/bin/env python3
"""
Erstelle vereinfachte Haustürverkauf Journey für Wülfrath

Erstellt eine optimierte Journey für Tablet-Nutzung durch Außendienstmitarbeiter
mit Verfügbarkeitsprüfung und automatischer Workflow-Triggerung bei fehlender Verfügbarkeit.

Verwendung:
    python scripts/demo/erstelle_hausturverkauf_journey.py
"""

import sys
import asyncio
import json
from pathlib import Path
from datetime import datetime

# Add lib to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from lib.auth import load_env
from lib.api_client import EpilotClient

JOURNEY_API_BASE = "https://journey-config.sls.epilot.io"
AUTOMATION_API_BASE = "https://automation.sls.epilot.io"

# Simplified Journey Configuration for Door-to-Door Sales
JOURNEY_CONFIG = {
    "name": "Wülfrath Haustürverkauf - Glasfaser",
    "design_id": None,  # Will use default design
    "settings": {
        "display_mode": "stepper",
        "show_progress": True,
        "mobile_optimized": True
    },
    "steps": [
        {
            "id": "step_01_welcome",
            "name": "Willkommen",
            "schema": {
                "blocks": [
                    {
                        "type": "content",
                        "content": {
                            "title": "Glasfaser für Wülfrath",
                            "description": "Prüfen Sie jetzt die Verfügbarkeit für ultraschnelles Internet an Ihrer Adresse.",
                            "image_url": None
                        }
                    }
                ]
            }
        },
        {
            "id": "step_02_address",
            "name": "Adresse & Verfügbarkeit",
            "schema": {
                "blocks": [
                    {
                        "type": "address",
                        "id": "customer_address",
                        "label": "Ihre Anschrift",
                        "required": True,
                        "fields": {
                            "street": True,
                            "house_number": True,
                            "postal_code": True,
                            "city": True
                        },
                        "default_values": {
                            "postal_code": "42489",
                            "city": "Wülfrath"
                        }
                    },
                    {
                        "type": "availability_check",
                        "id": "glasfaser_verfuegbarkeit",
                        "label": "Verfügbarkeit prüfen",
                        "api_endpoint": "/api/check-availability",
                        "check_on_blur": True,
                        "services": ["glasfaser", "ftth", "fttc"]
                    }
                ]
            }
        },
        {
            "id": "step_03_contact",
            "name": "Kontaktdaten",
            "schema": {
                "blocks": [
                    {
                        "type": "contact",
                        "id": "customer_contact",
                        "label": "Ihre Kontaktdaten",
                        "required": True,
                        "fields": {
                            "salutation": True,
                            "first_name": True,
                            "last_name": True,
                            "email": True,
                            "phone": True
                        }
                    }
                ]
            }
        },
        {
            "id": "step_04_product_selection",
            "name": "Tarifauswahl",
            "condition": {
                "field": "glasfaser_verfuegbarkeit.available",
                "operator": "equals",
                "value": True
            },
            "schema": {
                "blocks": [
                    {
                        "type": "product",
                        "id": "glasfaser_tarif",
                        "label": "Wählen Sie Ihren Glasfaser-Tarif",
                        "required": True,
                        "product_filter": {
                            "category": "glasfaser",
                            "tags": ["wuelfrath"]
                        },
                        "display_mode": "cards"
                    }
                ]
            }
        },
        {
            "id": "step_05_no_availability",
            "name": "Noch keine Verfügbarkeit",
            "condition": {
                "field": "glasfaser_verfuegbarkeit.available",
                "operator": "equals",
                "value": False
            },
            "schema": {
                "blocks": [
                    {
                        "type": "content",
                        "content": {
                            "title": "Leider noch nicht verfügbar",
                            "description": "An Ihrer Adresse ist Glasfaser aktuell noch nicht verfügbar. Wir prüfen gerne die Möglichkeit eines Ausbaus für Ihr Gebiet."
                        }
                    },
                    {
                        "type": "radio",
                        "id": "ausbau_interesse",
                        "label": "Möchten Sie über einen möglichen Ausbau informiert werden?",
                        "required": True,
                        "options": [
                            {"value": "ja", "label": "Ja, bitte informieren Sie mich"},
                            {"value": "nein", "label": "Nein, danke"}
                        ]
                    }
                ]
            }
        },
        {
            "id": "step_06_confirmation",
            "name": "Zusammenfassung",
            "schema": {
                "blocks": [
                    {
                        "type": "summary",
                        "id": "order_summary",
                        "label": "Ihre Bestellung",
                        "show_fields": [
                            "customer_contact",
                            "customer_address",
                            "glasfaser_tarif"
                        ]
                    },
                    {
                        "type": "consent",
                        "id": "agb_consent",
                        "label": "Ich akzeptiere die AGB",
                        "required": True
                    }
                ]
            }
        }
    ],
    "logics": [
        {
            "id": "logic_show_product_on_availability",
            "trigger": {
                "field": "glasfaser_verfuegbarkeit.available",
                "operator": "equals",
                "value": True
            },
            "action": {
                "type": "show_step",
                "target": "step_04_product_selection"
            }
        },
        {
            "id": "logic_show_no_availability",
            "trigger": {
                "field": "glasfaser_verfuegbarkeit.available",
                "operator": "equals",
                "value": False
            },
            "action": {
                "type": "show_step",
                "target": "step_05_no_availability"
            }
        }
    ]
}

# Automation for No Availability → Workflow Trigger
AUTOMATION_CONFIG = {
    "flow_name": "Wülfrath Haustürverkauf - Kein Glasfaser → Ausbau-Prüfung Workflow",
    "enabled": True,
    "triggers": [
        {
            "type": "journey_submission",
            "configuration": {
                "source_id": "JOURNEY_ID_PLACEHOLDER"  # Will be replaced after journey creation
            }
        }
    ],
    "conditions": [
        {
            "id": "condition_no_availability",
            "statements": [
                {
                    "operation": "equals",
                    "source": {
                        "schema": "submission",
                        "originType": "entity",
                        "attribute": "glasfaser_verfuegbarkeit.available",
                        "origin": "journey"
                    },
                    "values": [False]
                },
                {
                    "operation": "equals",
                    "source": {
                        "schema": "submission",
                        "originType": "entity",
                        "attribute": "ausbau_interesse",
                        "origin": "journey"
                    },
                    "values": ["ja"]
                }
            ]
        }
    ],
    "actions": [
        {
            "name": "Create Contact from Journey",
            "type": "map-entity",
            "config": {
                "target_schema": "contact",
                "mapping_attributes": [
                    {
                        "source": "customer_contact.first_name",
                        "target": "first_name"
                    },
                    {
                        "source": "customer_contact.last_name",
                        "target": "last_name"
                    },
                    {
                        "source": "customer_contact.email",
                        "target": "email"
                    },
                    {
                        "source": "customer_contact.phone",
                        "target": "phone"
                    },
                    {
                        "source": "customer_address.street",
                        "target": "address_line1"
                    },
                    {
                        "source": "customer_address.postal_code",
                        "target": "postal_code"
                    },
                    {
                        "source": "customer_address.city",
                        "target": "city"
                    }
                ]
            }
        },
        {
            "name": "Create Opportunity - Glasfaser Ausbau Anfrage",
            "type": "map-entity",
            "config": {
                "target_schema": "opportunity",
                "mapping_attributes": [
                    {
                        "source": "customer_address.street",
                        "target": "_title",
                        "operation": {
                            "_template": "Glasfaser Ausbau Anfrage - {{customer_address.street}} {{customer_address.house_number}}"
                        }
                    },
                    {
                        "operation": {
                            "_set": "ausstehend"
                        },
                        "target": "status"
                    },
                    {
                        "operation": {
                            "_set": "Glasfaser Ausbau"
                        },
                        "target": "typ"
                    },
                    {
                        "source": "customer_address",
                        "target": "anschrift",
                        "operation": {
                            "_template": "{{customer_address.street}} {{customer_address.house_number}}, {{customer_address.postal_code}} {{customer_address.city}}"
                        }
                    }
                ],
                "relation_attributes": [
                    {
                        "mode": "append",
                        "source_filter": {
                            "schema": "contact"
                        },
                        "target": "contact"
                    }
                ]
            }
        },
        {
            "name": "Trigger Workflow - Ausbau Machbarkeit Prüfen",
            "type": "trigger-workflow",
            "config": {
                "target_workflow": "WORKFLOW_ID_PLACEHOLDER",  # User needs to provide workflow ID
                "conditions": [],
                "assign_steps": []
            },
            "condition_id": "condition_no_availability"
        },
        {
            "name": "Send Email - Ausbau Anfrage Bestätigung",
            "type": "send-email",
            "config": {
                "email_template_id": "EMAIL_TEMPLATE_ID_PLACEHOLDER",
                "language_code": "de",
                "to": "{{customer_contact.email}}",
                "subject": "Ihre Glasfaser Ausbau-Anfrage für Wülfrath"
            },
            "condition_id": "condition_no_availability"
        },
        {
            "name": "Send Email - Vertragsabschluss Bestätigung",
            "type": "send-email",
            "config": {
                "email_template_id": "EMAIL_TEMPLATE_ID_PLACEHOLDER",
                "language_code": "de",
                "to": "{{customer_contact.email}}",
                "subject": "Willkommen bei Stadtwerke Wülfrath - Ihr Glasfaser-Tarif"
            }
        }
    ]
}

async def create_journey(client: EpilotClient) -> str:
    """
    Erstellt die Haustürverkauf Journey.
    
    Returns:
        Journey ID
    """
    print("=" * 70)
    print("📱 ERSTELLE HAUSTÜRVERKAUF JOURNEY")
    print("=" * 70)
    print()
    print(f"Journey Name: {JOURNEY_CONFIG['name']}")
    print(f"Steps: {len(JOURNEY_CONFIG['steps'])}")
    print()
    
    # Note: This is a simplified representation
    # In practice, you would use the Journey Builder UI or a more complete API call
    print("⚠️  HINWEIS: Journey-Erstellung über API ist komplex.")
    print("   Empfohlener Weg:")
    print("   1. Journey Builder UI öffnen")
    print("   2. Neue Journey erstellen: 'Wülfrath Haustürverkauf - Glasfaser'")
    print("   3. Folgende Steps hinzufügen:")
    print()
    
    for i, step in enumerate(JOURNEY_CONFIG['steps'], 1):
        print(f"   {i}. {step['name']}")
        if 'condition' in step:
            print(f"      → Conditional Step (nur bei: {step['condition']})")
    
    print()
    print("📋 WICHTIGE KONFIGURATIONEN:")
    print()
    print("Step 2 - Verfügbarkeitsprüfung:")
    print("  • Address Block mit PLZ 42489 (Wülfrath)")
    print("  • Availability Check Block")
    print("    - API: /api/check-availability")
    print("    - Services: glasfaser, ftth, fttc")
    print("    - Variable: glasfaser_verfuegbarkeit.available (true/false)")
    print()
    print("Step 4 - Tarifauswahl:")
    print("  • Nur anzeigen wenn: glasfaser_verfuegbarkeit.available = true")
    print("  • Product Block mit Filter: category=glasfaser, tags=wuelfrath")
    print()
    print("Step 5 - Keine Verfügbarkeit:")
    print("  • Nur anzeigen wenn: glasfaser_verfuegbarkeit.available = false")
    print("  • Radio Button: ausbau_interesse (ja/nein)")
    print()
    
    # Save configuration as JSON for reference
    output_dir = Path(__file__).parent.parent.parent / "data" / "output" / "demo"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    config_file = output_dir / "hausturverkauf_journey_config.json"
    with open(config_file, 'w', encoding='utf-8') as f:
        json.dump(JOURNEY_CONFIG, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Journey-Konfiguration gespeichert: {config_file}")
    print()
    print("🔑 NÄCHSTER SCHRITT:")
    print("   Nach Journey-Erstellung die Journey-ID hier eingeben:")
    
    # Placeholder return
    journey_id = input("\n   Journey ID: ").strip()
    
    return journey_id

async def create_automation(client: EpilotClient, journey_id: str, workflow_id: str) -> dict:
    """
    Erstellt die Automation für No-Availability → Workflow Trigger.
    
    Returns:
        Automation details
    """
    print()
    print("=" * 70)
    print("⚙️  ERSTELLE AUTOMATION")
    print("=" * 70)
    print()
    
    # Update placeholder IDs
    automation = AUTOMATION_CONFIG.copy()
    automation['triggers'][0]['configuration']['source_id'] = journey_id
    
    for action in automation['actions']:
        if action['type'] == 'trigger-workflow':
            action['config']['target_workflow'] = workflow_id
    
    print(f"Automation: {automation['flow_name']}")
    print()
    print("Trigger:")
    print(f"  • Journey Submission: {journey_id}")
    print()
    print("Conditions:")
    print("  • glasfaser_verfuegbarkeit.available = false")
    print("  • ausbau_interesse = 'ja'")
    print()
    print("Actions:")
    print("  1. Create Contact")
    print("  2. Create Opportunity (Glasfaser Ausbau Anfrage)")
    print(f"  3. Trigger Workflow: {workflow_id}")
    print("  4. Send Confirmation Email")
    print()
    
    try:
        url = f"{AUTOMATION_API_BASE}/v1/automation/flow"
        result = await client.post(url, data=automation)
        
        automation_id = result.get('id')
        print(f"✅ Automation erstellt: {automation_id}")
        print()
        
        return result
        
    except Exception as e:
        print(f"❌ Fehler bei Automation-Erstellung: {e}")
        print()
        print("⚠️  Bitte Automation manuell im Automation Builder erstellen:")
        print(f"   1. Trigger: journey_submission (source_id: {journey_id})")
        print("   2. Condition: glasfaser_verfuegbarkeit.available = false AND ausbau_interesse = 'ja'")
        print("   3. Actions: Contact → Opportunity → Trigger Workflow")
        return None

async def main():
    """Hauptfunktion"""
    load_env()
    client = EpilotClient()
    
    print()
    print("╔════════════════════════════════════════════════════════════════════╗")
    print("║  WÜLFRATH HAUSVERKAUF JOURNEY - GLASFASER MIT VERFÜGBARKEITSPRÜFUNG ║")
    print("╚════════════════════════════════════════════════════════════════════╝")
    print()
    print("Diese Journey ist optimiert für:")
    print("  ✓ Tablet-Nutzung durch Außendienstmitarbeiter")
    print("  ✓ Schnelle Erfassung (6 Steps vs. 27 beim Original)")
    print("  ✓ Automatische Verfügbarkeitsprüfung")
    print("  ✓ Workflow-Trigger bei fehlender Verfügbarkeit")
    print()
    
    # Step 1: Create Journey (manual process, get ID)
    journey_id = await create_journey(client)
    
    if not journey_id:
        print("❌ Keine Journey ID angegeben. Abbruch.")
        return
    
    print()
    print("🔑 WORKFLOW KONFIGURATION:")
    print()
    print("Für die Ausbau-Prüfung benötigen Sie einen Workflow:")
    print()
    print("Workflow Name: 'Glasfaser Ausbau Machbarkeit Prüfen'")
    print("Phasen:")
    print("  1. Prüfung")
    print("     • Adresse in GIS-System prüfen")
    print("     • Entfernung zum nächsten Verteiler messen")
    print("     • Technische Machbarkeit bewerten")
    print("  2. Kostenabschätzung")
    print("     • Ausbaukosten kalkulieren")
    print("     • Fördermittel prüfen")
    print("  3. Entscheidung")
    print("     • Wirtschaftlichkeit bewerten")
    print("     • Ausbau genehmigen/ablehnen")
    print("  4. Kundeninformation")
    print("     • Kunde über Ergebnis informieren")
    print()
    
    workflow_id = input("Workflow ID: ").strip()
    
    if not workflow_id:
        print("❌ Keine Workflow ID angegeben. Automation wird nicht erstellt.")
        print("   Sie können die Automation später manuell erstellen.")
        return
    
    # Step 2: Create Automation
    automation_result = await create_automation(client, journey_id, workflow_id)
    
    print()
    print("=" * 70)
    print("✅ SETUP ABGESCHLOSSEN")
    print("=" * 70)
    print()
    print("📱 Journey URL: https://portal.stadtwerke-wuelfrath.de/glasfaser")
    print(f"   Journey ID: {journey_id}")
    print()
    if automation_result:
        print(f"⚙️  Automation ID: {automation_result.get('id')}")
    print()
    print("🔄 WORKFLOW:")
    print("   Wenn Kunde Adresse eingibt ohne Glasfaser-Verfügbarkeit")
    print("   und Interesse am Ausbau bekundet:")
    print()
    print("   1. Contact wird erstellt")
    print("   2. Opportunity 'Glasfaser Ausbau Anfrage' wird erstellt")
    print(f"   3. Workflow '{workflow_id}' startet automatisch")
    print("   4. Stadt prüft Ausbaumöglichkeit")
    print("   5. Kunde erhält Rückmeldung")
    print()
    print("📊 TEST:")
    print("   1. Journey auf Tablet öffnen")
    print("   2. Adresse ohne Glasfaser eingeben (z.B. Randgebiet Wülfrath)")
    print("   3. 'Ja, bitte informieren' auswählen")
    print("   4. In Epilot: Opportunity und Workflow prüfen")
    print()

if __name__ == "__main__":
    asyncio.run(main())
