#!/usr/bin/env python3
"""
Erstelle Demo Kunden für Stadtwerke Wülfrath

Erstellt Kundenkontakte aus JSON-Datei in Epilot.

Verwendung:
    python scripts/demo/erstelle_demo_kunden.py
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
DATA_FILE = Path(__file__).parent.parent.parent / "data" / "input" / "demo" / "wuelfrath_kunden.json"

async def create_customers_from_file(client: EpilotClient, data_file: Path) -> dict:
    """
    Erstellt Kunden aus JSON-Datei.
    
    Returns:
        Dictionary mit Kunden-Namen und IDs
    """
    print(f"👥 Lade Kundendaten aus {data_file.name}...\n")
    
    with open(data_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    kunden = data.get('kunden', [])
    print(f"✅ {len(kunden)} Kunden gefunden\n")
    
    customer_map = {}
    
    privatkunden = 0
    gewerbeckunden = 0
    
    for i, kunde in enumerate(kunden, 1):
        kunde_name = kunde.get('_title', f'Kunde {i}')
        schema = kunde.get('_schema', 'contact')
        
        try:
            url = f"{ENTITY_API_BASE}/v1/entity/{schema}"
            result = await client.post(url, data=kunde)
            customer_id = result.get('_id')
            customer_map[kunde_name] = customer_id
            
            kundentyp = kunde.get('kundentyp', 'N/A')
            adresse = kunde.get('address_line1', 'N/A')
            sparten = ", ".join(kunde.get('sparte', []))
            
            if kundentyp == "Privatkunde":
                privatkunden += 1
            elif kundentyp == "Gewerbekunde":
                gewerbeckunden += 1
            
            print(f"   [{i}/{len(kunden)}] ✅ {kunde_name}")
            print(f"             {kundentyp} - {adresse}")
            print(f"             Sparten: {sparten}")
            
            # Small delay to avoid rate limits
            await asyncio.sleep(0.5)
            
        except Exception as e:
            print(f"   [{i}/{len(kunden)}] ❌ Fehler bei {kunde_name}: {e}")
    
    print()
    print(f"📊 Zusammenfassung:")
    print(f"   Privatkunden: {privatkunden}")
    print(f"   Gewerbekunden: {gewerbeckunden}")
    
    return customer_map

async def main():
    """Hauptfunktion"""
    load_env()
    client = EpilotClient()
    
    print("=" * 70)
    print("👥 STADTWERKE WÜLFRATH - DEMO KUNDEN")
    print("=" * 70)
    print()
    
    if not DATA_FILE.exists():
        print(f"❌ Datendatei nicht gefunden: {DATA_FILE}")
        sys.exit(1)
    
    # Kunden erstellen
    customer_map = await create_customers_from_file(client, DATA_FILE)
    
    # Ergebnis speichern
    output_dir = Path(__file__).parent.parent.parent / "data" / "output" / "demo"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    output_file = output_dir / "kunden_ids.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump({
            "erstellt_am": datetime.now().isoformat(),
            "anzahl": len(customer_map),
            "kunden": customer_map
        }, f, indent=2, ensure_ascii=False)
    
    print()
    print("=" * 70)
    print(f"✅ {len(customer_map)} Kunden erfolgreich erstellt!")
    print(f"📄 Kunden-IDs gespeichert in: {output_file}")
    print("=" * 70)

if __name__ == "__main__":
    asyncio.run(main())
