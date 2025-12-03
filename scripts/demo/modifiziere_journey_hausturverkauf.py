#!/usr/bin/env python3
"""
Modifiziere bestehende Journey für Haustürverkauf

Nimmt eine Kopie der Tarifabschluss Journey und vereinfacht sie für Tablet-Nutzung
mit Verfügbarkeitsprüfung und Workflow-Trigger bei fehlender Verfügbarkeit.

Verwendung:
    python scripts/demo/modifiziere_journey_hausturverkauf.py
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
JOURNEY_ID = "879e1f89-426b-4dde-8e0a-8955f459220b"

async def get_journey(client: EpilotClient, journey_id: str) -> dict:
    """Hole aktuelle Journey-Konfiguration"""
    url = f"{JOURNEY_API_BASE}/v1/journey/configuration/{journey_id}"
    return await client.get(url)

async def update_journey(client: EpilotClient, journey_id: str, journey_config: dict) -> dict:
    """Update Journey-Konfiguration"""
    url = f"{JOURNEY_API_BASE}/v1/journey/configuration/{journey_id}"
    return await client.put(url, data=journey_config)

async def main():
    """Hauptfunktion"""
    load_env()
    client = EpilotClient()
    
    print("=" * 70)
    print("🔧 MODIFIZIERE JOURNEY FÜR HAUSVERKAUF")
    print("=" * 70)
    print()
    print(f"Journey ID: {JOURNEY_ID}")
    print()
    
    # 1. Hole aktuelle Journey
    print("📥 Lade aktuelle Journey-Konfiguration...")
    try:
        current_journey = await get_journey(client, JOURNEY_ID)
        print(f"✅ Journey geladen: {current_journey.get('name')}")
        print(f"   Aktuelle Steps: {len(current_journey.get('steps', []))}")
        print()
    except Exception as e:
        print(f"❌ Fehler beim Laden: {e}")
        return
    
    # Speichere Original als Backup
    output_dir = Path(__file__).parent.parent.parent / "data" / "output" / "demo"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    backup_file = output_dir / f"journey_backup_{JOURNEY_ID}.json"
    with open(backup_file, 'w', encoding='utf-8') as f:
        json.dump(current_journey, f, indent=2, ensure_ascii=False)
    print(f"💾 Backup gespeichert: {backup_file}")
    print()
    
    # 2. Modifiziere Journey
    print("✏️  Modifiziere Journey...")
    print()
    
    # Update basic info
    current_journey['name'] = "Wülfrath Haustürverkauf - Glasfaser"
    
    # Vereinfache Steps - behalte nur die wichtigsten
    original_steps = current_journey.get('steps', [])
    print(f"   Original hatte {len(original_steps)} Steps")
    
    # Finde relevante Steps aus Original
    simplified_steps = []
    
    # Durchsuche Steps nach relevanten Inhalten
    for step in original_steps:
        step_name = step.get('name', '').lower()
        
        # PLZ/Adresse Step
        if 'plz' in step_name or 'adresse' in step_name:
            step['name'] = "Adresse & Verfügbarkeit"
            simplified_steps.append(step)
            print(f"   ✓ Behalte Step: {step['name']}")
            break
    
    # Produktauswahl Step
    for step in original_steps:
        step_name = step.get('name', '').lower()
        if 'produkt' in step_name:
            step['name'] = "Tarifauswahl"
            simplified_steps.append(step)
            print(f"   ✓ Behalte Step: {step['name']}")
            break
    
    # Kontaktdaten Step
    for step in original_steps:
        schema = step.get('schema', {})
        blocks = schema.get('blocks', [])
        for block in blocks:
            if block.get('type') == 'contact':
                step['name'] = "Kontaktdaten"
                simplified_steps.append(step)
                print(f"   ✓ Behalte Step: {step['name']}")
                break
        if step.get('name') == "Kontaktdaten":
            break
    
    # Zusammenfassung/Bestätigung Step
    for step in reversed(original_steps):
        step_name = step.get('name', '').lower()
        if 'zusammenfassung' in step_name or 'bestätigung' in step_name or 'abschluss' in step_name:
            step['name'] = "Zusammenfassung"
            simplified_steps.append(step)
            print(f"   ✓ Behalte Step: {step['name']}")
            break
    
    # Falls nicht genug Steps gefunden, nehme ersten 6
    if len(simplified_steps) < 4:
        print("   ⚠️  Nicht genug passende Steps gefunden, nehme erste 6 Steps")
        simplified_steps = original_steps[:6]
    
    # Update Steps
    current_journey['steps'] = simplified_steps
    
    print()
    print(f"   Neue Steps: {len(simplified_steps)}")
    for i, step in enumerate(simplified_steps, 1):
        print(f"   {i}. {step.get('name')}")
    
    print()
    
    # Entferne komplexe Logics die nicht mehr passen
    if 'logics' in current_journey:
        original_logics = len(current_journey['logics'])
        # Behalte nur Logics die sich auf verbliebene Steps beziehen
        step_ids = [s.get('id') for s in simplified_steps]
        current_journey['logics'] = [
            logic for logic in current_journey['logics']
            if logic.get('target') in step_ids or not logic.get('target')
        ]
        print(f"   Logics reduziert: {original_logics} → {len(current_journey['logics'])}")
        print()
    
    # 3. Update Journey via API
    print("📤 Update Journey in Epilot...")
    try:
        updated_journey = await update_journey(client, JOURNEY_ID, current_journey)
        print(f"✅ Journey erfolgreich aktualisiert!")
        print()
    except Exception as e:
        print(f"❌ Fehler beim Update: {e}")
        print()
        print("💡 Tipp: Journey kann eventuell nur über UI vollständig bearbeitet werden")
        print("   Versuche folgende Änderungen manuell:")
        print(f"   1. Öffne Journey in Epilot: https://portal.epilot.cloud/app/journeys/{JOURNEY_ID}")
        print("   2. Lösche überflüssige Steps (reduziere auf 4-6)")
        print("   3. Benenne Steps um wie oben gezeigt")
        print()
        return
    
    # Speichere modifizierte Version
    modified_file = output_dir / f"journey_modified_{JOURNEY_ID}.json"
    with open(modified_file, 'w', encoding='utf-8') as f:
        json.dump(current_journey, f, indent=2, ensure_ascii=False)
    print(f"💾 Modifizierte Version gespeichert: {modified_file}")
    print()
    
    # 4. Zusammenfassung
    print("=" * 70)
    print("✅ JOURNEY VEREINFACHT")
    print("=" * 70)
    print()
    print(f"Journey Name: {current_journey['name']}")
    print(f"Journey ID: {JOURNEY_ID}")
    print(f"Steps: {len(original_steps)} → {len(simplified_steps)}")
    print()
    print("📱 Journey URL:")
    print(f"   https://portal.epilot.cloud/app/journeys/{JOURNEY_ID}")
    print()
    print("🔧 NÄCHSTE SCHRITTE:")
    print()
    print("1. Journey in Epilot UI öffnen und testen")
    print("2. Verfügbarkeitsprüfung in Step 1 hinzufügen:")
    print("   • API Endpoint konfigurieren")
    print("   • Variable: glasfaser_verfuegbarkeit.available")
    print()
    print("3. Conditional Steps hinzufügen:")
    print("   • Step für 'Keine Verfügbarkeit' mit Interesse-Abfrage")
    print("   • Logic: Zeige nur wenn verfuegbarkeit = false")
    print()
    print("4. Automation erstellen für Workflow-Trigger:")
    print("   • Trigger: journey_submission")
    print(f"   • source_id: {JOURNEY_ID}")
    print("   • Condition: glasfaser_verfuegbarkeit.available = false")
    print("   • Action: trigger-workflow")
    print()

if __name__ == "__main__":
    asyncio.run(main())
