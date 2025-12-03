# Workflow Scripts Documentation

This directory contains scripts and documentation for Epilot workflow management.

## 📁 Directory Structure

```
scripts/workflows/
├── docs/                          # Documentation (version controlled)
│   ├── AUSBAU_GLASFASER_COMPLETE.md
│   ├── TARIFABSCHLUSS_FULFILLMENT_COMPLETE.md
│   ├── TARIFABSCHLUSS_QUICK_ANSWER.md
│   ├── WORKFLOW_EXECUTION_GUIDE.md
│   └── WORKFLOW_QUICK_ANSWERS.md
│
├── output/                        # Generated workflow JSONs (gitignored)
│   ├── workflow_ausbau_*.json
│   ├── workflow_tarifabschluss_*.json
│   └── *_backup_*.json
│
├── create_tarifabschluss_fulfillment.py
├── update_ausbau_glasfaser_workflow.py
├── export_workflows.py
└── README.md (this file)
```

## 📚 Available Documentation

### Workflow Guides
- **WORKFLOW_EXECUTION_GUIDE.md** - Complete guide on starting and using workflows
- **WORKFLOW_QUICK_ANSWERS.md** - Quick reference for common questions

### Ausbau Glasfaser (Fiber Expansion)
- **AUSBAU_GLASFASER_COMPLETE.md** - Complete documentation for fiber expansion workflow
- 5 phases, 22 steps
- Addresses service provider scheduling, product availability, mobile documentation

### Tarifabschluss (Contract Fulfillment)
- **TARIFABSCHLUSS_FULFILLMENT_COMPLETE.md** - Complete fulfillment workflow documentation
- **TARIFABSCHLUSS_QUICK_ANSWER.md** - Quick reference
- 5 phases, 24 steps
- Covers contract processing, technical checks, installation, customer care

## 🚀 Scripts

### create_tarifabschluss_fulfillment.py
Creates comprehensive fulfillment workflow for tariff contracts and updates automation.

```bash
python scripts/workflows/create_tarifabschluss_fulfillment.py
```

### update_ausbau_glasfaser_workflow.py
Updates the Ausbau Glasfaser workflow with comprehensive structure.

```bash
python scripts/workflows/update_ausbau_glasfaser_workflow.py
```

### export_workflows.py
Exports all workflows from Epilot to JSON files.

```bash
python scripts/workflows/export_workflows.py
```

## 📊 Output Files

The `output/` directory contains generated JSON files:
- Workflow definitions (current state)
- Backup files (timestamped)
- Updated workflow versions

**Note:** This directory is gitignored as it contains dynamic API responses.

## 🔑 Key Concepts

### Workflows
Structured processes guiding staff through multi-step operations:
- Contract processing
- Infrastructure projects
- Service fulfillment
- Customer onboarding

### Workflow Structure
- **Phases (SECTION)**: High-level stages (e.g., Planning, Installation)
- **Steps (STEP)**: Individual tasks within phases
- **Approval Gates**: Quality checkpoints (🔒)
- **Mobile Steps**: Field work with real-time documentation (📱)

### Entity Attachment
Workflows can attach to any entity type:
- Opportunities (planning/sales)
- Orders (fulfillment/execution)
- Contacts (onboarding)
- Custom schemas

## 📝 Best Practices

1. **Read documentation first** - Comprehensive guides in `docs/`
2. **Version control** - All docs and scripts are in git
3. **Backup before changes** - Scripts create automatic backups
4. **Test in stages** - Verify each phase before proceeding
5. **Check output** - Review generated JSONs in `output/`

## 🔗 Related Resources

- **Automations**: `../automations/` - Workflow triggers and notifications
- **Demo Scripts**: `../demo/` - Testing and demonstration
- **Entity API**: `../entities/` - Entity creation and management

## 📖 Further Reading

See documentation in `docs/` directory for:
- How to manually start workflows
- Workflow vs entity relationships
- Pain points addressed by each workflow
- Implementation details and API usage
- Success metrics and monitoring

---

**Last Updated:** 2025-12-03  
**Maintained by:** Epilot Integration Team
