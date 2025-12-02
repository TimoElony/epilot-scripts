# Stadtwerke Wülfrath - Demo Umgebung

Dieses Verzeichnis enthält alle Skripte und Daten zur Erstellung einer realistischen Demo-Umgebung für **Stadtwerke Wülfrath**.

## Überblick

Die Demo simuliert ein kleines Stadtwerk mit ~21.000 Einwohnern in Wülfrath (NRW), das folgende Sparten anbietet:
- ⚡ Strom (Elektrizität)
- 🔥 Gas (Erdgas)
- 💧 Wasser (Trinkwasser & Abwasser)
- 🌐 Glasfaser (Internet)

## Demo-Daten

### Produkte (10)
- **Anschlüsse** (5): Strom Privat/Gewerbe, Gas, Wasser, Glasfaser
- **Tarife** (5): Stromtarife, Gastarif, Wassertarif, Glasfaser-Internet

### Kunden (20)
- **Privatkunden** (15): Verschiedene Haushalte in Wülfrath
- **Gewerbekunden** (5): Bäckerei, Autowerkstatt, Restaurant, Apotheke, Wohnbaugesellschaft

### Chancen/Opportunities (8)
- Status: neu, in_bearbeitung, genehmigt, abgeschlossen
- Typen: Neuanschluss, Service-Ergänzung, Tarifänderung

### Aufträge/Orders (5)
- Verschiedene Status und Produktkombinationen
- Verknüpft mit Kunden und Chancen

## Verwendung

### Komplette Demo-Umgebung erstellen

```bash
# Einfachste Methode - erstellt alles in korrekter Reihenfolge
python scripts/demo/erstelle_demo_umgebung.py
```

### Einzelne Komponenten erstellen

```bash
# 1. Produkte (keine Abhängigkeiten)
python scripts/demo/erstelle_demo_produkte.py

# 2. Kunden (keine Abhängigkeiten)
python scripts/demo/erstelle_demo_kunden.py

# 3. Chancen (benötigt Kunden-IDs)
python scripts/demo/erstelle_demo_chancen.py

# 4. Aufträge (benötigt Kunden-, Chancen- und Produkt-IDs)
python scripts/demo/erstelle_demo_auftraege.py
```

## Datenstruktur

```
data/
├── input/demo/                    # Quelldaten (JSON)
│   ├── wuelfrath_produkte.json   # 10 Produkte
│   ├── wuelfrath_kunden.json     # 20 Kunden
│   ├── wuelfrath_chancen.json    # 8 Chancen
│   └── wuelfrath_auftraege.json  # 5 Aufträge
│
└── output/demo/                   # Erstellte Entity-IDs
    ├── produkt_ids.json          # Mapping: Name → Entity-ID
    ├── kunden_ids.json           # Mapping: Name → Entity-ID
    ├── chancen_ids.json          # Mapping: Titel → Entity-ID
    └── auftrag_ids.json          # Mapping: Titel → Entity-ID
```

## Preise (2025 Deutschland)

### Anschlussgebühren
- Strom Privat: €450
- Strom Gewerbe: €750
- Gas: €650
- Wasser: €550
- Glasfaser: €200

### Tarife (monatlich)
- **Strom Privat**: €0,32/kWh + €12,90 Grundgebühr
- **Strom Gewerbe**: €0,28/kWh + €45,00 Grundgebühr
- **Gas**: €0,12/kWh + €18,50 Grundgebühr
- **Wasser**: €3,20/m³ + €30,00 Grundgebühr
- **Glasfaser 500**: €59,90 Flatrate

## Adressen

Alle Kunden befinden sich in **42489 Wülfrath** mit realistischen Straßennamen:
- Wilhelmstraße
- Düsseler Straße
- Berghauser Straße
- Lindenstraße
- Ratinger Straße
- Hochdahler Straße
- Mettmanner Straße
- Nordstraße, Südstraße
- Kirchstraße, Parkstraße
- Hauptstraße, Gartenstraße, Waldstraße

## Integration mit bestehenden Journeys

Die Demo-Daten sind kompatibel mit den vorhandenen Epilot Journeys:
- **Hausanschluss Glasfaser** - Für Glasfaser-Anschlussanfragen
- **Hausanschluss Angebotsannahme** - Für Angebots-Bestätigungen
- **Tarifabschluss** - Für Tarifwechsel und neue Verträge
- **Installateur-Journeys** - Für Fachkräfte-Verwaltung

## Entity-Beziehungen

```
Kunde (Contact)
  ↓
Chance (Opportunity) → verknüpft mit Kunde
  ↓
Auftrag (Order) → verknüpft mit Kunde + Chance + Produkte
```

## Beispiel-Szenarien

### 1. Neukunde mit Komplettanschluss
**Kunde**: Michael Schmidt  
**Adresse**: Wilhelmstraße 23  
**Chance**: Hausanschluss Neubau  
**Produkte**: Strom + Gas + Wasser  
**Status**: Genehmigt → Auftrag bestätigt

### 2. Glasfaser-Upgrade
**Kunde**: Anna Müller  
**Adresse**: Düsseler Straße 45  
**Chance**: Glasfaseranschluss für Homeoffice  
**Status**: Neu → In Bearbeitung

### 3. Gewerblicher Großkunde
**Kunde**: Wohnbau Wülfrath eG  
**Adresse**: Nordstraße 88 (24 Wohneinheiten)  
**Chance**: Mehrfamilienhaus Komplett  
**Status**: Abgeschlossen mit Rechnung

## Technische Details

### API-Endpoints
- **Entity API**: `https://entity.sls.epilot.io/v1/entities`
- **Search API**: `https://entity.sls.epilot.io/v1/entity:search`

### Rate Limiting
Die Skripte enthalten automatische Verzögerungen (0,5 Sekunden zwischen Requests), um API-Rate-Limits zu respektieren.

### Fehlerbehandlung
- Skripte validieren Abhängigkeiten (z.B. Kunden-IDs vor Chancen-Erstellung)
- Fehlgeschlagene Entity-Erstellungen werden protokolliert
- Exit-Codes zeigen Erfolg/Fehler an

## Cleanup

Um die Demo-Umgebung zurückzusetzen, müssen die erstellten Entities in Epilot manuell gelöscht werden. Die Entity-IDs sind in `data/output/demo/*.json` gespeichert.

**Hinweis**: Ein Cleanup-Script könnte in Zukunft hinzugefügt werden.

## Nächste Schritte

Nach Erstellung der Demo-Umgebung:

1. **Epilot UI öffnen** und die erstellten Entities überprüfen
2. **Journey testen**: Hausanschluss-Formular ausfüllen
3. **Automation beobachten**: Journey-Submission → Entity-Erstellung
4. **Workflow starten**: Chance in Workflow überführen
5. **Demo präsentieren**: Kunde → Chance → Auftrag Workflow zeigen

## Lizenz & Hinweise

- Demo-Daten sind fiktiv, aber realistisch
- Preise basieren auf 2025 deutschen Marktdaten
- Wülfrath ist eine echte Stadt in NRW
- Straßennamen sind realistisch, Hausnummern fiktiv
- Personen und Firmen sind erfunden

---

**Erstellt für Epilot MVP Demo - Dezember 2025**
