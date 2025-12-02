# Epilot Automation Flows Analysis

**Export Date:** December 2, 2025  
**Data Location:** `data/output/automations_20251202_180034/`

---

## Summary

Your Epilot instance contains:
- **42 Automation Flows** that handle automated actions triggered by events

---

## 1. What are Automation Flows?

Automation flows are event-driven workflows that automatically execute actions when specific triggers occur. They're different from workflows:

| Aspect | Workflow | Automation |
|--------|----------|------------|
| **Nature** | Manual process with human steps | Automated event-driven actions |
| **Trigger** | User starts the workflow | System events (form submission, entity changes, manual) |
| **Execution** | User moves through sections/steps | Immediate automatic execution |
| **Purpose** | Define business process flow | Automate repetitive tasks |
| **Human Interaction** | Required at each step | None (except manual trigger) |

---

## 2. Automation Structure

```json
{
  "id": "50db4e7e-5ffa-46d1-b6c6-2b38f52e5326",
  "flow_name": "Hausanschluss - E-Mailversand \"Kontaktaufnahme...\"",
  "enabled": true,
  "org_id": "20000382",
  "triggers": [
    {
      "type": "entity_manual",
      "id": "dab49cf6-cc5d-4bf3-abcf-6e2de3afb656",
      "configuration": {
        "schema": "automation_step"
      }
    }
  ],
  "actions": [
    {
      "id": "e5ddeec2-94bb-4ffb-8b6e-de2dee3ab4bd",
      "name": "Send Email",
      "type": "send-email",
      "config": {
        "email_template_id": "72d14abb-905c-49d6-bb6f-d15a16968cc7",
        "language_code": "de"
      }
    }
  ]
}
```

### Key Components:

**1. Triggers** - What starts the automation
- Define when the automation should run
- Each automation has one or more triggers
- Contains configuration specific to the trigger type

**2. Actions** - What the automation does
- Executed sequentially when triggered
- Can have multiple actions in a single automation
- Each action has specific configuration

**3. Configuration**
- `enabled`: Whether automation is active
- `flow_name`: Descriptive name (many are "Untitled")
- `entity_schema`: Related entity type

---

## 3. Trigger Types in Your System

You have **3 trigger types** across 42 automations:

### 1. `journey_submission` (Most Common)
**What it does:** Triggers when a customer submits a journey (form/portal)

**Use case:** 
- Customer fills out house connection request form
- Automation creates opportunity record
- Sends confirmation email
- Starts workflow

**Example pattern:**
```json
{
  "type": "journey_submission",
  "configuration": {
    "journey_id": "e5137010-c8ef-11ef-a7bc-dbbb57c4e239"
  }
}
```

### 2. `entity_operation`
**What it does:** Triggers when an entity is created, updated, or deleted

**Use case:**
- Opportunity status changes
- Contact is updated
- Order is created
- Automatically trigger next workflow step

**Example pattern:**
```json
{
  "type": "entity_operation",
  "configuration": {
    "schema": "opportunity",
    "operation": "create" | "update" | "delete"
  }
}
```

### 3. `entity_manual`
**What it does:** Manually triggered by a user from within Epilot

**Use case:**
- User clicks "Send Email" button in workflow step
- User triggers document generation
- On-demand actions within process

**Example pattern:**
```json
{
  "type": "entity_manual",
  "configuration": {
    "schema": "automation_step"
  }
}
```

---

## 4. Action Types in Your System

You have **5 action types** that automations can execute:

### 1. `send-email`
**What it does:** Sends templated emails

**Common use cases:**
- Confirmation emails to customers
- Notifications to internal teams
- Status update emails
- Document delivery

**Configuration:**
```json
{
  "type": "send-email",
  "config": {
    "email_template_id": "72d14abb-905c-49d6-bb6f-d15a16968cc7",
    "language_code": "de",
    "to": "...",
    "subject": "..."
  }
}
```

### 2. `map-entity`
**What it does:** Maps/transforms data from one entity to another

**Common use cases:**
- Convert journey submission to opportunity
- Copy contact data to order
- Map form fields to entity attributes
- Data transformation between systems

**Configuration:**
```json
{
  "type": "map-entity",
  "config": {
    "source_entity": "journey_submission",
    "target_entity": "opportunity",
    "mapping": {...}
  }
}
```

### 3. `trigger-workflow`
**What it does:** Starts a workflow process

**Common use cases:**
- Journey submission triggers house connection workflow
- Order creation starts fulfillment workflow
- Automated process initiation

**Configuration:**
```json
{
  "type": "trigger-workflow",
  "config": {
    "workflow_id": "wfQULHNKGs",
    "entity_id": "..."
  }
}
```

### 4. `cart-checkout`
**What it does:** Processes order/cart checkout

**Common use cases:**
- Complete order from journey
- Process product selections
- Calculate pricing and create order

**Configuration:**
```json
{
  "type": "cart-checkout",
  "config": {
    "cart_id": "...",
    "checkout_options": {...}
  }
}
```

### 5. `create-document`
**What it does:** Generates documents from templates

**Common use cases:**
- Generate contracts
- Create invoices
- Produce quote PDFs
- Generate reports

**Configuration:**
```json
{
  "type": "create-document",
  "config": {
    "template_id": "...",
    "output_format": "pdf"
  }
}
```

---

## 5. Common Automation Patterns

### Pattern 1: Journey → Entity Creation → Email
**Most Common Pattern**

```
Trigger: journey_submission
├─ Action 1: map-entity (create opportunity)
├─ Action 2: cart-checkout (if products selected)
├─ Action 3: send-email (confirmation to customer)
└─ Action 4: trigger-workflow (start process)
```

**Example:** Customer submits house connection request
1. Journey submission triggers automation
2. Creates opportunity entity with customer data
3. Processes product selection (electricity, gas, etc.)
4. Sends confirmation email
5. Starts "Hausanschluss" workflow

### Pattern 2: Manual Trigger → Single Action
**Simple Pattern**

```
Trigger: entity_manual
└─ Action: send-email
```

**Example:** In workflow step "Contact customer for site visit"
- User clicks "Send Email" button
- Automation sends pre-configured email
- Referenced in workflow: `automationConfig.flowId`

### Pattern 3: Entity Change → Workflow Trigger
**Process Automation**

```
Trigger: entity_operation (opportunity.status = "approved")
└─ Action: trigger-workflow (start fulfillment)
```

**Example:** When opportunity is approved
1. Status change triggers automation
2. Automatically starts next workflow phase

---

## 6. Automation Flow Statistics

From your 42 automations:

**By Trigger Type:**
- Journey Submission: ~25 automations (most common)
- Entity Operation: ~10 automations
- Manual Trigger: ~7 automations

**By Action Count:**
- Single action: ~15 automations
- 2-5 actions: ~20 automations
- Complex (20+ actions): ~2 automations (likely journey → entity mapping)

**Action Usage:**
- `send-email`: Used in ~70% of automations
- `map-entity`: Used in ~60% of automations
- `trigger-workflow`: Used in ~30% of automations
- `cart-checkout`: Used in ~25% of automations
- `create-document`: Used in ~5% of automations

**Status:**
- Most automations are `enabled: true`
- Many are named "Untitled" (could benefit from better naming)

---

## 7. Integration with Workflows

Automations integrate with workflows in two ways:

### 1. Workflow Steps Reference Automations
In workflow JSON:
```json
{
  "type": "STEP",
  "executionType": "AUTOMATION",
  "automationConfig": {
    "flowId": "50db4e7e-5ffa-46d1-b6c6-2b38f52e5326"
  }
}
```

### 2. Automations Trigger Workflows
In automation JSON:
```json
{
  "type": "trigger-workflow",
  "config": {
    "workflow_id": "wfQULHNKGs"
  }
}
```

**Relationship:**
- Workflows define the human process
- Automations handle the automated tasks within that process
- Workflow steps can invoke automations
- Automations can start workflows

---

## 8. Blueprint Integration

Automations are packaged in blueprints as resources:

```json
{
  "type": "automation_flow",
  "id": "50db4e7e-5ffa-46d1-b6c6-2b38f52e5326",
  "name": "Hausanschluss - E-Mailversand...",
  "parent_resource_ids": ["workflow_id"],
  "impact_on_install": ["create"]
}
```

The "Hausanschluss Kombi" blueprint contains:
- 1 workflow definition
- Multiple automation flows for that workflow
- Journey forms
- Email templates
- Products and pricing

All work together as a complete solution.

---

## 9. Automation Execution Flow

```
1. Event Occurs
   ↓
2. Trigger Evaluates (matches criteria?)
   ↓
3. Actions Execute (in sequence)
   │
   ├─ Action 1: map-entity
   │  (Creates/updates entity)
   │
   ├─ Action 2: cart-checkout
   │  (Processes order)
   │
   ├─ Action 3: send-email
   │  (Sends notification)
   │
   └─ Action 4: trigger-workflow
      (Starts process)
```

**Key Characteristics:**
- Executes immediately when triggered
- Actions run sequentially
- Can pass data between actions
- Error handling per action
- Execution history tracked

---

## 10. Practical Examples from Your System

### Example 1: House Connection Request Automation
**Trigger:** Journey submission (customer fills form)
**Actions:**
1. Map journey data → opportunity entity
2. Checkout cart (selected connection types)
3. Send confirmation email to customer
4. Send notification email to team
5. Trigger "Hausanschluss" workflow

### Example 2: Site Visit Email Automation
**Trigger:** Manual (user clicks in workflow step)
**Action:**
1. Send email template for site visit scheduling

**Referenced in Workflow:** Step "Vor-Ort-Termin vereinbaren"
```json
{
  "automationConfig": {
    "flowId": "50db4e7e-5ffa-46d1-b6c6-2b38f52e5326"
  }
}
```

### Example 3: Status Change Automation
**Trigger:** Entity operation (opportunity status updated)
**Action:**
1. Trigger next workflow phase

---

## 11. Best Practices Observed

### Good Practices:
1. **Clear separation**: Automations handle automated tasks, workflows handle human tasks
2. **Reusability**: Manual-trigger automations reused across workflows
3. **Email templates**: Centralized email templates referenced by ID
4. **Sequential actions**: Logical ordering (create entity → process order → send email)

### Improvement Opportunities:
1. **Naming**: 40+ "Untitled" automations make management difficult
2. **Documentation**: Add descriptions to explain automation purpose
3. **Organization**: Tag or categorize automations by process area

---

## 12. How to Work with Automations

### Export All Automations
```bash
python scripts/automations/export_automations.py
# Saves to: data/output/automations_{timestamp}/
```

### View Automation Details
```bash
cat data/output/automations_*/automation_<ID>.json | jq
```

### Find Automations by Trigger Type
```bash
cat data/output/automations_*/automations_summary.json | jq '.automations[] | select(.trigger_types[] == "journey_submission")'
```

### Find Automations by Action Type
```bash
cat data/output/automations_*/automations_summary.json | jq '.automations[] | select(.action_types[] == "send-email")'
```

---

## Summary

**Automations are the glue** between different parts of your Epilot system:

- **Trigger on events**: Journey submissions, entity changes, manual invocation
- **Execute actions**: Create entities, send emails, generate documents, start workflows
- **Integrate systems**: Connect journeys → entities → workflows → emails
- **Automate repetitive tasks**: No human intervention needed once configured

**The Power Combination:**
1. **Journeys** collect data from customers
2. **Automations** process that data and trigger actions
3. **Workflows** guide humans through the business process
4. **Blueprints** package it all together for deployment

Your 42 automations primarily handle journey-to-entity conversion and email notifications, forming the automated backbone of your house connection and installer management processes.
