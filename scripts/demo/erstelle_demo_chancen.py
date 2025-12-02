#!/usr/bin/env python3
"""
Erstelle Demo Chancen für Stadtwerke Wülfrath

Erstellt Opportunities (Chancen) aus JSON-Datei in Epilot.

Verwendung:
    python scripts/demo/erstelle_demo_chancen.py
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
DATA_FILE = Path(__file__).parent.parent.parent / "data" / "input" / "demo" / "wuelfrath_chancen.json"
KUNDEN_FILE = Path(__file__).parent.parent.parent / "data" / "output" / "demo" / "kunden_ids.json"

async def create_opportunities_from_file(client: EpilotClient, data_file: Path, kunden_ids: dict) -> dict:
    """
    Erstellt Opportunities aus JSON-Datei.
    
    Returns:
        Dictionary mit Chancen-Titeln und IDs
    """
    print(f"💼 Lade Chancen-Daten aus {data_file.name}...\n")
    
    with open(data_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    chancen = data.get('chancen', [])
    print(f"✅ {len(chancen)} Chancen gefunden\n")
    
    opportunity_map = {}
    
    status_count = {}
    
    for i, chance in enumerate(chancen, 1):
        titel = chance.get('titel', f'Chance {i}')
        kunde_name = chance.get('kunde_name')
        
        # Finde Kunden-ID
        kunde_id = kunden_ids.get(kunde_name)
        
        if not kunde_id:
            print(f"   [{i}/{len(chancen)}] ⚠️  Kunde '{kunde_name}' nicht gefunden, überspringe")
            continue
        
        # Baue Opportunity Entity
        opportunity_data = {
            "_schema": "opportunity",
            "_title": titel,
            "status": chance.get('status', 'neu'),
            "contact": [{"$relation": [{"entity_id": kunde_id}]}],
            "anschrift": chance.get('anschrift'),
            "typ": chance.get('typ'),
            "sparten": chance.get('sparten', []),
            "wunschtermin": chance.get('wunschtermin'),
            "beschreibung": chance.get('beschreibung'),
            "_tags": ["demo", "wuelfrath"] + chance.get('sparten', [])
        }
        
        if 'abschlussdatum' in chance:
            opportunity_data['abschlussdatum'] = chance['abschlussdatum']
        
        try:
            url = f"{ENTITY_API_BASE}/v1/entity/opportunity"
            result = await client.post(url, data=opportunity_data)
            opportunity_id = result.get('_id')
            opportunity_map[titel] = opportunity_id
            
            status = chance.get('status', 'neu')
            typ = chance.get('typ', 'N/A')
            status_count[status] = status_count.get(status, 0) + 1
            
            print(f"   [{i}/{len(chancen)}] ✅ {titel}")
            print(f"             Status: {status}, Typ: {typ}")
            print(f"             Kunde: {kunde_name}")
            
            # Small delay to avoid rate limits
            await asyncio.sleep(0.5)
            
        except Exception as e:
            print(f"   [{i}/{len(chancen)}] ❌ Fehler bei {titel}: {e}")
    
    print()
    print(f"📊 Status-Verteilung:")
    for status, count in status_count.items():
        print(f"   {status}: {count}")
    
    return opportunity_map

async def main():
    """Hauptfunktion"""
    load_env()
    client = EpilotClient()
    
    print("=" * 70)
    print("💼 STADTWERKE WÜLFRATH - DEMO CHANCEN")
    print("=" * 70)
    print()
    
    if not DATA_FILE.exists():
        print(f"❌ Datendatei nicht gefunden: {DATA_FILE}")
        sys.exit(1)
    
    if not KUNDEN_FILE.exists():
        print(f"❌ Kunden-IDs nicht gefunden: {KUNDEN_FILE}")
        print("   Bitte zuerst 'erstelle_demo_kunden.py' ausführen!")
        sys.exit(1)
    
    # Lade Kunden-IDs
    with open(KUNDEN_FILE, 'r', encoding='utf-8') as f:
        kunden_data = json.load(f)
        kunden_ids = kunden_data.get('kunden', {})
    
    print(f"📋 {len(kunden_ids)} Kunden-IDs geladen\n")
    
    # Chancen erstellen
    opportunity_map = await create_opportunities_from_file(client, DATA_FILE, kunden_ids)
    
    # Ergebnis speichern
    output_dir = Path(__file__).parent.parent.parent / "data" / "output" / "demo"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    output_file = output_dir / "chancen_ids.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump({
            "erstellt_am": datetime.now().isoformat(),
            "anzahl": len(opportunity_map),
            "chancen": opportunity_map
        }, f, indent=2, ensure_ascii=False)
    
    print()
    print("=" * 70)
    print(f"✅ {len(opportunity_map)} Chancen erfolgreich erstellt!")
    print(f"📄 Chancen-IDs gespeichert in: {output_file}")
    print("=" * 70)

if __name__ == "__main__":
    asyncio.run(main())
