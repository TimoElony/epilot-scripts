#!/usr/bin/env python3
"""
Update Ausbau Glasfaser Workflow via API

Creates a comprehensive workflow structure for fiber optic expansion based on the requirements:
- Service provider scheduling
- Product availability scheduling
- Real-time construction documentation via mobile journeys
- Admin approval for process continuation

Usage:
    python scripts/workflows/update_ausbau_glasfaser_workflow.py
"""

import sys
import asyncio
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, Any

# Add lib to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from lib.auth import load_env
from lib.api_client import EpilotClient

WORKFLOW_API_BASE = "https://workflows-definition.sls.epilot.io"
WORKFLOW_ID = "wfQpwhJF6J"

def create_comprehensive_workflow_structure() -> Dict[str, Any]:
    """
    Create a comprehensive workflow structure for Glasfaser Ausbau.
    
    Pain points addressed:
    - Dienstleister Terminierung (Service Provider Scheduling)
    - Produktverfügbarkeit Terminierung (Product Availability Scheduling)
    - Mobile Journeys für Echtzeitdokumentation (Real-time Documentation)
    - Prozess-Freigabe durch Sachbearbeiter (Admin Approval)
    """
    
    return {
        "name": "Ausbau Glasfaser",
        "description": """Der grobe Prozess des Glasfaserausbaus ohne viele Details, mit Fokus auf Schmerzpunkte der Stadtwerke, vor allem:
-Terminierung der Dienstleister
-Terminierung der Produktverfügbarkeit
-Mobile Journeys sollen Echtzeitdokumentation des Baufortschrittes ermoeglichen
-Sachbearbeiter der Stadtwerke will Ueberblick ueber Prozessschritte behalten und ohne viel Aufwand die Freigabe fuer Fortsetzung des Prozesses geben""",
        "enabled": True,
        "enableECPWorkflow": False,
        "assignedTo": [],
        "closingReasons": [],
        "updateEntityAttributes": [],
        "flow": [
            # Phase 1: Planung und Vorbereitung
            {
                "id": "phase-planning",
                "name": "Phase 1: Planung und Vorbereitung",
                "type": "SECTION",
                "order": 1,
                "steps": [
                    {
                        "id": "step-initial-assessment",
                        "name": "Erstbewertung und Standortanalyse",
                        "type": "STEP",
                        "order": 2,
                        "assignedTo": [],
                        "userIds": [],
                        "ecp": {"enabled": False},
                        "installer": {"enabled": False}
                    },
                    {
                        "id": "step-technical-planning",
                        "name": "Technische Planung erstellen",
                        "type": "STEP",
                        "order": 3,
                        "assignedTo": [],
                        "userIds": [],
                        "ecp": {"enabled": False},
                        "installer": {"enabled": False}
                    },
                    {
                        "id": "step-cost-estimation",
                        "name": "Kostenvoranschlag und Budget",
                        "type": "STEP",
                        "order": 4,
                        "assignedTo": [],
                        "userIds": [],
                        "ecp": {"enabled": False},
                        "installer": {"enabled": False}
                    },
                    {
                        "id": "step-approval-planning",
                        "name": "🔒 FREIGABE: Planung genehmigen",
                        "type": "STEP",
                        "order": 5,
                        "assignedTo": [],
                        "userIds": [],
                        "ecp": {"enabled": False},
                        "installer": {"enabled": False}
                    }
                ]
            },
            
            # Phase 2: Dienstleister Management (Pain Point!)
            {
                "id": "phase-service-provider",
                "name": "Phase 2: Dienstleister Management",
                "type": "SECTION",
                "order": 6,
                "steps": [
                    {
                        "id": "step-provider-selection",
                        "name": "⚠️ Dienstleister auswählen",
                        "type": "STEP",
                        "order": 7,
                        "assignedTo": [],
                        "userIds": [],
                        "ecp": {"enabled": False},
                        "installer": {"enabled": False}
                    },
                    {
                        "id": "step-provider-scheduling",
                        "name": "⚠️ Termine mit Dienstleister koordinieren",
                        "type": "STEP",
                        "order": 8,
                        "assignedTo": [],
                        "userIds": [],
                        "ecp": {"enabled": False},
                        "installer": {"enabled": False}
                    },
                    {
                        "id": "step-contract-dienstleister",
                        "name": "Verträge abschließen",
                        "type": "STEP",
                        "order": 9,
                        "assignedTo": [],
                        "userIds": [],
                        "ecp": {"enabled": False},
                        "installer": {"enabled": False}
                    },
                    {
                        "id": "step-approval-dienstleister",
                        "name": "🔒 FREIGABE: Dienstleister bestätigt",
                        "type": "STEP",
                        "order": 10,
                        "assignedTo": [],
                        "userIds": [],
                        "ecp": {"enabled": False},
                        "installer": {"enabled": False}
                    }
                ]
            },
            
            # Phase 3: Produktverfügbarkeit (Pain Point!)
            {
                "id": "phase-product-availability",
                "name": "Phase 3: Produktverfügbarkeit sicherstellen",
                "type": "SECTION",
                "order": 11,
                "steps": [
                    {
                        "id": "step-material-ordering",
                        "name": "Material und Komponenten bestellen",
                        "type": "STEP",
                        "order": 12,
                        "assignedTo": [],
                        "userIds": [],
                        "ecp": {"enabled": False},
                        "installer": {"enabled": False}
                    },
                    {
                        "id": "step-delivery-scheduling",
                        "name": "⚠️ Liefertermine koordinieren",
                        "type": "STEP",
                        "order": 13,
                        "assignedTo": [],
                        "userIds": [],
                        "ecp": {"enabled": False},
                        "installer": {"enabled": False}
                    },
                    {
                        "id": "step-availability-confirmation",
                        "name": "⚠️ Produktverfügbarkeit bestätigen",
                        "type": "STEP",
                        "order": 14,
                        "assignedTo": [],
                        "userIds": [],
                        "ecp": {"enabled": False},
                        "installer": {"enabled": False}
                    },
                    {
                        "id": "step-approval-products",
                        "name": "🔒 FREIGABE: Produkte verfügbar",
                        "type": "STEP",
                        "order": 15,
                        "assignedTo": [],
                        "userIds": [],
                        "ecp": {"enabled": False},
                        "installer": {"enabled": False}
                    }
                ]
            },
            
            # Phase 4: Bauausführung mit Mobile Journeys (Pain Point!)
            {
                "id": "phase-construction",
                "name": "Phase 4: Bauausführung",
                "type": "SECTION",
                "order": 16,
                "steps": [
                    {
                        "id": "step-construction-start",
                        "name": "Baubeginn dokumentieren",
                        "type": "STEP",
                        "order": 17,
                        "assignedTo": [],
                        "userIds": [],
                        "ecp": {"enabled": False},
                        "installer": {"enabled": True}  # Mobile Journey enabled!
                    },
                    {
                        "id": "step-trench-installation",
                        "name": "📱 Tiefbauarbeiten (Mobile Journey)",
                        "type": "STEP",
                        "order": 18,
                        "assignedTo": [],
                        "userIds": [],
                        "ecp": {"enabled": False},
                        "installer": {"enabled": True}  # Real-time documentation!
                    },
                    {
                        "id": "step-cable-laying",
                        "name": "📱 Kabelverlegung (Mobile Journey)",
                        "type": "STEP",
                        "order": 19,
                        "assignedTo": [],
                        "userIds": [],
                        "ecp": {"enabled": False},
                        "installer": {"enabled": True}  # Real-time documentation!
                    },
                    {
                        "id": "step-connection-installation",
                        "name": "📱 Anschluss Installation (Mobile Journey)",
                        "type": "STEP",
                        "order": 20,
                        "assignedTo": [],
                        "userIds": [],
                        "ecp": {"enabled": False},
                        "installer": {"enabled": True}  # Real-time documentation!
                    },
                    {
                        "id": "step-approval-construction",
                        "name": "🔒 FREIGABE: Bauarbeiten abgeschlossen",
                        "type": "STEP",
                        "order": 21,
                        "assignedTo": [],
                        "userIds": [],
                        "ecp": {"enabled": False},
                        "installer": {"enabled": False}
                    }
                ]
            },
            
            # Phase 5: Abnahme und Inbetriebnahme
            {
                "id": "phase-commissioning",
                "name": "Phase 5: Abnahme und Inbetriebnahme",
                "type": "SECTION",
                "order": 22,
                "steps": [
                    {
                        "id": "step-testing",
                        "name": "Technische Tests durchführen",
                        "type": "STEP",
                        "order": 23,
                        "assignedTo": [],
                        "userIds": [],
                        "ecp": {"enabled": False},
                        "installer": {"enabled": False}
                    },
                    {
                        "id": "step-official-acceptance",
                        "name": "Offizielle Abnahme",
                        "type": "STEP",
                        "order": 24,
                        "assignedTo": [],
                        "userIds": [],
                        "ecp": {"enabled": False},
                        "installer": {"enabled": False}
                    },
                    {
                        "id": "step-product-activation",
                        "name": "⚠️ Produkte aktivieren / Verfügbarkeit schalten",
                        "type": "STEP",
                        "order": 25,
                        "assignedTo": [],
                        "userIds": [],
                        "ecp": {"enabled": False},
                        "installer": {"enabled": False}
                    },
                    {
                        "id": "step-customer-notification",
                        "name": "Kunden benachrichtigen (Verfügbarkeit)",
                        "type": "STEP",
                        "order": 26,
                        "assignedTo": [],
                        "userIds": [],
                        "ecp": {"enabled": False},
                        "installer": {"enabled": False}
                    },
                    {
                        "id": "step-final-approval",
                        "name": "🔒 FREIGABE: Projekt abschließen",
                        "type": "STEP",
                        "order": 27,
                        "assignedTo": [],
                        "userIds": [],
                        "ecp": {"enabled": False},
                        "installer": {"enabled": False}
                    }
                ]
            }
        ]
    }

async def update_workflow(client: EpilotClient):
    """Update the Ausbau Glasfaser workflow via API."""
    
    print("=" * 70)
    print("🔧 UPDATE AUSBAU GLASFASER WORKFLOW")
    print("=" * 70)
    print()
    print(f"Workflow ID: {WORKFLOW_ID}")
    print()
    
    # Get current workflow
    print("📥 Fetching current workflow...")
    url_get = f"{WORKFLOW_API_BASE}/v1/workflows/definitions/{WORKFLOW_ID}"
    current = await client.get(url_get)
    
    # Create backup
    backup_file = Path(f"scripts/workflows/output/workflow_ausbau_{WORKFLOW_ID}_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
    backup_file.parent.mkdir(parents=True, exist_ok=True)
    with open(backup_file, 'w') as f:
        json.dump(current, f, indent=2)
    print(f"✅ Backup saved: {backup_file}")
    print()
    
    # Create new structure
    print("🔨 Creating new workflow structure...")
    new_workflow = create_comprehensive_workflow_structure()
    
    print(f"   Phases: {len([s for s in new_workflow['flow'] if s['type'] == 'SECTION'])}")
    print(f"   Steps: {sum(len(s.get('steps', [])) for s in new_workflow['flow'] if s['type'] == 'SECTION')}")
    print()
    
    # Update via API
    print("📤 Updating workflow via API...")
    url_update = f"{WORKFLOW_API_BASE}/v1/workflows/definitions/{WORKFLOW_ID}"
    
    try:
        result = await client.put(url_update, data=new_workflow)
        print("✅ Workflow updated successfully!")
        print()
        print(f"   Name: {result.get('name')}")
        print(f"   ID: {result.get('id')}")
        print(f"   Enabled: {result.get('enabled')}")
        print()
        
        # Save updated version
        output_file = Path(f"scripts/workflows/output/workflow_ausbau_{WORKFLOW_ID}_updated.json")
        output_file.parent.mkdir(parents=True, exist_ok=True)
        with open(output_file, 'w') as f:
            json.dump(result, f, indent=2)
        print(f"💾 Updated workflow saved: {output_file}")
        
        return result
        
    except Exception as e:
        print(f"❌ Error updating workflow: {e}")
        print()
        print("Workflow structure prepared but not updated.")
        print(f"Manual update may be needed in UI: https://portal.epilot.cloud/app/workflows/{WORKFLOW_ID}")
        return None

async def main():
    """Main function."""
    load_env()
    client = EpilotClient()
    
    try:
        result = await update_workflow(client)
        
        if result:
            print()
            print("=" * 70)
            print("✅ SUCCESS!")
            print("=" * 70)
            print()
            print("Next steps:")
            print("1. Check workflow in UI: https://portal.epilot.cloud/app/workflows/")
            print("2. Configure user assignments for approval steps")
            print("3. Test mobile journey steps with installer app")
            print("4. Create automations for notifications")
            print()
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())
