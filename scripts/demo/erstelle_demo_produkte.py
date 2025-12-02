#!/usr/bin/env python3
"""
Erstelle Demo Produkte für Stadtwerke Wülfrath

Erstellt Produktkatalog aus JSON-Datei in Epilot.

Verwendung:
    python scripts/demo/erstelle_demo_produkte.py
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
DATA_FILE = Path(__file__).parent.parent.parent / "data" / "input" / "demo" / "wuelfrath_produkte.json"

async def create_products_from_file(client: EpilotClient, data_file: Path) -> dict:
    """
    Erstellt Produkte aus JSON-Datei.
    
    Returns:
        Dictionary mit Produkt-Namen und IDs
    """
    print(f"📦 Lade Produktdaten aus {data_file.name}...\n")
    
    with open(data_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    produkte = data.get('produkte', [])
    print(f"✅ {len(produkte)} Produkte gefunden\n")
    
    product_map = {}
    
    for i, produkt in enumerate(produkte, 1):
        produkt_name = produkt.get('_title', f'Produkt {i}')
        schema = produkt.get('_schema', 'product')
        
        try:
            url = f"{ENTITY_API_BASE}/v1/entity/{schema}"
            result = await client.post(url, data=produkt)
            product_id = result.get('_id')
            product_map[produkt_name] = product_id
            
            kategorie = produkt.get('kategorie', 'N/A')
            sparte = produkt.get('sparte', 'N/A')
            preis = produkt.get('preis', produkt.get('arbeitspreis', 'N/A'))
            
            print(f"   [{i}/{len(produkte)}] ✅ {produkt_name}")
            print(f"             Kategorie: {kategorie}, Sparte: {sparte}, Preis: {preis}")
            
            # Small delay to avoid rate limits
            await asyncio.sleep(0.5)
            
        except Exception as e:
            print(f"   [{i}/{len(produkte)}] ❌ Fehler bei {produkt_name}: {e}")
    
    return product_map

async def main():
    """Hauptfunktion"""
    load_env()
    client = EpilotClient()
    
    print("=" * 70)
    print("🏭 STADTWERKE WÜLFRATH - DEMO PRODUKTE")
    print("=" * 70)
    print()
    
    if not DATA_FILE.exists():
        print(f"❌ Datendatei nicht gefunden: {DATA_FILE}")
        sys.exit(1)
    
    # Produkte erstellen
    product_map = await create_products_from_file(client, DATA_FILE)
    
    # Ergebnis speichern
    output_dir = Path(__file__).parent.parent.parent / "data" / "output" / "demo"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    output_file = output_dir / "produkt_ids.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump({
            "erstellt_am": datetime.now().isoformat(),
            "anzahl": len(product_map),
            "produkte": product_map
        }, f, indent=2, ensure_ascii=False)
    
    print()
    print("=" * 70)
    print(f"✅ {len(product_map)} Produkte erfolgreich erstellt!")
    print(f"📄 Produkt-IDs gespeichert in: {output_file}")
    print("=" * 70)

if __name__ == "__main__":
    asyncio.run(main())
