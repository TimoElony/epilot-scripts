# Opportunity → Workflow Automation Guide

## How Hausanschluss Opportunities Trigger Workflows

### Overview
Yes, this is configured in **Automations**, not in Workflows themselves. Automations are the event-driven bridge that connects customer actions (journey submissions) and entity changes (opportunity status) to workflow execution.

---

## Real Example: Hausanschluss Kombi Automation

**Automation Name:** "Journey Automation: Hausanschluss Kombi (Anfrage - Strom, Gas, Wasser, Fernwärme, Glasfaser)"

**File:** `automation_ff2c5af8-7719-4f41-b5a4-04719cb43551.json`

**Workflow ID:** `wfhqY-Pp4k`

### How It Works (Step-by-Step)

```
1. Customer submits Journey form
   ↓
2. Automation TRIGGER: journey_submission
   - Journey ID: dd76e170-b4a3-11f0-99fc-272b9293c5e0
   ↓
3. Automation ACTIONS (executed in sequence):
   
   A. Create Entities (map-entity actions):
      - Create Account (Firma) from "Kontaktdaten AnschlussnehmerIn"
      - Create Contact from "Kontaktdaten AnschlussnehmerIn"
      - Create Account from "Kontaktdaten GrundstückseigentümerIn"
      - Create Contact from "Kontaktdaten GrundstückseigentümerIn"
      - Create Account from "Kontaktdaten AntragstellerIn"
      - Create Contact from "Kontaktdaten AntragstellerIn"
      - Create Account from "Kontaktdaten AnschlussnutzerIn"
      - Create Contact from "Kontaktdaten AnschlussnutzerIn"
      - Create Account from "Kontaktdaten RechnungsempfängerIn"
      - Create Contact from "Kontaktdaten RechnungsempfängerIn"
   
   B. Create Order (cart-checkout):
      - Create "Bestellung aus Journey"
   
   C. Create Opportunity (map-entity):
      - Create "Opportunity aus Journey"
      - ID: bfcccd02-a1e2-4fad-a7f9-015a75f77317
   
   D. Conditional Purpose Assignment (10 conditional map-entity actions):
      - IF "ha_netzanschlusssparte" contains "Strom" AND "ha_neuanschluss_oder_veraenderung" = "Neuanschluss"
        → Add purpose "e6ed96be-f780-431d-b716-0a5183e3e7ef" (Neuanschluss - Strom)
      - IF "ha_netzanschlusssparte" contains "Strom" AND "ha_neuanschluss_oder_veraenderung" = "Veränderung..."
        → Add purpose "b8768290-d92b-490d-8741-e051c31f6be7" (Veränderung - Strom)
      - [8 more similar conditions for Gas, Wasser, Fernwärme, Glasfaser]
   
   E. **TRIGGER WORKFLOW** (trigger-workflow action):
      - Action ID: 367cc371-279c-4dd5-8350-261750c66515
      - Target Workflow: wfhqY-Pp4k
      - Config: {
          "filter_with_purposes": true,
          "conditions": [],
          "assign_steps": [],
          "target_workflow": "wfhqY-Pp4k"
        }
   
   F. Send Confirmation Email (send-email):
      - Template ID: 459ca38a-ccee-45a8-853a-e5b41cc1a34d
      - Language: de
```

### Key Configuration Elements

#### Trigger Configuration
```json
{
  "triggers": [
    {
      "type": "journey_submission",
      "configuration": {
        "source_id": "dd76e170-b4a3-11f0-99fc-272b9293c5e0"
      },
      "id": "354e2241-01da-44b5-b886-19361d766b5a"
    }
  ]
}
```

#### Workflow Trigger Action
```json
{
  "created_automatically": false,
  "name": "Trigger Workflow",
  "id": "367cc371-279c-4dd5-8350-261750c66515",
  "type": "trigger-workflow",
  "config": {
    "filter_with_purposes": true,
    "conditions": [],
    "assign_steps": [],
    "target_workflow": "wfhqY-Pp4k"
  }
}
```

**Important:** `filter_with_purposes: true` means the workflow will filter steps based on the opportunity's `_purpose` field set in previous actions.

---

## Two Main Patterns for Opportunity → Workflow Automation

### Pattern 1: Journey Submission → Opportunity Creation → Workflow Trigger

**Use Case:** Customer submits a form (e.g., Hausanschluss request), automatically creates opportunity and starts workflow

**Configuration:**
```json
{
  "flow_name": "Journey Automation: [Your Journey Name]",
  "enabled": true,
  "triggers": [
    {
      "type": "journey_submission",
      "configuration": {
        "source_id": "YOUR_JOURNEY_ID"
      }
    }
  ],
  "actions": [
    {
      "name": "Create Opportunity from Journey",
      "type": "map-entity",
      "config": {
        "mapping_config": {
          "config_id": "YOUR_MAPPING_CONFIG_ID",
          "target_id": "YOUR_TARGET_BLOCK_ID"
        },
        "target_schema": "opportunity"
      }
    },
    {
      "name": "Trigger Workflow",
      "type": "trigger-workflow",
      "config": {
        "target_workflow": "YOUR_WORKFLOW_ID"
      }
    },
    {
      "name": "Send Confirmation Email",
      "type": "send-email",
      "config": {
        "email_template_id": "YOUR_EMAIL_TEMPLATE_ID",
        "language_code": "de"
      }
    }
  ]
}
```

**Advantages:**
- Fully automated from customer submission to workflow start
- No manual intervention needed
- Immediate workflow execution
- Typical for: Hausanschluss requests, contract applications, service requests

---

### Pattern 2: Opportunity Status Change → Workflow Trigger

**Use Case:** Manual review required - workflow starts only when opportunity reaches specific status (e.g., "geschlossen" or "bearbeitung")

**Configuration:**
```json
{
  "flow_name": "Opportunity Status Change - Trigger Workflow",
  "enabled": true,
  "triggers": [
    {
      "type": "entity_operation",
      "configuration": {
        "entity_schema": "opportunity",
        "operation": "update",
        "conditions": [
          {
            "attribute": "status",
            "operator": "equals",
            "value": "bearbeitung"
          }
        ]
      }
    }
  ],
  "actions": [
    {
      "name": "Trigger Workflow on Approval",
      "type": "trigger-workflow",
      "config": {
        "target_workflow": "YOUR_WORKFLOW_ID"
      }
    },
    {
      "name": "Notify Team",
      "type": "send-email",
      "config": {
        "email_template_id": "YOUR_EMAIL_TEMPLATE_ID",
        "language_code": "de"
      }
    }
  ]
}
```

**Advantages:**
- Manual quality check before workflow starts
- Workflow only executes for approved opportunities
- Typical for: High-value contracts, complex installations, permit-required services

---

## Automation Action Types Explained

### 1. map-entity
**Purpose:** Create or update entities (contact, account, opportunity, order)

**Example:**
```json
{
  "name": "Create Opportunity from Journey",
  "type": "map-entity",
  "allow_failure": false,
  "config": {
    "mapping_config": {
      "config_id": "72c7638f-ec6b-490f-a59c-9ec843ffc30c",
      "version": 3,
      "target_id": "95bdbf2d-d9cb-43fd-bf1a-be71d639f7ff"
    },
    "target_schema": "opportunity"
  }
}
```

### 2. trigger-workflow
**Purpose:** Start a workflow with the created/updated opportunity

**Example:**
```json
{
  "name": "Trigger Workflow",
  "type": "trigger-workflow",
  "config": {
    "filter_with_purposes": true,
    "conditions": [],
    "assign_steps": [],
    "target_workflow": "wfhqY-Pp4k"
  }
}
```

**Config Options:**
- `target_workflow`: Workflow ID to execute
- `filter_with_purposes`: If true, workflow steps are filtered by opportunity's `_purpose` field
- `conditions`: Additional runtime conditions
- `assign_steps`: Auto-assign specific workflow steps to users/teams

### 3. send-email
**Purpose:** Send confirmation/notification emails

**Example:**
```json
{
  "name": "Send Confirmation Email",
  "type": "send-email",
  "config": {
    "email_template_id": "459ca38a-ccee-45a8-853a-e5b41cc1a34d",
    "language_code": "de",
    "attachments": []
  }
}
```

### 4. cart-checkout
**Purpose:** Create order from journey cart

**Example:**
```json
{
  "name": "Create Order from Journey",
  "type": "cart-checkout",
  "allow_failure": true,
  "config": {
    "mapping_config": {
      "config_id": "72c7638f-ec6b-490f-a59c-9ec843ffc30c",
      "version": 3,
      "target_id": "fb19127c-40d5-4a8e-9378-56130d4d21fe"
    }
  }
}
```

### 5. create-document
**Purpose:** Generate PDF documents from templates

**Example:**
```json
{
  "name": "Generate Contract PDF",
  "type": "create-document",
  "config": {
    "document_template_id": "YOUR_TEMPLATE_ID",
    "language_code": "de"
  }
}
```

---

## Conditional Logic in Automations

The Hausanschluss automation uses **conditional actions** to assign different purposes based on customer selections:

### Condition Structure
```json
{
  "conditions": [
    {
      "id": "0d6433ef-bbbc-461e-aca9-fb7c217eb445",
      "statements": [
        {
          "operation": "contains",
          "source": {
            "schema": "opportunity",
            "attribute": "ha_netzanschlusssparte"
          },
          "values": ["Strom"]
        },
        {
          "operation": "equals",
          "source": {
            "schema": "opportunity",
            "attribute": "ha_neuanschluss_oder_veraenderung"
          },
          "values": ["Neuanschluss"]
        }
      ]
    }
  ]
}
```

### Action with Condition
```json
{
  "name": "Add Strom Neuanschluss Purpose",
  "type": "map-entity",
  "config": {
    "mapping_attributes": [
      {
        "operation": {
          "_append": ["e6ed96be-f780-431d-b716-0a5183e3e7ef"]
        },
        "target": "_purpose"
      }
    ],
    "target_schema": "opportunity"
  },
  "condition_id": "0d6433ef-bbbc-461e-aca9-fb7c217eb445"
}
```

**How It Works:**
1. Check if `ha_netzanschlusssparte` contains "Strom" AND `ha_neuanschluss_oder_veraenderung` equals "Neuanschluss"
2. If TRUE: Execute action to add purpose ID to opportunity
3. Later workflow uses `filter_with_purposes: true` to show only relevant steps

---

## Applying This to Your Wülfrath Demo

### Current Demo Opportunities
You have 8 opportunities created:

**Official Epilot Opportunity Statuses (per documentation):**
- **Ausstehend** (Pending) - New opportunities awaiting review
- **Bearbeitung** (In Progress) - Currently being processed
- **Abgeschlossen** (Closed/Completed) - Successfully completed
- **Abgebrochen** (Canceled) - Canceled/Rejected

**Your Demo Opportunities:**
1. Glasfaser Neubaugebiet Nordstraße (ausstehend)
2. Stromvertrag Gewerbepark (bearbeitung)
3. Wasseranschluss Einfamilienhaus (bearbeitung)
4. Gasanschluss Mehrfamilienhaus (bearbeitung)
5. Glasfaser Altbau Sanierung (ausstehend)
6. Wasser + Abwasser Neubau (geschlossen)
7. Strom + Gas Komplettpaket (bearbeitung)
8. Fernwärme Industriegebiet (geschlossen)

### Option A: Create Journey-Based Automation

**Best for:** Demonstrating full end-to-end automation from customer form to workflow execution

**Steps:**
1. Create a journey for "Hausanschluss Anfrage Wülfrath"
2. Configure form blocks for customer data, address, service selection (Strom, Gas, Wasser, Glasfaser)
3. Create automation with:
   - Trigger: `journey_submission`
   - Actions:
     - Create contact/account from form
     - Create opportunity
     - Trigger workflow (e.g., "Hausanschluss Bearbeitung Wülfrath")
     - Send confirmation email

### Option B: Create Status-Based Automation

**Best for:** Demonstrating approval workflows and manual quality checks

**Steps:**
1. Create automation with:
   - Trigger: `entity_operation` on opportunity schema
   - Conditions: `status` equals `"bearbeitung"` (or `"geschlossen"`)
   - Actions:
     - Trigger workflow (e.g., "Hausanschluss Installation Planung")
     - Send notification email to customer
     - Send task assignment email to installation team

**Example Configuration:**
```python
import httpx
import os
from dotenv import load_dotenv

load_dotenv()

api_token = os.getenv("EPILOT_API_TOKEN")
base_url = "https://automation.sls.epilot.io"

automation_config = {
    "flow_name": "Wülfrath Demo: Hausanschluss Bearbeitung → Workflow",
    "enabled": True,
    "triggers": [
        {
            "type": "entity_operation",
            "configuration": {
                "entity_schema": "opportunity",
                "operation": "update",
                "conditions": [
                    {
                        "attribute": "status",
                        "operator": "equals",
                        "value": "bearbeitung"
                    }
                ]
            }
        }
    ],
    "actions": [
        {
            "name": "Trigger Installation Workflow",
            "type": "trigger-workflow",
            "config": {
                "target_workflow": "YOUR_WORKFLOW_ID_HERE"
            }
        },
        {
            "name": "Send Approval Email",
            "type": "send-email",
            "config": {
                "email_template_id": "YOUR_EMAIL_TEMPLATE_ID_HERE",
                "language_code": "de"
            }
        }
    ]
}

# Create automation
response = httpx.post(
    f"{base_url}/v1/automation/flow",
    headers={"Authorization": f"Bearer {api_token}"},
    json=automation_config
)

print(f"Status: {response.status_code}")
print(response.json())
```

---

## Key Takeaways

### ✅ Automations Configure Opportunity → Workflow Triggers

**NOT workflows themselves** - workflows just define the process steps. Automations are the event-driven bridge.

### ✅ Two Main Trigger Types

1. **journey_submission**: Fully automated from form submission
2. **entity_operation**: Triggered by entity changes (status, field values)

### ✅ trigger-workflow Action Type

This is the key action that starts workflow execution:
```json
{
  "type": "trigger-workflow",
  "config": {
    "target_workflow": "wfhqY-Pp4k"
  }
}
```

### ✅ Conditional Logic for Smart Routing

Use conditions to:
- Assign different purposes based on service type (Strom, Gas, Wasser, Glasfaser)
- Filter workflow steps with `filter_with_purposes: true`
- Route to different workflows based on opportunity attributes

### ✅ Action Sequence Matters

Typical order:
1. Create entities (contact, account)
2. Create opportunity
3. Set opportunity attributes (purpose, status)
4. **Trigger workflow** ← The critical action
5. Send confirmation emails

---

## Next Steps for Your Project

1. **Explore Existing Automations:**
   ```bash
   cd /home/timoe/epilot-scripts/data/output/automations_20251202_180034
   # All 42 automation configurations are here
   ```

2. **Read Full Analysis:**
   ```bash
   cat /home/timoe/epilot-scripts/scripts/automations/AUTOMATION_ANALYSIS.md
   ```

3. **Create Demo Automation Script:**
   - Add script to `scripts/demo/erstelle_demo_automation.py`
   - Configure for Wülfrath opportunities
   - Test with existing opportunity status changes

4. **Link to Existing Workflows:**
   - Export workflows to find relevant workflow IDs
   - Reference workflow IDs in automation `target_workflow` config

---

## Statistics from Your Epilot Organization

**Total Automations Analyzed:** 42

**Trigger Type Distribution:**
- `journey_submission`: ~25 automations (60%)
- `entity_operation`: ~10 automations (24%)
- `entity_manual`: ~7 automations (16%)

**Action Type Usage:**
- `send-email`: 70% of automations
- `map-entity`: 60% of automations
- `trigger-workflow`: **30% of automations** (13 total)
- `cart-checkout`: 25% of automations
- `create-document`: 5% of automations

**Key Finding:** About 1/3 of your automations trigger workflows, showing this is a core integration pattern in your organization.

---

## API Endpoints Reference

### List Automations
```
GET https://automation.sls.epilot.io/v1/automation/flow
```

### Create Automation
```
POST https://automation.sls.epilot.io/v1/automation/flow
```

### Get Automation Details
```
GET https://automation.sls.epilot.io/v1/automation/flow/{flow_id}
```

### Update Automation
```
PUT https://automation.sls.epilot.io/v1/automation/flow/{flow_id}
```

### Enable/Disable Automation
```
PATCH https://automation.sls.epilot.io/v1/automation/flow/{flow_id}
Body: {"enabled": true/false}
```

---

## Questions? Common Scenarios

### Q: How do I make specific opportunity types trigger different workflows?

**A:** Use conditional actions with `condition_id`:
1. Define conditions checking opportunity attributes (type, category, service)
2. Create multiple `trigger-workflow` actions, each with different `condition_id`
3. Each condition routes to a different workflow

### Q: Can one opportunity trigger multiple workflows?

**A:** Yes! Add multiple `trigger-workflow` actions (with or without conditions) to execute workflows in sequence or based on different criteria.

### Q: How do I prevent workflow from starting until manual approval?

**A:** Use Pattern 2 (entity_operation trigger) with condition:
```json
{
  "operation": "equals",
  "attribute": "status",
  "value": "bearbeitung"
}
```

**Note:** The official Epilot opportunity statuses are:
- `ausstehend` (Pending)
- `bearbeitung` (In Progress)
- `geschlossen` (Closed/Completed)
- `abgebrochen` (Canceled)

Source: [Epilot Documentation - Status in Opportunities](https://help.epilot.cloud/de_DE/kundenbetreuung/6449990323730-Status-in-Opportunities-und-Bestellungen)

### Q: Can I test automations without affecting production?

**A:** Yes:
1. Set `"enabled": false` in automation config
2. Use test journey with different `source_id`
3. Create test opportunities with specific tags
4. Add condition to filter by tag: `{"attribute": "_tags", "operation": "contains", "value": "test"}`

---

**Generated:** 2025-12-02  
**Source Files:**
- `/home/timoe/epilot-scripts/data/output/automations_20251202_180034/automation_ff2c5af8-7719-4f41-b5a4-04719cb43551.json`
- `/home/timoe/epilot-scripts/scripts/automations/AUTOMATION_ANALYSIS.md`
