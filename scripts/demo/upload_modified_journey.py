#!/usr/bin/env python3
"""
Upload Modified Journey Configuration

Da die Journey API schreibgeschützt zu sein scheint, bietet dieses Script eine
alternative Lösung: Es erstellt eine JSON-Datei die manuell im UI importiert werden kann.

Verwendung:
    python scripts/demo/upload_modified_journey.py
"""

import sys
import json
from pathlib import Path

# Add lib to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

def create_simplified_journey():
    """
    Erstelle eine vereinfachte Journey-Konfiguration basierend auf dem Backup.
    """
    backup_file = Path("data/output/demo/journey_backup_879e1f89-426b-4dde-8e0a-8955f459220b.json")
    
    if not backup_file.exists():
        print(f"❌ Backup-Datei nicht gefunden: {backup_file}")
        return None
    
    print(f"📥 Lade Backup: {backup_file}")
    with open(backup_file, 'r', encoding='utf-8') as f:
        journey = json.load(f)
    
    print(f"✓ Geladen: {journey.get('name')} ({len(journey.get('steps', []))} Steps)")
    
    # Identifiziere die wichtigsten Steps
    steps = journey.get('steps', [])
    
    # Suche nach den wichtigsten Step-Typen
    essential_steps = []
    step_keywords = {
        'address': ['plz', 'adresse', 'address', 'postcode'],
        'product': ['produkt', 'product', 'tarif', 'auswahl'],
        'contact': ['kontakt', 'contact', 'persönlich', 'personal'],
        'summary': ['zusammenfassung', 'summary', 'bestätigung', 'confirm']
    }
    
    for category, keywords in step_keywords.items():
        for step in steps:
            step_name = step.get('name', '').lower()
            if any(kw in step_name for kw in keywords):
                if step not in essential_steps:
                    essential_steps.append(step)
                    break
    
    # Falls nicht alle gefunden, nimm die ersten relevanten
    if len(essential_steps) < 4:
        print("⚠️  Nicht alle passenden Steps gefunden, füge weitere hinzu...")
        for step in steps[:6]:
            if step not in essential_steps:
                essential_steps.append(step)
            if len(essential_steps) >= 6:
                break
    
    # Erstelle modifizierte Journey
    modified = journey.copy()
    modified['name'] = 'Wülfrath Haustürverkauf - Glasfaser'
    modified['steps'] = essential_steps[:6]  # Maximal 6 Steps
    
    # Benenne Steps um
    if len(modified['steps']) > 0:
        modified['steps'][0]['name'] = 'Adresse & Verfügbarkeit'
    if len(modified['steps']) > 1:
        modified['steps'][1]['name'] = 'Tarifauswahl'
    if len(modified['steps']) > 2 and 'kontakt' in modified['steps'][2]['name'].lower():
        modified['steps'][2]['name'] = 'Kontaktdaten'
    if len(modified['steps']) >= 4:
        modified['steps'][-1]['name'] = 'Zusammenfassung'
    
    # Bereinige Logics - behalte nur die für vorhandene Steps
    step_ids = {step.get('id') for step in modified['steps']}
    original_logics = modified.get('logics', [])
    filtered_logics = []
    
    for logic in original_logics:
        # Prüfe ob Logic sich auf vorhandene Steps bezieht
        target_id = logic.get('target')
        if target_id in step_ids:
            filtered_logics.append(logic)
    
    modified['logics'] = filtered_logics
    
    print(f"\n✓ Modifizierte Journey erstellt:")
    print(f"  Name: {modified['name']}")
    print(f"  Steps: {len(modified['steps'])}")
    for i, step in enumerate(modified['steps'], 1):
        print(f"    {i}. {step.get('name')}")
    print(f"  Logics: {len(modified['logics'])}")
    
    return modified

def save_for_manual_import(journey_config):
    """
    Speichere die Journey-Konfiguration in einem Format,
    das manuell importiert werden kann.
    """
    output_dir = Path("data/output/demo")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    output_file = output_dir / "hausturverkauf_journey_simplified.json"
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(journey_config, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 Gespeichert: {output_file}")
    return output_file

def print_manual_instructions(output_file):
    """
    Drucke Anweisungen für manuellen Import/Update.
    """
    print("\n" + "=" * 70)
    print("📋 MANUELLE ANWEISUNGEN")
    print("=" * 70)
    print()
    print("Da die Journey API keinen direkten Update erlaubt, gibt es 2 Optionen:")
    print()
    print("OPTION 1: Manuell in der UI bearbeiten")
    print("-" * 70)
    print("1. Öffne deine Journey im Browser:")
    print("   https://portal.epilot.cloud/app/journeys/879e1f89-426b-4dde-8e0a-8955f459220b")
    print()
    print("2. Ändere den Namen zu: 'Wülfrath Haustürverkauf - Glasfaser'")
    print()
    print("3. Lösche überflüssige Steps, behalte nur:")
    print("   - Adresse & Verfügbarkeit (aus PLZ-Step)")
    print("   - Tarifauswahl (aus Produktauswahl)")
    print("   - Kontaktdaten (aus Kontakt-Step)")
    print("   - Zusammenfassung (aus Final-Step)")
    print()
    print("4. Füge Verfügbarkeitsprüfung hinzu im ersten Step:")
    print("   - Block Type: 'Availability Check'")
    print("   - Variable: glasfaser_verfuegbarkeit.available")
    print()
    print("5. Erstelle einen zusätzlichen Step für 'Keine Verfügbarkeit':")
    print("   - Anzeigen wenn: glasfaser_verfuegbarkeit.available = false")
    print("   - Interessenabfrage: Radio-Button 'Informieren bei Ausbau?'")
    print()
    print("OPTION 2: Neue Journey aus Template erstellen")
    print("-" * 70)
    print("1. Erstelle eine neue Journey im UI")
    print("2. Verwende die gespeicherte Konfiguration als Referenz:")
    print(f"   {output_file}")
    print("3. Kopiere die Step-Struktur manuell")
    print()
    print("=" * 70)
    print()
    print("📚 Vollständige Anleitung: data/output/demo/HAUSTURVERKAUF_JOURNEY_GUIDE.md")
    print()

def main():
    """
    Hauptfunktion
    """
    print("=" * 70)
    print("🔧 ERSTELLE VEREINFACHTE JOURNEY-KONFIGURATION")
    print("=" * 70)
    print()
    
    # Erstelle vereinfachte Journey
    modified_journey = create_simplified_journey()
    
    if not modified_journey:
        sys.exit(1)
    
    # Speichere für manuellen Import
    output_file = save_for_manual_import(modified_journey)
    
    # Drucke Anweisungen
    print_manual_instructions(output_file)
    
    print("✅ Fertig!")

if __name__ == "__main__":
    main()
