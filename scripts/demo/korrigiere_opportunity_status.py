#!/usr/bin/env python3
"""
Korrigiere Opportunity Status-Werte in Epilot

Aktualisiert bestehende Opportunities mit den offiziellen Epilot-Status-Werten:
- neu → ausstehend
- in_bearbeitung → bearbeitung
- genehmigt → bearbeitung (oder abgeschlossen, je nach Kontext)
- abgelehnt → abgebrochen

Verwendung:
    python scripts/demo/korrigiere_opportunity_status.py
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

ENTITY_API_BASE = "https://entity.sls.epilot.io"
CHANCEN_IDS_FILE = Path(__file__).parent.parent.parent / "data" / "output" / "demo" / "chancen_ids.json"
CHANCEN_DATA_FILE = Path(__file__).parent.parent.parent / "data" / "input" / "demo" / "wuelfrath_chancen.json"

# Status mapping from old (incorrect) to new (official)
STATUS_MAPPING = {
    "neu": "ausstehend",
    "in_bearbeitung": "bearbeitung",
    "genehmigt": "bearbeitung",  # These were approved, so in progress
    "abgelehnt": "abgebrochen",
    "abgeschlossen": "geschlossen"  # Fix: geschlossen not abgeschlossen
}

async def update_opportunity_status(client: EpilotClient, opp_id: str, title: str, new_status: str) -> bool:
    """
    Aktualisiert den Status einer Opportunity.
    
    Returns:
        True wenn erfolgreich, False bei Fehler
    """
    try:
        # Hole aktuelle Opportunity
        url = f"{ENTITY_API_BASE}/v1/entity/opportunity/{opp_id}"
        current_opp = await client.get(url)
        
        old_status = current_opp.get('status', 'unbekannt')
        
        # Nur aktualisieren wenn Status sich ändert
        if old_status == new_status:
            print(f"   ⏭️  {title}")
            print(f"        Status bereits korrekt: {new_status}")
            return True
        
        # Update status
        current_opp['status'] = new_status
        
        # Sende Update
        await client.put(url, data=current_opp)
        
        print(f"   ✅ {title}")
        print(f"        {old_status} → {new_status}")
        return True
        
    except Exception as e:
        print(f"   ❌ {title}")
        print(f"        Fehler: {e}")
        return False

async def main():
    """Hauptfunktion"""
    load_env()
    client = EpilotClient()
    
    print("=" * 70)
    print("🔧 KORREKTUR: OPPORTUNITY STATUS-WERTE")
    print("=" * 70)
    print()
    print("Offizielle Epilot Status-Werte:")
    print("  • ausstehend (Pending)")
    print("  • bearbeitung (In Progress)")
    print("  • geschlossen (Closed/Completed)")
    print("  • abgebrochen (Canceled)")
    print()
    print("Quelle: https://help.epilot.cloud/de_DE/kundenbetreuung/")
    print("        6449990323730-Status-in-Opportunities-und-Bestellungen")
    print()
    print("=" * 70)
    print()
    
    if not CHANCEN_IDS_FILE.exists():
        print(f"❌ Chancen-IDs nicht gefunden: {CHANCEN_IDS_FILE}")
        sys.exit(1)
    
    if not CHANCEN_DATA_FILE.exists():
        print(f"❌ Chancen-Daten nicht gefunden: {CHANCEN_DATA_FILE}")
        sys.exit(1)
    
    # Lade Opportunity IDs
    with open(CHANCEN_IDS_FILE, 'r', encoding='utf-8') as f:
        ids_data = json.load(f)
    
    opp_ids = ids_data.get('chancen', {})
    print(f"📋 {len(opp_ids)} Opportunities gefunden\n")
    
    # Lade korrekte Status-Werte aus JSON
    with open(CHANCEN_DATA_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Erstelle Mapping: Titel → korrekter Status
    correct_statuses = {}
    for chance in data.get('chancen', []):
        titel = chance.get('titel')
        status = chance.get('status')
        if titel and status:
            correct_statuses[titel] = status
    
    # Update jede Opportunity
    success_count = 0
    update_count = 0
    skip_count = 0
    
    for i, (title, opp_id) in enumerate(opp_ids.items(), 1):
        print(f"[{i}/{len(opp_ids)}]")
        
        # Finde korrekten Status
        correct_status = correct_statuses.get(title)
        
        if not correct_status:
            print(f"   ⚠️  {title}")
            print(f"        Kein Status in Datendatei gefunden, überspringe")
            skip_count += 1
            continue
        
        # Update Opportunity
        result = await update_opportunity_status(client, opp_id, title, correct_status)
        
        if result:
            success_count += 1
            # Check if status was actually changed (not just verified)
            url = f"{ENTITY_API_BASE}/v1/entity/opportunity/{opp_id}"
            current_opp = await client.get(url)
            if current_opp.get('status') == correct_status:
                update_count += 1
        
        # Small delay
        await asyncio.sleep(0.3)
        print()
    
    print("=" * 70)
    print("📊 ZUSAMMENFASSUNG")
    print("=" * 70)
    print(f"✅ Erfolgreich verarbeitet: {success_count}/{len(opp_ids)}")
    print(f"🔄 Status aktualisiert: {update_count}")
    print(f"⏭️  Bereits korrekt: {success_count - update_count}")
    print(f"⏭️  Übersprungen: {skip_count}")
    print()
    
    if success_count == len(opp_ids):
        print("🎉 Alle Opportunities wurden erfolgreich aktualisiert!")
        print()
        print("Die Opportunities verwenden jetzt die offiziellen Epilot-Status:")
        print("  • ausstehend")
        print("  • bearbeitung")
        print("  • geschlossen")
        print("  • abgebrochen")
    else:
        print(f"⚠️  {len(opp_ids) - success_count} Opportunities konnten nicht aktualisiert werden")
    
    print()

if __name__ == "__main__":
    asyncio.run(main())
