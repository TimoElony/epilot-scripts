#!/usr/bin/env python3
"""
Modifiziere Journey in Blueprint für Haustürverkauf

Liest den Blueprint aus data/Tarifabschluss_org_20000382_blueprint_2025-12-03T13_33_45.874Z,
vereinfacht die Journey und speichert eine neue Version die hochgeladen werden kann.

Verwendung:
    python scripts/demo/modifiziere_blueprint_journey.py
"""

import sys
import json
import re
from pathlib import Path
from datetime import datetime

def load_simplified_journey():
    """Lade die bereits erstellte vereinfachte Journey-Konfiguration."""
    journey_file = Path("data/output/demo/hausturverkauf_journey_simplified.json")
    
    if not journey_file.exists():
        print(f"❌ Vereinfachte Journey nicht gefunden: {journey_file}")
        print("   Bitte erst upload_modified_journey.py ausführen.")
        return None
    
    with open(journey_file, 'r', encoding='utf-8') as f:
        return json.load(f)

def modify_journey_tf(blueprint_dir: Path, simplified_journey: dict):
    """
    Modifiziere die journey.tf Datei im Blueprint.
    
    Strategie:
    1. Lade journey.tf
    2. Extrahiere die wichtigsten Step-Definitionen aus der vereinfachten Journey
    3. Ersetze steps und logics im Terraform-Code
    4. Ändere den Namen
    5. Speichere modifizierte Version
    """
    journey_tf = blueprint_dir / "journey.tf"
    
    if not journey_tf.exists():
        print(f"❌ journey.tf nicht gefunden in {blueprint_dir}")
        return None
    
    print(f"📥 Lade Blueprint Journey: {journey_tf}")
    with open(journey_tf, 'r', encoding='utf-8') as f:
        tf_content = f.read()
    
    # 1. Ändere den Namen
    print("✏️  Ändere Journey-Namen...")
    tf_content = re.sub(
        r'name\s*=\s*"Tarifabschluss"',
        'name     = "Wülfrath Haustürverkauf - Glasfaser"',
        tf_content
    )
    
    # 2. Vereinfache Steps - extrahiere nur die ersten N Steps aus dem JSON
    print("✏️  Vereinfache Steps...")
    steps_to_keep = simplified_journey.get('steps', [])[:4]  # Nur 4 Haupt-Steps
    
    # Konvertiere Steps zu Terraform-Format (jsonencode)
    steps_json = json.dumps(steps_to_keep, indent=2, ensure_ascii=False)
    
    # Finde und ersetze steps = jsonencode([...])
    # Dies ist komplex wegen verschachtelter Klammern, daher nehmen wir einen anderen Ansatz:
    # Wir ersetzen nur die Anzahl und Namen der Steps, behalten aber die Struktur
    
    # Alternativ: Erstelle eine reduzierte Version mit Platzhaltern
    step_names = [step.get('name', f'Step {i}') for i, step in enumerate(steps_to_keep, 1)]
    
    print(f"   Neue Steps ({len(step_names)}):")
    for i, name in enumerate(step_names, 1):
        print(f"     {i}. {name}")
    
    # 3. Vereinfache Logics - extrahiere aus simplified_journey
    print("✏️  Vereinfache Logics...")
    logics_to_keep = simplified_journey.get('logics', [])[:3]  # Max 3 Logics
    
    # Konvertiere Logics zu Terraform-Format
    logics_json = json.dumps(logics_to_keep, indent=2, ensure_ascii=False)
    
    print(f"   Neue Logics: {len(logics_to_keep)}")
    
    # Da die vollständige Ersetzung von Steps komplex ist (3000+ Zeilen),
    # erstellen wir eine NEUE vereinfachte journey.tf mit nur den essentiellen Steps
    
    return create_simplified_journey_tf(simplified_journey, tf_content)

def create_simplified_journey_tf(simplified_journey: dict, original_tf: str):
    """
    Erstelle eine neue, vereinfachte journey.tf basierend auf der Struktur.
    
    Wir extrahieren nur die wichtigsten Teile und erstellen eine minimal funktionale Version.
    """
    # Extrahiere die Resource-Definition und Metadaten aus dem Original
    resource_match = re.search(
        r'resource "epilot-journey_journey" "journey_[^"]*" \{(.*?)\n  brand_id',
        original_tf,
        re.DOTALL
    )
    
    lifecycle_block = ""
    if resource_match:
        lifecycle_block = resource_match.group(1).strip()
    
    # Erstelle vereinfachte Steps
    steps = simplified_journey.get('steps', [])[:4]
    logics = simplified_journey.get('logics', [])[:3]
    
    # Konvertiere zu Terraform JSON-Format
    steps_json = json.dumps(steps, ensure_ascii=False)
    logics_json = json.dumps(logics, ensure_ascii=False)
    
    # Erstelle den neuen Terraform-Code
    simplified_tf = f'''# __generated__ by Terraform
# Modified for Wülfrath Haustürverkauf - Simplified Journey

# __generated__ by Terraform from "879e1f89-426b-4dde-8e0a-8955f459220b"
resource "epilot-journey_journey" "journey_879e1f89426b4dde8e0a8955f459220b" {{
  lifecycle {{
    ignore_changes  = [manifest]
    prevent_destroy = true
  }}
  brand_id = null
  context_schema = []
  
  journey_type = null
  logics = jsonencode({logics_json})
  manifest = distinct([var.manifest_id])
  name     = "{simplified_journey.get('name', 'Wülfrath Haustürverkauf - Glasfaser')}"
  rules = []
  
  settings = {{
    access_mode                  = null
    address_suggestions_file_id  = null
    address_suggestions_file_url = null
    description                  = "Vereinfachte Journey für Haustürverkauf mit Verfügbarkeitsprüfung"
    
    embed_options = {{
      button = {{
        align = "left"
        text  = "Inhalt anzeigen"
      }}
      lang          = "de"
      mode          = "inline"
      scroll_to_top = true
      top_bar       = true
      width         = "100%"
    }}
    enable_dark_mode = null
    
    entity_tags   = ["copy", "hausturverkauf"]
    file_purposes = []
    
    runtime_entities     = ["OPPORTUNITY", "ORDER"]
    safe_mode_automation = false
    targeted_customer    = null
    template_id          = "bb790890-09b7-11ed-842b-1f60da7f4bb3"
    third_party_cookies  = null
    use_new_design       = null
  }}
  
  steps = jsonencode({steps_json})
}}
'''
    
    return simplified_tf

def save_modified_blueprint(blueprint_dir: Path, modified_journey_tf: str):
    """Speichere den modifizierten Blueprint in einem neuen Verzeichnis."""
    
    # Erstelle neues Verzeichnis
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    new_dir_name = f"Hausturverkauf_Blueprint_{timestamp}"
    new_dir = blueprint_dir.parent / new_dir_name
    new_dir.mkdir(exist_ok=True)
    
    print(f"\n📁 Erstelle neues Blueprint-Verzeichnis: {new_dir.name}")
    
    # Kopiere alle Dateien außer journey.tf
    import shutil
    
    for file in blueprint_dir.iterdir():
        if file.name != 'journey.tf' and not file.name.endswith(':Zone.Identifier'):
            shutil.copy2(file, new_dir / file.name)
            print(f"   ✓ Kopiert: {file.name}")
    
    # Speichere die modifizierte journey.tf
    new_journey_tf = new_dir / "journey.tf"
    with open(new_journey_tf, 'w', encoding='utf-8') as f:
        f.write(modified_journey_tf)
    
    print(f"   ✓ Erstellt: journey.tf (modifiziert)")
    
    # Erstelle README mit Anweisungen
    readme_content = f"""# Wülfrath Haustürverkauf Blueprint

Dieser Blueprint wurde automatisch aus dem Tarifabschluss-Blueprint erstellt
und für den Haustürverkauf vereinfacht.

## Änderungen

- Journey-Name: "Wülfrath Haustürverkauf - Glasfaser"
- Steps reduziert: 27 → 4 Haupt-Steps
  1. Adresse & Verfügbarkeit
  2. Tarifauswahl
  3. Persönliche Informationen
  4. Zusammenfassung
- Logics vereinfacht
- Entity Tags: ["copy", "hausturverkauf"]

## Upload zu Epilot

### Option 1: Über UI (Blueprint Manager)
1. Öffne Epilot Portal: https://portal.epilot.cloud
2. Gehe zu Blueprints / Templates
3. Wähle "Upload Blueprint" oder "Import from Files"
4. Lade alle .tf Dateien aus diesem Verzeichnis hoch
5. Deploy den Blueprint

### Option 2: Über Terraform CLI
```bash
cd {new_dir}
terraform init
terraform plan
terraform apply
```

## Nächste Schritte nach Upload

1. **Verfügbarkeitsprüfung konfigurieren**
   - Im ersten Step "Adresse & Verfügbarkeit"
   - Block Type: Availability Check
   - Variable: glasfaser_verfuegbarkeit.available

2. **Automation erstellen** für Workflow-Trigger
   - Trigger: journey_submission
   - Source: Diese Journey
   - Conditions: available=false AND interesse=ja
   - Actions: create-contact, create-opportunity, trigger-workflow

3. **Workflow erstellen**: "Glasfaser Ausbau Machbarkeit Prüfen"
   - Phase 1: Technical Assessment
   - Phase 2: Cost Estimation
   - Phase 3: Decision
   - Phase 4: Customer Communication

## Dokumentation

Siehe: data/output/demo/HAUSTURVERKAUF_JOURNEY_GUIDE.md

Erstellt: {timestamp}
"""
    
    readme_file = new_dir / "README.md"
    with open(readme_file, 'w', encoding='utf-8') as f:
        f.write(readme_content)
    
    print(f"   ✓ Erstellt: README.md")
    
    return new_dir

def main():
    """Hauptfunktion"""
    print("=" * 70)
    print("🔧 MODIFIZIERE BLUEPRINT JOURNEY FÜR HAUSVERKAUF")
    print("=" * 70)
    print()
    
    # 1. Lade vereinfachte Journey
    print("📥 Lade vereinfachte Journey-Konfiguration...")
    simplified_journey = load_simplified_journey()
    
    if not simplified_journey:
        sys.exit(1)
    
    print(f"✓ Geladen: {simplified_journey.get('name')}")
    print(f"  Steps: {len(simplified_journey.get('steps', []))}")
    print(f"  Logics: {len(simplified_journey.get('logics', []))}")
    print()
    
    # 2. Finde Blueprint-Verzeichnis
    blueprint_dir = Path("data/Tarifabschluss_org_20000382_blueprint_2025-12-03T13_33_45.874Z")
    
    if not blueprint_dir.exists():
        print(f"❌ Blueprint-Verzeichnis nicht gefunden: {blueprint_dir}")
        sys.exit(1)
    
    # 3. Modifiziere journey.tf
    print("🔨 Modifiziere Blueprint...")
    modified_journey_tf = modify_journey_tf(blueprint_dir, simplified_journey)
    
    if not modified_journey_tf:
        print("❌ Fehler bei der Modifikation")
        sys.exit(1)
    
    # 4. Speichere modifizierten Blueprint
    new_blueprint_dir = save_modified_blueprint(blueprint_dir, modified_journey_tf)
    
    print()
    print("=" * 70)
    print("✅ ERFOLGREICH!")
    print("=" * 70)
    print()
    print(f"📦 Neuer Blueprint gespeichert in:")
    print(f"   {new_blueprint_dir}")
    print()
    print("🚀 NÄCHSTE SCHRITTE:")
    print()
    print("1. Blueprint hochladen:")
    print("   - Öffne Epilot Portal: https://portal.epilot.cloud")
    print("   - Gehe zu Blueprints")
    print("   - Upload alle .tf Dateien aus dem neuen Verzeichnis")
    print()
    print("2. Nach Upload in Epilot UI:")
    print("   - Verfügbarkeitsprüfung im ersten Step hinzufügen")
    print("   - Automation für Workflow-Trigger konfigurieren")
    print("   - Workflow erstellen (siehe Guide)")
    print()
    print(f"📚 Siehe README.md im Blueprint-Verzeichnis für Details")
    print()

if __name__ == "__main__":
    main()
