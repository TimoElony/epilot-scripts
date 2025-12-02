#!/usr/bin/env python3
"""
Erstelle Komplette Demo-Umgebung für Stadtwerke Wülfrath

Orchestriert die Erstellung aller Demo-Entities in der richtigen Reihenfolge.

Verwendung:
    python scripts/demo/erstelle_demo_umgebung.py
"""

import sys
import asyncio
import subprocess
from pathlib import Path
from datetime import datetime

# Add lib to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

SCRIPTS_DIR = Path(__file__).parent

def run_script(script_name: str) -> bool:
    """
    Führt ein Python-Script aus und gibt True bei Erfolg zurück.
    """
    script_path = SCRIPTS_DIR / script_name
    
    if not script_path.exists():
        print(f"❌ Script nicht gefunden: {script_name}")
        return False
    
    print(f"\n{'='*70}")
    print(f"▶️  Führe aus: {script_name}")
    print(f"{'='*70}\n")
    
    try:
        result = subprocess.run(
            [sys.executable, str(script_path)],
            check=True,
            capture_output=False
        )
        return result.returncode == 0
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Fehler beim Ausführen von {script_name}")
        print(f"   Exit Code: {e.returncode}")
        return False
    except Exception as e:
        print(f"\n❌ Unerwarteter Fehler: {e}")
        return False

def main():
    """Hauptfunktion"""
    start_time = datetime.now()
    
    print("=" * 70)
    print("🏭 STADTWERKE WÜLFRATH - KOMPLETTE DEMO-UMGEBUNG")
    print("=" * 70)
    print()
    print("Diese Script erstellt alle Demo-Entities in der richtigen Reihenfolge:")
    print("  1. Produkte (keine Abhängigkeiten)")
    print("  2. Kunden (keine Abhängigkeiten)")
    print("  3. Chancen (hängen von Kunden ab)")
    print("  4. Aufträge (hängen von Kunden, Chancen, Produkten ab)")
    print()
    print(f"⏰ Start: {start_time.strftime('%H:%M:%S')}")
    print("=" * 70)
    
    success = True
    
    # Schritt 1: Produkte
    if not run_script("erstelle_demo_produkte.py"):
        print("\n❌ Fehler beim Erstellen der Produkte!")
        success = False
    
    # Schritt 2: Kunden
    if success and not run_script("erstelle_demo_kunden.py"):
        print("\n❌ Fehler beim Erstellen der Kunden!")
        success = False
    
    # Schritt 3: Chancen
    if success and not run_script("erstelle_demo_chancen.py"):
        print("\n❌ Fehler beim Erstellen der Chancen!")
        success = False
    
    # Schritt 4: Aufträge
    if success and not run_script("erstelle_demo_auftraege.py"):
        print("\n❌ Fehler beim Erstellen der Aufträge!")
        success = False
    
    # Zusammenfassung
    end_time = datetime.now()
    duration = (end_time - start_time).total_seconds()
    
    print("\n")
    print("=" * 70)
    if success:
        print("✅ DEMO-UMGEBUNG ERFOLGREICH ERSTELLT!")
    else:
        print("❌ DEMO-UMGEBUNG KONNTE NICHT VOLLSTÄNDIG ERSTELLT WERDEN")
    print("=" * 70)
    print(f"⏱️  Dauer: {duration:.1f} Sekunden")
    print(f"🏁 Ende: {end_time.strftime('%H:%M:%S')}")
    print()
    print("📊 Erstellte Entities:")
    print("   - 10 Produkte (Anschlüsse & Tarife)")
    print("   - 20 Kunden (15 Privat, 5 Gewerbe)")
    print("   - 8 Chancen (verschiedene Status)")
    print("   - 5 Aufträge (mit Verknüpfungen)")
    print()
    print("📁 Entity-IDs gespeichert in: data/output/demo/")
    print("=" * 70)
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
