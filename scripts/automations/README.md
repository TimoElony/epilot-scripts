# Automation Scripts Documentation

This directory contains scripts and documentation for Epilot automation flow management.

## 📁 Directory Structure

```
scripts/automations/
├── docs/                          # Documentation (version controlled)
│   ├── OPPORTUNITY_WORKFLOW_AUTOMATION_GUIDE.md
│   └── AUTOMATION_ANALYSIS.md
│
├── output/                        # Generated automation JSONs (gitignored)
│   ├── automation_ausbau_*.json
│   ├── automation_tarifabschluss_*.json
│   └── automation_*_updated.json
│
├── create_ausbau_automations.py
├── export_automations.py
└── README.md (this file)
```

## 📚 Available Documentation

### Automation Guides
- **OPPORTUNITY_WORKFLOW_AUTOMATION_GUIDE.md** - How opportunities trigger workflows
- **AUTOMATION_ANALYSIS.md** - Analysis of all 40+ automations in system

## 🚀 Scripts

### create_ausbau_automations.py
Creates supporting automations for Ausbau Glasfaser workflow.

```bash
python scripts/automations/create_ausbau_automations.py
```

**Creates 4 automations:**
1. Step completed notification
2. Approval reminder
3. Update opportunity phase
4. Customer availability notification

### export_automations.py
Exports all automation flows from Epilot to JSON files.

```bash
python scripts/automations/export_automations.py
```

## 📊 Output Files

The `output/` directory contains generated JSON files:
- Automation flow definitions
- Updated automation configurations
- Support automation configs

**Note:** This directory is gitignored as it contains dynamic API responses.

## 🔑 Key Concepts

### Automation Flows
Event-driven processes that automatically execute actions when triggered.

### Trigger Types
1. **journey_submission** - When customer submits a journey form
2. **entity_operation** - When entity is created/updated/deleted
3. **entity_manual** - Manually triggered by user

### Action Types
1. **map-entity** - Create or update entities
2. **trigger-workflow** - Start a workflow process
3. **send-email** - Send notification emails
4. **cart-checkout** - Process orders
5. **create-document** - Generate PDFs

### Common Patterns

#### Pattern 1: Journey → Entity → Workflow
```
Journey submission
  ↓
Create entities (contact, opportunity, order)
  ↓
Trigger workflow
  ↓
Send confirmation emails
```

#### Pattern 2: Status Change → Workflow
```
Entity status changes (e.g., opportunity → "bearbeitung")
  ↓
Check conditions
  ↓
Trigger workflow
  ↓
Notify team
```

## 📝 Automation Examples

### Tarifabschluss Journey Automation
**Triggers:** Journey submission (Tarifabschluss)  
**Actions:**
1. Create contacts
2. Process cart checkout (order)
3. Create opportunity
4. **Start fulfillment workflow** ← Ensures guided process

### Ausbau Glasfaser Automations
**Purpose:** Support fiber expansion workflow  
**Includes:**
- Step completion notifications
- Approval reminders
- Opportunity status updates
- Customer availability notifications

## 🎯 Best Practices

1. **Use descriptive names** - Clear automation flow names
2. **Add conditions** - Filter when actions execute
3. **Handle failures** - Set `allow_failure` appropriately
4. **Test thoroughly** - Verify with test entities first
5. **Document purpose** - Clear descriptions in configs

## 🔗 Integration Points

### With Journeys
- Automations process journey submissions
- Create entities from form data
- Trigger post-submission workflows

### With Workflows
- Automations start workflows automatically
- Notify on workflow events
- Update entity status based on workflow progress

### With Entities
- React to entity changes (CRUD operations)
- Update related entities
- Maintain data consistency

## 📖 Further Reading

See documentation in `docs/` directory for:
- Complete automation architecture guide
- Opportunity → Workflow patterns
- Hausanschluss automation analysis
- Conditional logic examples
- API endpoint reference

## 🔍 Finding Automations

### In Epilot Portal
```
https://portal.epilot.cloud/app/automations
```

### Via API
```bash
curl -X GET \
  https://automation.sls.epilot.io/v1/automation/flows \
  -H "Authorization: Bearer $EPILOT_API_TOKEN"
```

### In This Repo
```bash
# Export all automations
python scripts/automations/export_automations.py

# Check output
ls scripts/automations/output/
```

---

**Last Updated:** 2025-12-03  
**Maintained by:** Epilot Integration Team
