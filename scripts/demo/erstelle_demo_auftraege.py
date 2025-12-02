#!/usr/bin/env python3
"""
Erstelle Demo Aufträge für Stadtwerke Wülfrath

Erstellt Orders (Aufträge) aus JSON-Datei in Epilot.

Verwendung:
    python scripts/demo/erstelle_demo_auftraege.py
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
DATA_FILE = Path(__file__).parent.parent.parent / "data" / "input" / "demo" / "wuelfrath_auftraege.json"
KUNDEN_FILE = Path(__file__).parent.parent.parent / "data" / "output" / "demo" / "kunden_ids.json"
CHANCEN_FILE = Path(__file__).parent.parent.parent / "data" / "output" / "demo" / "chancen_ids.json"
PRODUKT_FILE = Path(__file__).parent.parent.parent / "data" / "output" / "demo" / "produkt_ids.json"

async def create_orders_from_file(
    client: EpilotClient, 
    data_file: Path, 
    kunden_ids: dict,
    chancen_ids: dict,
    produkt_ids: dict
) -> dict:
    """
    Erstellt Orders aus JSON-Datei.
    
    Returns:
        Dictionary mit Auftrags-Titeln und IDs
    """
    print(f"🛒 Lade Auftrags-Daten aus {data_file.name}...\n")
    
    with open(data_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    auftraege = data.get('auftraege', [])
    print(f"✅ {len(auftraege)} Aufträge gefunden\n")
    
    order_map = {}
    
    status_count = {}
    
    for i, auftrag in enumerate(auftraege, 1):
        titel = auftrag.get('titel', f'Auftrag {i}')
        kunde_name = auftrag.get('kunde_name')
        
        # Finde Kunden-ID
        kunde_id = kunden_ids.get(kunde_name)
        
        if not kunde_id:
            print(f"   [{i}/{len(auftraege)}] ⚠️  Kunde '{kunde_name}' nicht gefunden, überspringe")
            continue
        
        # Baue Order Entity
        order_data = {
            "_schema": "order",
            "_title": titel,
            "status": auftrag.get('status', 'offen'),
            "customer": [{"$relation": [{"entity_id": kunde_id}]}],
            "amount_total": auftrag.get('gesamtbetrag', 0.0),
            "currency": "EUR",
            "order_date": auftrag.get('auftragsdatum'),
            "_tags": ["demo", "wuelfrath"]
        }
        
        # Verknüpfe mit Chance falls vorhanden
        chancen_titel = auftrag.get('chancen_titel')
        if chancen_titel and chancen_titel in chancen_ids:
            chance_id = chancen_ids[chancen_titel]
            order_data["opportunity"] = [{"$relation": [{"entity_id": chance_id}]}]
        
        # Füge Produktinformationen hinzu (als Text, da line_items komplex sein können)
        produkte_info = []
        for produkt in auftrag.get('produkte', []):
            produkt_name = produkt.get('produkt_name')
            menge = produkt.get('menge', 1)
            produkte_info.append(f"{menge}x {produkt_name}")
        
        if produkte_info:
            order_data["produkte_beschreibung"] = ", ".join(produkte_info)
        
        if 'rechnungsdatum' in auftrag:
            order_data['rechnungsdatum'] = auftrag['rechnungsdatum']
        
        if 'bemerkung' in auftrag:
            order_data['bemerkung'] = auftrag['bemerkung']
        
        try:
            url = f"{ENTITY_API_BASE}/v1/entity/order"
            result = await client.post(url, data=order_data)
            order_id = result.get('_id')
            order_map[titel] = order_id
            
            status = auftrag.get('status', 'offen')
            betrag = auftrag.get('gesamtbetrag', 0.0)
            status_count[status] = status_count.get(status, 0) + 1
            
            print(f"   [{i}/{len(auftraege)}] ✅ {titel}")
            print(f"             Status: {status}, Betrag: €{betrag:.2f}")
            print(f"             Kunde: {kunde_name}")
            
            # Small delay to avoid rate limits
            await asyncio.sleep(0.5)
            
        except Exception as e:
            print(f"   [{i}/{len(auftraege)}] ❌ Fehler bei {titel}: {e}")
    
    print()
    print(f"📊 Status-Verteilung:")
    for status, count in status_count.items():
        print(f"   {status}: {count}")
    
    return order_map

async def main():
    """Hauptfunktion"""
    load_env()
    client = EpilotClient()
    
    print("=" * 70)
    print("🛒 STADTWERKE WÜLFRATH - DEMO AUFTRÄGE")
    print("=" * 70)
    print()
    
    if not DATA_FILE.exists():
        print(f"❌ Datendatei nicht gefunden: {DATA_FILE}")
        sys.exit(1)
    
    if not KUNDEN_FILE.exists():
        print(f"❌ Kunden-IDs nicht gefunden: {KUNDEN_FILE}")
        print("   Bitte zuerst 'erstelle_demo_kunden.py' ausführen!")
        sys.exit(1)
    
    # Lade IDs
    with open(KUNDEN_FILE, 'r', encoding='utf-8') as f:
        kunden_data = json.load(f)
        kunden_ids = kunden_data.get('kunden', {})
    
    chancen_ids = {}
    if CHANCEN_FILE.exists():
        with open(CHANCEN_FILE, 'r', encoding='utf-8') as f:
            chancen_data = json.load(f)
            chancen_ids = chancen_data.get('chancen', {})
    
    produkt_ids = {}
    if PRODUKT_FILE.exists():
        with open(PRODUKT_FILE, 'r', encoding='utf-8') as f:
            produkt_data = json.load(f)
            produkt_ids = produkt_data.get('produkte', {})
    
    print(f"📋 {len(kunden_ids)} Kunden-IDs geladen")
    print(f"📋 {len(chancen_ids)} Chancen-IDs geladen")
    print(f"📋 {len(produkt_ids)} Produkt-IDs geladen\n")
    
    # Aufträge erstellen
    order_map = await create_orders_from_file(
        client, DATA_FILE, kunden_ids, chancen_ids, produkt_ids
    )
    
    # Ergebnis speichern
    output_dir = Path(__file__).parent.parent.parent / "data" / "output" / "demo"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    output_file = output_dir / "auftrag_ids.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump({
            "erstellt_am": datetime.now().isoformat(),
            "anzahl": len(order_map),
            "auftraege": order_map
        }, f, indent=2, ensure_ascii=False)
    
    print()
    print("=" * 70)
    print(f"✅ {len(order_map)} Aufträge erfolgreich erstellt!")
    print(f"📄 Auftrags-IDs gespeichert in: {output_file}")
    print("=" * 70)

if __name__ == "__main__":
    asyncio.run(main())
