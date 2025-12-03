# Workflow Execution Guide - How to Start and Use Workflows

**Date:** 2025-12-03  
**Status:** ✅ Complete Guide

## Table of Contents
1. [How to Manually Start a Workflow](#1-how-to-manually-start-a-workflow)
2. [What Entities Can Have Workflows](#2-what-entities-can-have-workflows)
3. [Opportunities vs Other Entities](#3-opportunities-vs-other-entities)
4. [Automation-Triggered Workflows](#4-automation-triggered-workflows)
5. [Best Practices](#5-best-practices)

---

## 1. How to Manually Start a Workflow

### Method 1: Via Epilot UI (Easiest)

**Steps:**
1. Open entity in Epilot portal (opportunity, order, contact, etc.)
2. Click "Workflows" tab or "Start Workflow" button
3. Select workflow from dropdown (e.g., "Ausbau Glasfaser")
4. Click "Start"
5. Workflow execution creates workflow steps visible in entity

**Portal URLs:**
- Opportunities: `https://portal.epilot.cloud/app/opportunities/{entity_id}`
- Orders: `https://portal.epilot.cloud/app/orders/{entity_id}`
- Any entity: `https://portal.epilot.cloud/app/entities/{schema}/{entity_id}`

### Method 2: Via API (Programmatic)

**Endpoint:**
```
POST https://workflows-execution.sls.epilot.io/v1/workflows/executions
```

**Payload:**
```json
{
  "definitionId": "wfQpwhJF6J",
  "entityId": "abc123-your-entity-id",
  "entitySchema": "opportunity"
}
```

**Python Example:**
```python
import asyncio
from lib.auth import load_env
from lib.api_client import EpilotClient

async def start_workflow():
    load_env()
    client = EpilotClient()
    
    payload = {
        "definitionId": "wfQpwhJF6J",  # Ausbau Glasfaser workflow
        "entityId": "abc123-your-entity-id",  # Your entity ID
        "entitySchema": "opportunity"  # Entity type
    }
    
    result = await client.post(
        "https://workflows-execution.sls.epilot.io/v1/workflows/executions",
        data=payload
    )
    
    execution_id = result.get('id')
    print(f"✅ Workflow started: {execution_id}")
    return result

asyncio.run(start_workflow())
```

**Response:**
```json
{
  "id": "38w428mr9ee",
  "definitionId": "wfQpwhJF6J",
  "entityId": "abc123-your-entity-id",
  "entitySchema": "opportunity",
  "status": "STARTED",
  "createdAt": "2025-12-03T15:00:00Z",
  "steps": [...]
}
```

### Method 3: Via Automation (Automatic)

Workflows can start automatically when triggered by automations:
- Journey submission → Create entity → Trigger workflow
- Entity status change → Trigger workflow
- Manual button click in process → Trigger workflow

See [Section 4](#4-automation-triggered-workflows) for details.

---

## 2. What Entities Can Have Workflows

### ✅ Any Entity Schema Can Have Workflows!

Workflows are **not limited to opportunities**. You can attach workflows to:

| Entity Schema | Use Case Example | Workflow Example |
|--------------|------------------|------------------|
| **opportunity** | Sales process, customer requests | "Hausanschluss Bearbeitung" |
| **order** | Order fulfillment, delivery | "Order Processing & Delivery" |
| **contact** | Onboarding, verification | "Customer Onboarding Process" |
| **contract** | Contract review, approval | "Contract Review Workflow" |
| **submission** | Form processing | Journey submission handling |
| **automation_step** | Workflow steps themselves | Sub-workflows |
| **file** | Document approval | "Document Review Process" |
| **account** | Company onboarding | "B2B Partner Setup" |
| **Custom schemas** | Any custom entity type | Your custom processes |

### How It Works

When you start a workflow execution, you specify:
1. **definitionId**: Which workflow to run (e.g., `wfQpwhJF6J`)
2. **entityId**: Which specific entity instance (e.g., opportunity ID `abc123`)
3. **entitySchema**: What type of entity (e.g., `opportunity`, `order`, `contact`)

The workflow then:
- Creates workflow steps linked to that entity
- Shows in entity's "Workflows" tab in UI
- Can update entity attributes as workflow progresses
- Can access entity data in workflow steps

### Example Scenarios

#### Scenario 1: Ausbau Glasfaser on Opportunity
```json
{
  "definitionId": "wfQpwhJF6J",
  "entityId": "opp-glasfaser-nordstrasse-123",
  "entitySchema": "opportunity"
}
```
**Use Case:** Track expansion project from planning to customer notification

#### Scenario 2: Ausbau Glasfaser on Order
```json
{
  "definitionId": "wfQpwhJF6J",
  "entityId": "order-ausbau-projekt-456",
  "entitySchema": "order"
}
```
**Use Case:** Track actual construction work after contract signed

#### Scenario 3: Ausbau Glasfaser on Contact (Less Common)
```json
{
  "definitionId": "wfQpwhJF6J",
  "entityId": "contact-stadtwerke-tech-team",
  "entitySchema": "contact"
}
```
**Use Case:** Track infrastructure projects assigned to specific team

---

## 3. Opportunities vs Other Entities

### Understanding Entity Purposes

#### Opportunities (Sales & Planning)
**Purpose:** Track potential business before it's confirmed

**Characteristics:**
- Pre-sale or pre-project phase
- Status: ausstehend → bearbeitung → geschlossen/abgebrochen
- Represents "could happen" not "will happen"
- Used for pipeline management

**When to Use:**
- Customer expresses interest in Glasfaser expansion
- Preliminary site assessment needed
- Feasibility study phase
- Sales qualification

**Wülfrath Example:**
```json
{
  "_schema": "opportunity",
  "_title": "Glasfaser Neubaugebiet Nordstraße",
  "status": "ausstehend",
  "beschreibung": "Interesse an Glasfaser für neues Wohngebiet",
  "kontakt": ["kunde-meier-123"]
}
```

#### Orders (Confirmed Work)
**Purpose:** Track confirmed projects and work execution

**Characteristics:**
- Post-sale or confirmed project
- Has contract, budget, timeline
- Represents "will happen" commitments
- Used for delivery management

**When to Use:**
- Contract signed for Glasfaser expansion
- Budget approved by Stadtwerke
- Construction work scheduled
- Actual implementation phase

**Wülfrath Example:**
```json
{
  "_schema": "order",
  "_title": "Ausbau Glasfaser Nordstraße - Bauauftrag",
  "status": "in_progress",
  "amount_total": 45000.00,
  "opportunity": [{"$relation": [{"entity_id": "opp-123"}]}],
  "produkte": ["prod-glasfaser-ausbau"]
}
```

### Recommended Approach for Ausbau Glasfaser

#### ✅ Best Practice: Use Both

**Phase 1: Opportunity (Planning & Approval)**
- Entity: **Opportunity**
- Workflow: None or "Ausbau Planung" (if you create one)
- Purpose: Assess feasibility, get approvals, budget planning
- Status flow: ausstehend → bearbeitung → geschlossen (approved)

**Phase 2: Order (Execution)**
- Entity: **Order** (created from opportunity)
- Workflow: **"Ausbau Glasfaser"** (wfQpwhJF6J)
- Purpose: Execute construction, coordinate providers, document progress
- Links back to original opportunity

**Why This Works:**
1. **Opportunity** tracks sales/planning phase with your current demo data
2. **Order** represents actual construction contract and execution
3. Workflow lives on Order where actual work happens
4. Opportunity → Order conversion is standard Epilot pattern
5. Historical tracking: Order references original Opportunity

#### Alternative: Opportunity-Only Approach

**If you want simpler structure:**
- Keep infrastructure projects as Opportunities
- Run "Ausbau Glasfaser" workflow on Opportunity
- Use opportunity custom fields to track construction details
- Status meanings shift:
  - **ausstehend**: Planning phase
  - **bearbeitung**: Active construction
  - **geschlossen**: Construction complete

**When This Makes Sense:**
- Internal projects (not customer-facing sales)
- Stadtwerke infrastructure expansion (not per-customer)
- Don't need separate sales vs execution tracking
- Simpler for demos and smaller municipalities

### Your Current Demo Data

You have 8 opportunities in demo. Here's how to proceed:

**Option A: Treat as Planning Phase**
1. Opportunities represent "we're considering this expansion"
2. Create Orders when approved: `opp.status = geschlossen` → Create Order
3. Run "Ausbau Glasfaser" workflow on Orders

**Option B: Treat as Execution Phase**
1. Opportunities represent "approved expansion projects"
2. Run "Ausbau Glasfaser" workflow directly on Opportunities
3. Status "bearbeitung" = active construction
4. Status "geschlossen" = construction complete

**Recommendation:** Use **Option A** if you want to demo full lifecycle (planning → execution). Use **Option B** for simpler demos focused on construction management.

---

## 4. Automation-Triggered Workflows

### Pattern: Journey → Entity → Workflow

Most common in production Epilot:

```
Customer submits Journey
  ↓
Automation: journey_submission trigger
  ↓
Actions:
  1. map-entity → Create Opportunity
  2. trigger-workflow → Start "Ausbau Glasfaser"
  3. send-email → Notify team
```

**Automation Config:**
```json
{
  "flow_name": "Glasfaser Anfrage → Ausbau Workflow",
  "enabled": true,
  "triggers": [{
    "type": "journey_submission",
    "configuration": {
      "source_id": "YOUR_JOURNEY_ID"
    }
  }],
  "actions": [
    {
      "name": "Create Opportunity",
      "type": "map-entity",
      "config": {
        "target_schema": "opportunity",
        "mapping_config": {...}
      }
    },
    {
      "name": "Start Ausbau Workflow",
      "type": "trigger-workflow",
      "config": {
        "target_workflow": "wfQpwhJF6J"
      }
    },
    {
      "name": "Notify Team",
      "type": "send-email",
      "config": {
        "to": ["team@stadtwerke-wuelfrath.de"],
        "subject": "Neues Ausbau-Projekt",
        "email_template_id": "..."
      }
    }
  ]
}
```

### Pattern: Entity Status Change → Workflow

For approval-based workflows:

```
User changes Opportunity status to "bearbeitung"
  ↓
Automation: entity_operation trigger
  ↓
Actions:
  1. trigger-workflow → Start "Ausbau Glasfaser"
  2. send-email → Notify construction team
```

**Automation Config:**
```json
{
  "flow_name": "Opportunity Approved → Start Construction",
  "enabled": true,
  "triggers": [{
    "type": "entity_operation",
    "configuration": {
      "schema": "opportunity",
      "operation": ["update"],
      "attributes": ["status"]
    }
  }],
  "conditions": [{
    "id": "status-check",
    "statements": [{
      "operation": "equals",
      "source": {
        "schema": "opportunity",
        "attribute": "status"
      },
      "values": ["bearbeitung"]
    }]
  }],
  "actions": [{
    "name": "Start Construction Workflow",
    "type": "trigger-workflow",
    "condition_id": "status-check",
    "config": {
      "target_workflow": "wfQpwhJF6J"
    }
  }]
}
```

### Pattern: Manual Trigger Within Workflow

For ad-hoc workflow starts:

```
User in existing workflow clicks "Start Sub-Process"
  ↓
Automation: entity_manual trigger
  ↓
Actions:
  1. trigger-workflow → Start another workflow
```

---

## 5. Best Practices

### ✅ DO: Choose Right Entity Type

| Project Type | Recommended Entity | Reason |
|--------------|-------------------|--------|
| Infrastructure expansion (not customer-specific) | **Opportunity** or custom schema | Internal planning project |
| Customer house connection | **Opportunity** → **Order** | Sales → Execution transition |
| Contracted construction work | **Order** | Confirmed work with budget |
| Internal process (no customer) | Custom schema or **Opportunity** | Flexibility |

### ✅ DO: Link Entities Together

When using Opportunity → Order pattern:

**In Order entity:**
```json
{
  "_schema": "order",
  "_title": "Ausbau Nordstraße - Bauauftrag",
  "opportunity": [{"$relation": [{"entity_id": "opp-123"}]}],
  "contact": [{"$relation": [{"entity_id": "contact-456"}]}]
}
```

This creates:
- Clear audit trail (Order came from which Opportunity?)
- UI navigation (click to see related entities)
- Reporting (conversion rates, pipeline analysis)

### ✅ DO: Use Workflow for Process Management

Workflows are for:
- Multi-step processes with coordination
- Approval gates
- Mobile field work documentation
- Status tracking across phases
- Team collaboration

Workflows are NOT for:
- Simple status changes (use entity attributes)
- Single-action tasks (use automations)
- Pure data storage (use entity fields)

### ✅ DO: Configure Entity Updates in Workflow

In workflow definition, you can auto-update entity:

```json
{
  "updateEntityAttributes": [
    {
      "source": "current_section",
      "target": {
        "entitySchema": "opportunity",
        "entityAttribute": "ausbau_phase"
      }
    },
    {
      "source": "workflow_status",
      "target": {
        "entitySchema": "opportunity",
        "entityAttribute": "status"
      }
    }
  ]
}
```

This automatically updates opportunity fields as workflow progresses.

### ❌ DON'T: Confuse Entity Schema with Business Purpose

- **Opportunities are NOT only for sales** - use for any "proposed" or "potential" work
- **Orders are NOT only for customer orders** - use for any confirmed work
- **Workflows can attach to ANY entity type** - don't limit yourself

### ❌ DON'T: Over-complicate Entity Structure

**Too Complex:**
```
Opportunity → Lead → Project → Order → Workorder → Task
```

**Better:**
```
Opportunity (planning) → Order (execution)
```

Keep it simple. Epilot entities are flexible - use fields and workflows to add complexity, not more entity types.

---

## Practical Examples for Your Demo

### Example 1: Start Workflow on Existing Demo Opportunity

**Using API:**
```python
import asyncio
from lib.auth import load_env
from lib.api_client import EpilotClient

async def start_demo_workflow():
    load_env()
    client = EpilotClient()
    
    # Get one of your demo opportunities
    opps = await client.get("https://entity.sls.epilot.io/v1/entity/opportunity?limit=1")
    opp_id = opps['results'][0]['_id']
    
    # Start Ausbau Glasfaser workflow on it
    result = await client.post(
        "https://workflows-execution.sls.epilot.io/v1/workflows/executions",
        data={
            "definitionId": "wfQpwhJF6J",
            "entityId": opp_id,
            "entitySchema": "opportunity"
        }
    )
    
    print(f"✅ Workflow started on opportunity {opp_id}")
    print(f"   Execution ID: {result['id']}")
    print(f"   View in UI: https://portal.epilot.cloud/app/opportunities/{opp_id}")

asyncio.run(start_demo_workflow())
```

### Example 2: Create Order and Start Workflow

**For Opportunity → Order pattern:**
```python
async def convert_opportunity_to_order_with_workflow():
    load_env()
    client = EpilotClient()
    
    opp_id = "your-opportunity-id"
    
    # Get opportunity details
    opp = await client.get(f"https://entity.sls.epilot.io/v1/entity/opportunity/{opp_id}")
    
    # Create order from opportunity
    order_data = {
        "_schema": "order",
        "_title": f"Ausbau: {opp['_title']}",
        "opportunity": [{"$relation": [{"entity_id": opp_id}]}],
        "contact": opp.get('contact', []),
        "anschrift": opp.get('anschrift'),
        "amount_total": 45000.00,  # Your project budget
        "_tags": ["ausbau", "glasfaser"] + opp.get('_tags', [])
    }
    
    order = await client.post(
        "https://entity.sls.epilot.io/v1/entity/order",
        data=order_data
    )
    order_id = order['_id']
    
    # Start workflow on order
    workflow = await client.post(
        "https://workflows-execution.sls.epilot.io/v1/workflows/executions",
        data={
            "definitionId": "wfQpwhJF6J",
            "entityId": order_id,
            "entitySchema": "order"
        }
    )
    
    # Update opportunity status
    await client.patch(
        f"https://entity.sls.epilot.io/v1/entity/opportunity/{opp_id}",
        data={"status": "geschlossen"}
    )
    
    print(f"✅ Created order {order_id} from opportunity {opp_id}")
    print(f"✅ Started Ausbau Glasfaser workflow: {workflow['id']}")
    print(f"✅ View order: https://portal.epilot.cloud/app/orders/{order_id}")
```

### Example 3: Create Automation for Status-Based Trigger

**Script to create automation:**
```python
async def create_status_trigger_automation():
    load_env()
    client = EpilotClient()
    
    automation = {
        "flow_name": "Wülfrath: Opportunity Approved → Start Ausbau",
        "entity_schema": "opportunity",
        "enabled": True,
        "triggers": [{
            "type": "entity_operation",
            "configuration": {
                "schema": "opportunity",
                "operation": ["update"],
                "attributes": ["status"]
            }
        }],
        "conditions": [{
            "id": "status-bearbeitung",
            "statements": [{
                "operation": "equals",
                "source": {
                    "schema": "opportunity",
                    "attribute": "status"
                },
                "values": ["bearbeitung"]
            }]
        }],
        "actions": [
            {
                "id": "start-workflow",
                "name": "Start Ausbau Glasfaser Workflow",
                "type": "trigger-workflow",
                "condition_id": "status-bearbeitung",
                "config": {
                    "target_workflow": "wfQpwhJF6J"
                }
            },
            {
                "id": "notify-team",
                "name": "Notify Construction Team",
                "type": "send-email",
                "condition_id": "status-bearbeitung",
                "config": {
                    "to": ["bau-team@stadtwerke-wuelfrath.de"],
                    "subject": "Neues Ausbau-Projekt genehmigt",
                    "body_html": """
                        <h2>Ausbau-Projekt genehmigt</h2>
                        <p>Opportunity: {{opportunity._title}}</p>
                        <p>Workflow wurde automatisch gestartet.</p>
                        <p><a href='https://portal.epilot.cloud/app/opportunities/{{opportunity._id}}'>Projekt öffnen</a></p>
                    """,
                    "language_code": "de"
                }
            }
        ]
    }
    
    result = await client.post(
        "https://automation.sls.epilot.io/v1/automation/flows",
        data=automation
    )
    
    print(f"✅ Automation created: {result['id']}")
    print("Now when you change opportunity status to 'bearbeitung',")
    print("the Ausbau Glasfaser workflow will start automatically!")

asyncio.run(create_status_trigger_automation())
```

---

## Quick Reference

### Start Workflow Manually (API)
```bash
POST https://workflows-execution.sls.epilot.io/v1/workflows/executions
{
  "definitionId": "wfQpwhJF6J",
  "entityId": "YOUR_ENTITY_ID",
  "entitySchema": "opportunity"  # or "order", "contact", etc.
}
```

### Get Workflow Executions
```bash
GET https://workflows-execution.sls.epilot.io/v1/workflows/executions?limit=10
```

### Get Specific Execution
```bash
GET https://workflows-execution.sls.epilot.io/v1/workflows/executions/{execution_id}
```

### Entity Schemas That Work Well with Workflows
- `opportunity` - Planning and sales processes
- `order` - Fulfillment and delivery
- `contact` - Onboarding and verification
- `contract` - Review and approval
- `submission` - Journey form processing
- Custom schemas - Your specific needs

---

## Summary

### Key Takeaways

1. **Workflows attach to ANY entity type**, not just opportunities
2. **Manual start**: UI button or API POST to `/workflows/executions`
3. **Automatic start**: Via automations (`trigger-workflow` action)
4. **Opportunities**: Best for planning/sales phase OR simpler single-entity approach
5. **Orders**: Best for execution phase with confirmed budget
6. **Infrastructure projects**: Can use opportunities (simpler) or opportunity→order (more structured)

### Your Ausbau Glasfaser Workflow

Can run on:
- ✅ Opportunities (your current demo data)
- ✅ Orders (after conversion from opportunity)
- ✅ Custom "infrastructure_project" schema (if you create one)
- ✅ Any other entity type that makes sense for your use case

**Recommendation for Wülfrath Demo:**
- Keep current opportunities as planning phase
- Start "Ausbau Glasfaser" workflow directly on opportunities for demo simplicity
- Status "bearbeitung" = active construction, status "geschlossen" = complete
- Later: Add automation to auto-start workflow when status changes

---

**Created:** 2025-12-03  
**Last Updated:** 2025-12-03  
**Version:** 1.0
