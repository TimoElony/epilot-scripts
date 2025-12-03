# Quick Answers to Your Questions

**Date:** 2025-12-03

## Q1: How do I manually start a workflow?

### Answer: Two Ways

**1. Via Epilot UI (Easiest):**
- Open any entity (opportunity, order, contact, etc.)
- Click "Start Workflow" button or "Workflows" tab
- Select "Ausbau Glasfaser" from dropdown
- Click "Start"

**2. Via API:**
```bash
POST https://workflows-execution.sls.epilot.io/v1/workflows/executions
{
  "definitionId": "wfQpwhJF6J",
  "entityId": "YOUR_ENTITY_ID_HERE",
  "entitySchema": "opportunity"
}
```

**3. Via Our Script:**
```bash
python scripts/demo/start_workflow_on_opportunity.py
# Will show you all opportunities and let you pick one
```

---

## Q2: How do I put a workflow on other entities (not just opportunities)?

### Answer: Change the entitySchema!

Workflows work on **ANY entity type**. Just change the `entitySchema` parameter:

```python
# On Opportunity
{
  "definitionId": "wfQpwhJF6J",
  "entityId": "opp-123",
  "entitySchema": "opportunity"  # ← This is all you change
}

# On Order
{
  "definitionId": "wfQpwhJF6J",
  "entityId": "order-456",
  "entitySchema": "order"  # ← Now it's on an order
}

# On Contact
{
  "definitionId": "wfQpwhJF6J",
  "entityId": "contact-789",
  "entitySchema": "contact"  # ← Now it's on a contact
}

# On Custom Schema
{
  "definitionId": "wfQpwhJF6J",
  "entityId": "project-abc",
  "entitySchema": "infrastructure_project"  # ← Your custom schema
}
```

**Workflows don't care about entity type!** They just need:
1. A workflow definition (wfQpwhJF6J)
2. An entity to attach to (any ID)
3. The entity's schema type (any schema)

---

## Q3: Should I treat infrastructure extensions as opportunities?

### Answer: Yes, that's totally fine!

**Opportunities are NOT strictly sales-related.** They're just called "opportunities" but you can use them for:

✅ **Sales opportunities** (traditional use)
✅ **Infrastructure projects** (your use case)
✅ **Internal initiatives**
✅ **Planning projects**
✅ **Any "proposed" or "potential" work**

### What Makes an Opportunity?

Think of it as: **"Something we're considering or planning"**

Not necessarily: "Something we're selling to a customer"

### Your Ausbau Glasfaser Projects

**Option 1: Keep them as Opportunities (Simpler)**
```
Opportunity = Infrastructure Expansion Project
- Status "ausstehend" = Planning phase
- Status "bearbeitung" = Active construction
- Status "geschlossen" = Complete
- Run workflow directly on opportunity
```

**Option 2: Opportunity → Order Pattern (More Structured)**
```
Opportunity = Planning & Approval Phase
- Assess feasibility
- Get budget approval
- Status "geschlossen" = Approved

↓ Convert to Order

Order = Execution Phase
- Actual construction work
- Budget tracking
- Run "Ausbau Glasfaser" workflow on order
```

### Recommendation for You

**Use Opportunities directly** because:
1. ✅ Your demo data is already opportunities
2. ✅ Infrastructure projects are internal (not customer sales)
3. ✅ Simpler structure for demos
4. ✅ Still professional and correct usage
5. ✅ You can always add Orders later if needed

**The word "opportunity" is just a label** - Epilot lets you use entities however makes sense for your business!

---

## Real-World Examples

### Stadtwerke Using Opportunities for Infrastructure

**Not a Customer Sale:**
```json
{
  "_schema": "opportunity",
  "_title": "Glasfaser Ausbau Neubaugebiet Nordstraße",
  "status": "bearbeitung",
  "typ": "Infrastructure",
  "beschreibung": "40 neue Glasfaser-Anschlüsse im Neubaugebiet",
  "budget": 45000.00,
  "_tags": ["ausbau", "glasfaser", "wuelfrath"]
}
```
✅ **This is correct usage!**

### Customer-Facing Sale

```json
{
  "_schema": "opportunity",
  "_title": "Glasfaser-Tarif für Familie Müller",
  "status": "bearbeitung",
  "contact": ["kunde-müller-123"],
  "sparten": ["Glasfaser"],
  "_tags": ["tarif", "privatkunde"]
}
```
✅ **This is also correct usage!**

**Same entity type, different business purposes** - both are valid!

---

## Key Insights

### 1. Workflows are Entity-Agnostic
- Work on opportunities, orders, contacts, custom schemas, etc.
- You choose what makes sense for your process
- No technical limitation on entity type

### 2. Opportunities are Flexible
- Not limited to sales
- Use for any planning/potential work
- Internal projects ✅
- Infrastructure ✅
- Sales ✅

### 3. Entity Names are Just Labels
- "Opportunity" doesn't mean "customer sale"
- "Order" doesn't mean "customer order"
- Use entities based on your workflow needs, not name semantics

### 4. Your Current Setup is Fine
- Opportunities for Ausbau projects ✅ Correct!
- Running workflow on opportunities ✅ Works great!
- Treating infrastructure as opportunities ✅ Valid approach!

---

## Try It Now!

**Start workflow on one of your demo opportunities:**

```bash
cd /home/timoe/epilot-scripts
source env/bin/activate
export $(cat .env | xargs)
python scripts/demo/start_workflow_on_opportunity.py
```

This will:
1. Show you all your demo opportunities
2. Let you pick one
3. Start the Ausbau Glasfaser workflow on it
4. Give you the portal link to view it

Then open in browser and see your 22-step workflow attached to the opportunity!

---

## Documentation Created

1. **Complete Guide:** `data/output/WORKFLOW_EXECUTION_GUIDE.md` (5000+ words)
2. **This Quick Answer:** `data/output/WORKFLOW_QUICK_ANSWERS.md`
3. **Working Script:** `scripts/demo/start_workflow_on_opportunity.py`

---

**Bottom Line:**

✅ Workflows work on ANY entity type  
✅ Start workflows via UI or API (it's easy!)  
✅ Opportunities for infrastructure projects is totally fine  
✅ Your current setup is correct - just start using the workflow!
