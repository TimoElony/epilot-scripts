# Epilot Workflows & Blueprints Analysis

**Export Date:** December 2, 2025  
**Data Location:** `data/output/workflows/` and `data/output/blueprints/`

---

## Summary

Your Epilot instance contains:
- **14 Workflows** (individual process definitions)
- **3 Blueprints** (packages containing 171-281 resources each, including workflows)

---

## 1. Workflows (Process Definitions)

### Overview
Workflows define the step-by-step processes for handling different business operations. They are stored in the Workflow Definition API.

### Your Workflows

| ID | Name | Description |
|----|------|-------------|
| wf42gHFCtx | Hausanschluss | House connection process |
| wf7t3jus0X | Service - Umzug/Auszug | Service requests (relocation/move-out) |
| wfDRa_TFj_ | Ausbauplanung | Expansion planning based on data |
| wfIOMqb8qB | Installateur - Gasteintragung | Installer concession check (guest) |
| **wfQULHNKGs** | **Blueprintprozess Hausanschluss** | **Blueprint-based house connection** |
| wfSSGjuImO | Installateur - Neueintragung | Installer registry new entry |
| wfXoqDCR72 | Installateur - Meldung Fachkraft | Installer specialist notification |
| wfZAnZluiK | Vertriebsplanung Outbound | Sales planning outbound |
| wfcm8xIxo2 | Vertriebskampagne Outbound | Sales campaign outbound |
| wfhqY-Pp4k | Hausanschluss | House connection (variant) |
| wfkuVWpfdA | Opportunity Glasfasertarif | Fiber optic opportunity |
| wfmT830B3d | Installateur - Ausweisverlängerung (Gast) | Installer ID renewal (guest) |
| wfwHt1tb8M | Hausanschluss | House connection (variant) |
| wfza8aq9-Z | Installateur - Ausweisverlängerung (Stamm) | Installer ID renewal (permanent) |

### Workflow Structure

```json
{
  "id": "wfQULHNKGs",
  "name": "Blueprintprozess Hausanschluss",
  "enabled": true,
  "enableECPWorkflow": true,  // Customer portal integration
  "flow": [
    {
      "id": "6enxgmWQ",
      "name": "Anfrage",  // Section name
      "type": "SECTION",
      "order": 1,
      "steps": [
        {
          "id": "G7clx_HD",
          "name": "Zuständigkeit prüfen",  // Step name
          "type": "STEP",
          "order": 2,
          "description": { "value": "..." },
          "assignedTo": [],
          "userIds": [],
          "ecp": {  // Customer portal settings
            "enabled": true,
            "label": "Prüfung der Anfrage",
            "description": "..."
          }
        }
      ]
    }
  ],
  "updateEntityAttributes": [...]  // Auto-update rules
}
```

### Key Components

**1. Sections (Stages)**
- High-level phases of the workflow (e.g., "Anfrage", "Angebotserstellung")
- Contain multiple steps
- Define the major milestones

**2. Steps (Tasks)**
- Individual tasks within sections
- Can be manual or automated
- Types:
  - `STEP`: Manual task requiring user action
  - `AUTOMATION`: Triggers automation flow

**3. Step Properties**
- **name**: Display name of the step
- **description**: Instructions for users
- **assignedTo**: Users/groups responsible
- **order**: Sequence within section
- **requirements**: Conditions to complete step
- **ecp**: Customer portal visibility settings
- **installer**: Installer portal settings
- **automationConfig**: Links to automation flows

**4. Automation Integration**
```json
{
  "executionType": "AUTOMATION",
  "automationConfig": {
    "flowId": "50db4e7e-5ffa-46d1-b6c6-2b38f52e5326"
  }
}
```

**5. Entity Updates**
```json
{
  "updateEntityAttributes": [
    {
      "source": "current_section",
      "target": {
        "entitySchema": "opportunity",
        "entityAttribute": "status"
      }
    }
  ]
}
```
Automatically updates entity fields as workflow progresses.

---

## 2. Blueprints (Resource Packages)

### Overview
Blueprints are packages that bundle multiple resources together for deployment. They act as containers that can include workflows, forms, products, templates, automations, and other resources. Workflows can be exported as part of blueprints, making blueprints the top-level packaging mechanism for complete business solutions.

### Your Blueprints

| Blueprint | Resources | Version | Description |
|-----------|-----------|---------|-------------|
| **Hausanschluss Kombi** | 281 | v2.0.0 | House connection combo (electricity, gas, water, district heating, fiber) |
| **Loomia** | 217 | v1.0.0 | Complete solution (possibly partner-specific) |
| **Konzessionsmanagement** | 171 | v2.0.0 | Concession management for installers |

### Blueprint Structure

```json
{
  "id": "49bedae9-43c9-4fb5-b67e-dd6a2285a374",
  "title": "Hausanschluss Kombi",
  "version": "v2.0.0",
  "source_type": "internal",
  "is_verified": true,
  "installation_status": "installed",
  "resources": [
    {
      "id": "617ec950-...",
      "type": "journey",
      "name": "Hausanschluss Kombi (Anfrage)",
      "address": "epilot-journey_journey.journey_...",
      "parent_resource_ids": [...],
      "impact_on_install": ["create"],
      "is_root": false,
      "hard_dependencies": []
    }
  ]
}
```

### Resource Types in Blueprints

The blueprints contain these resource types:

#### Core Process Components
- **`workflow_definition`**: The workflow processes themselves
- **`automation_flow`**: Automated actions and triggers
- **`journey`**: Customer-facing forms/portals

#### Data & Configuration
- **`schema_attribute`**: Custom fields for entities
- **`schema_group`**: Groups of fields
- **`schema_group_headline`**: Section headers
- **`entity_mapping`**: Data transformation rules
- **`custom_variable`**: Reusable variables

#### Business Logic
- **`product`**: Products/services offered
- **`price`**: Pricing configurations
- **`tax`**: Tax rules
- **`closing_reason`**: Workflow closure reasons

#### Templates & Content
- **`emailtemplate`**: Email templates
- **`file`**: Documents, images, PDFs
- **`taxonomy_classification`**: Categories/tags

#### Access & Visualization
- **`role`**: User roles and permissions (Loomia blueprint)
- **`dashboard`**: Dashboard configurations (Loomia blueprint)
- **`target`**: Goals/targets (Loomia blueprint)
- **`saved_view`**: Saved filters/views (Konzessionsmanagement)

### Resource Relationships

Resources have dependencies:
```json
{
  "parent_resource_ids": [
    "d5e492f0-cc0e-11ef-a14e-134eb0f9ad2a",
    "4677d7fe-112d-4cad-b411-678715ffa261"
  ],
  "hard_dependencies": []
}
```

- **parent_resource_ids**: Resources this depends on
- **hard_dependencies**: Critical dependencies that must be installed first

### Installation Impact

```json
{
  "impact_on_install": ["create"]
}
```

Possible values:
- `create`: Creates new resource
- `update`: Updates existing resource
- `delete`: Removes resource

---

## 3. Hausanschluss Blueprint Deep Dive

### What It Contains (281 Resources)

**Workflows**: Complete house connection process definitions
**Journeys**: Customer-facing forms for:
- Electricity connection requests
- Gas connection requests
- Water connection requests
- District heating requests
- Fiber optic requests
- Combined requests

**Products**: 
- Netzanschluss Strom (Electricity connection)
- Netzanschluss Gas (Gas connection)
- Netzanschluss Wasser (Water connection)
- Veränderung Netzanschluss (Connection modifications)

**Automations**:
- Email notifications
- Status updates
- Data validation
- Document generation

**Templates**:
- Email templates for customer communication
- Document templates

**Schema Configurations**:
- Custom fields for opportunity entities
- Field groupings
- Validation rules

---

## 4. Blueprint vs Workflow: Key Differences

| Aspect | Workflow | Blueprint |
|--------|----------|-----------|
| **Nature** | Process definition | Package/Container |
| **Scope** | Single process with sections & steps | Package of 100+ resources (can include workflows) |
| **Relationship** | Can be standalone or part of a blueprint | Contains workflows and other resources |
| **Components** | Sections + Steps | Workflows + Journeys + Products + Templates + Automations + etc. |
| **Installation** | Created individually | Installed as a complete package |
| **Dependencies** | References other resources | Bundles all dependencies together |
| **Versioning** | Updated in place | Versioned releases (v1.0.0, v2.0.0) |
| **Portability** | Org-specific | Can be exported/imported between orgs with all resources |
| **Export** | Can be exported as part of a blueprint | Top-level packaging mechanism |
| **Use Case** | Define a specific process | Package complete solutions for deployment |

---

## 5. Architecture & Packaging Patterns

### Understanding the Hierarchy

```
Blueprint (Package)
├── Workflows (can include multiple)
├── Journeys (customer forms)
├── Products & Pricing
├── Automation Flows
├── Email Templates
├── Schema Configurations
└── Other Resources
```

Workflows can exist in two ways:
1. **Standalone Workflows**: Created and managed independently
2. **Packaged Workflows**: Included within blueprints and exported together

### Pattern 1: Blueprint-Packaged Workflow
**Example**: "Blueprintprozess Hausanschluss" (wfQULHNKGs) within "Hausanschluss Kombi" blueprint

This workflow is packaged inside the blueprint along with all supporting resources:
- Pre-configured journeys (customer forms)
- Pre-configured products
- Pre-configured automations
- Pre-configured email templates

**Benefits**:
- ✅ Complete solution in one package
- ✅ Faster implementation (all resources together)
- ✅ Best practices built-in
- ✅ Consistency across deployments
- ✅ Easier updates (upgrade entire blueprint version)
- ✅ Portable between organizations

### Pattern 2: Standalone Workflow
**Example**: "Service - Umzug/Auszug" (wf7t3jus0X)

Custom-built workflow not part of any blueprint package.

**Benefits**:
- ✅ Full customization
- ✅ Org-specific logic
- ✅ Independent management
- ✅ Can later be packaged into a blueprint if needed

---

## 6. Common Workflow Patterns in Your System

### 1. Installer/Concession Management (5 workflows)
Process installer applications, renewals, and registrations:
- New registrations
- ID renewals
- Additional specialists
- Guest vs. permanent installers

### 2. House Connection (3 workflows + blueprint)
Handle customer requests for utility connections:
- Check jurisdiction
- Validate customer data
- Feasibility assessment
- Site visits
- Quote generation

### 3. Sales Processes (2 workflows)
Manage outbound sales:
- Planning
- Campaign execution

---

## 7. Automation Integration

Workflows can trigger automations at specific steps:

```json
{
  "executionType": "AUTOMATION",
  "automationConfig": {
    "flowId": "50db4e7e-5ffa-46d1-b6c6-2b38f52e5326"
  }
}
```

Automation flows can:
- Send emails
- Update records
- Create tasks
- Call webhooks
- Perform calculations
- Route to different paths

---

## 8. Customer Portal Integration

Workflows integrate with customer portals (ECP):

```json
{
  "ecp": {
    "enabled": true,
    "label": "Prüfung der Anfrage",
    "description": "Aktuell prüfen wir Ihre eingereichten Daten..."
  }
}
```

Customers see:
- Current process stage
- Status updates
- Next steps
- Expected timeline

---

## 9. Best Practices Observed

### From Your Workflows:

1. **Clear Section Names**: "Anfrage" → "Angebotserstellung" → "Beauftragung"
2. **Descriptive Step Names**: "Zuständigkeit prüfen", "Kundendaten plausibilisieren"
3. **Customer Communication**: ECP labels provide transparent status updates
4. **Optional Steps**: "(Optional) Vor-Ort-Termin" allows flexibility
5. **Automation Where Appropriate**: Repetitive tasks automated
6. **Entity Updates**: Status automatically reflects workflow progress

---

## 10. How to Work With Workflows & Blueprints

### Exporting Workflows
```bash
python scripts/workflows/export_workflows.py
# Workflows saved to: data/output/workflows/
```

### Exporting Blueprints
```bash
python scripts/blueprints/export_blueprints.py
# Blueprints saved to: data/output/blueprints/
```

### Analyzing a Specific Workflow
```bash
cat data/output/workflows/workflow_<ID>.json | jq '.flow'
```

### Analyzing Blueprint Contents
```bash
cat data/output/blueprints/blueprint_<ID>.json | jq '.resources[] | select(.type=="workflow_definition")'
```

### Finding Blueprint Resources by Type
```python
# Count resources by type
resources = blueprint['resources']
types = {}
for r in resources:
    t = r.get('type')
    types[t] = types.get(t, 0) + 1
```

---

## 11. Modification & Export Strategies

### To Modify a Standalone Workflow:
1. Export current workflow
2. Update JSON structure (sections, steps, automations)
3. Use Workflow Definition API to update
4. Test in non-production environment

### To Package a Workflow into a Blueprint:
1. Export the workflow definition
2. Create or update blueprint manifest
3. Add workflow as a resource with type `workflow_definition`
4. Include all dependent resources (journeys, products, automations, etc.)
5. Set appropriate dependencies and installation impact
6. Version the blueprint

### To Modify a Blueprint:
1. Export blueprint and all resources
2. Modify individual resources (including packaged workflows)
3. Update blueprint manifest
4. Increment version number (v1.0.0 → v1.1.0 or v2.0.0)
5. Re-deploy blueprint package

### To Export Workflows from Blueprints:
Workflows are automatically included when exporting blueprints - they appear as resources with type `workflow_definition` within the blueprint's resource list.

---

## Summary

Your Epilot system uses a **hierarchical packaging architecture**:

### Workflows (Process Definitions)
- Individual process definitions with sections and steps
- Can exist standalone or be packaged within blueprints
- Define the step-by-step business process logic
- Integration with automations and customer portals
- You have 14 workflows total

### Blueprints (Resource Packages)
- Top-level packaging mechanism for deployment
- Bundle 171-281 resources including workflows
- Contain workflows, forms, products, templates, automations, and more
- Versioned and portable between organizations
- Workflows can be exported as part of blueprints
- You have 3 blueprints: Hausanschluss Kombi, Loomia, and Konzessionsmanagement

**Key Relationship**: Blueprints are containers that package workflows together with all supporting resources. When you export a blueprint, the workflows are included as resources within the package. This makes blueprints the primary mechanism for deploying complete, pre-configured business solutions.

**Example**: The "Blueprintprozess Hausanschluss" workflow is packaged inside the "Hausanschluss Kombi" blueprint along with 280 other resources (forms, products, templates, etc.) that support the house connection process. When the blueprint is exported or deployed, all these resources travel together as a cohesive unit.
