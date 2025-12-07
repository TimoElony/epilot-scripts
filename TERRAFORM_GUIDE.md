# Terraform & Infrastructure as Code for Epilot

**Target Audience:** Developer learning Infrastructure as Code (IaC)  
**Context:** Managing Epilot workflows, automations, and blueprints as infrastructure  
**Prerequisites:** Read DEVOPS_LEARNING_GUIDE.md first

---

## Table of Contents

1. [What is Terraform?](#1-what-is-terraform)
2. [Why Use Terraform for Epilot?](#2-why-use-terraform-for-epilot)
3. [Epilot Blueprints Explained](#3-epilot-blueprints-explained)
4. [Terraform vs Python Scripts](#4-terraform-vs-python-scripts)
5. [Terraform Basics](#5-terraform-basics)
6. [Managing Epilot Resources with Terraform](#6-managing-epilot-resources-with-terraform)
7. [Blueprint-as-Code Pattern](#7-blueprint-as-code-pattern)
8. [Multi-Customer Deployment](#8-multi-customer-deployment)
9. [State Management](#9-state-management)
10. [Practical Examples](#10-practical-examples)

---

## 1. What is Terraform?

### Mental Model for Developers

**Your current approach (Python scripts):**
```python
# Imperative: Tell the computer HOW to do it
async def create_workflow():
    # Step 1: Create workflow
    workflow = await client.post("/workflows", workflow_data)
    # Step 2: Create automation
    automation = await client.post("/automations", automation_data)
    # Step 3: Link them together
    await client.put(f"/workflows/{workflow.id}", {"automation_id": automation.id})
```

**Terraform approach (Declarative):**
```hcl
# Declarative: Tell Terraform WHAT you want
resource "epilot_workflow" "tarifabschluss" {
  name = "Tarifabschluss Fulfillment"
  # ... configuration
}

resource "epilot_automation" "invoice" {
  name = "Create Invoice"
  trigger_workflow = epilot_workflow.tarifabschluss.id
  # ... configuration
}
```

**Key difference:** 
- **Imperative (Python):** Execute steps in order, manage state yourself
- **Declarative (Terraform):** Describe desired end state, Terraform figures out how to get there

---

## 2. Why Use Terraform for Epilot?

### Comparison: Python Scripts vs Terraform

| Aspect | Python Scripts (Current) | Terraform (IaC) |
|--------|-------------------------|----------------|
| **Approach** | Imperative (how) | Declarative (what) |
| **State Tracking** | Manual (you track IDs) | Automatic (tfstate file) |
| **Updates** | Write update logic | Change config, run `apply` |
| **Rollback** | Custom rollback scripts | `terraform apply` previous version |
| **Multi-env** | Custom env management | Workspaces built-in |
| **Drift Detection** | Manual comparison | `terraform plan` shows drift |
| **Dependencies** | Manual ordering | Automatic dependency graph |
| **Idempotency** | You implement it | Built-in |

### When to Use Each

**Use Python Scripts (what you have now):**
- ✅ Complex business logic
- ✅ Data transformation
- ✅ One-off migrations
- ✅ Custom validation
- ✅ Demo data generation

**Use Terraform:**
- ✅ Managing infrastructure (workflows, automations, entities)
- ✅ Multi-environment deployments
- ✅ Keeping staging and production in sync
- ✅ Tracking what's deployed where
- ✅ Deploying to multiple Stadtwerke customers

**Best approach: Use BOTH!**
- Terraform manages the infrastructure (workflows, automations)
- Python scripts handle data operations (creating demo opportunities, importing customers)

---

## 3. Epilot Blueprints Explained

### What Are Blueprints?

**Blueprints are Epilot's built-in "Infrastructure as Code" system.**

```
Blueprint (Package)
    ├── Workflows (process definitions)
    ├── Automations (event-driven actions)
    ├── Entity Schemas (data models)
    ├── Journeys (customer portals)
    ├── Email Templates
    └── Configuration (settings)
```

**Example:** "Hausanschluss Kombi" blueprint contains:
- 3 workflows (house connection process)
- 12 automations (notifications, status updates)
- 5 entity schemas (custom data types)
- 2 journeys (customer self-service portals)
- 20+ email templates

### Blueprint Manifest Structure

```json
{
  "id": "blueprint-hausanschluss",
  "version": "2.1.0",
  "name": "Hausanschluss Kombi",
  "description": "Complete house connection workflow for Stadtwerke",
  "resources": [
    {
      "type": "workflow",
      "id": "wf-hausanschluss-main",
      "source": "workflows/hausanschluss.json"
    },
    {
      "type": "automation",
      "id": "auto-welcome-email",
      "source": "automations/welcome.json"
    }
  ],
  "dependencies": {
    "base-crm": "^1.0.0"
  }
}
```

### Your Exported Blueprints

From your `scripts/blueprints/export_blueprints.py`:

```python
# You have access to these blueprint operations:
# GET /v2/blueprint-manifest/blueprints - List all blueprints
# GET /v2/blueprint-manifest/blueprints/{id} - Get blueprint details
# POST /v2/blueprint-manifest/blueprints - Create blueprint
# PUT /v2/blueprint-manifest/blueprints/{id} - Update blueprint
```

---

## 4. Terraform vs Python Scripts

### Your Current Python Workflow

```python
# scripts/workflows/create_tarifabschluss_fulfillment.py
async def main():
    # 1. Define workflow
    workflow_data = {
        "name": "Tarifabschluss",
        "definition_id": "tarifabschluss_v2",
        "flow": [...]  # 800+ lines of definition
    }
    
    # 2. Create it
    result = await client.post(WORKFLOW_API, workflow_data)
    workflow_id = result['id']
    
    # 3. Manually track the ID
    print(f"Created workflow: {workflow_id}")
    # You have to remember: wfc5jpYf0r
```

**Problems:**
- ❌ If you run this twice, you get 2 workflows
- ❌ No record of what's deployed where
- ❌ Updates require custom logic
- ❌ Can't easily see what changed

### Equivalent Terraform Approach

```hcl
# terraform/workflows.tf
resource "epilot_workflow" "tarifabschluss" {
  name          = "Tarifabschluss Fulfillment"
  definition_id = "tarifabschluss_v2"
  
  flow = jsonencode([
    # Same 800+ lines but as HCL or JSON file reference
  ])
}

# Terraform tracks the ID automatically in tfstate
# Output it if you need it elsewhere
output "tarifabschluss_workflow_id" {
  value = epilot_workflow.tarifabschluss.id
}
```

**Benefits:**
- ✅ Run `terraform apply` 100 times = still just 1 workflow
- ✅ Terraform tracks workflow_id in state file
- ✅ Updates: Change config and `terraform apply`
- ✅ `terraform plan` shows exactly what will change

---

## 5. Terraform Basics

### Installation

```bash
# macOS
brew install terraform

# Linux
wget https://releases.hashicorp.com/terraform/1.6.0/terraform_1.6.0_linux_amd64.zip
unzip terraform_1.6.0_linux_amd64.zip
sudo mv terraform /usr/local/bin/

# Verify
terraform version
```

### Core Commands

```bash
# Initialize Terraform (downloads providers)
terraform init

# See what Terraform will do (dry-run)
terraform plan

# Apply changes
terraform apply

# Destroy everything (careful!)
terraform destroy

# Show current state
terraform show

# Format code
terraform fmt

# Validate configuration
terraform validate
```

### Basic Terraform File Structure

```
terraform/
├── main.tf           # Main configuration
├── variables.tf      # Input variables
├── outputs.tf        # Output values
├── providers.tf      # Provider configuration
├── terraform.tfvars  # Variable values (add to .gitignore!)
└── modules/
    ├── workflow/     # Reusable workflow module
    └── automation/   # Reusable automation module
```

### Simple Example

```hcl
# terraform/providers.tf
terraform {
  required_version = ">= 1.0"
  
  required_providers {
    http = {
      source  = "hashicorp/http"
      version = "~> 3.0"
    }
  }
}

# terraform/variables.tf
variable "epilot_token" {
  description = "Epilot API token"
  type        = string
  sensitive   = true
}

variable "epilot_org_id" {
  description = "Epilot organization ID"
  type        = string
}

# terraform/main.tf
locals {
  epilot_api_base = "https://workflows-definition.sls.epilot.io/v1"
}

# Note: This is pseudo-code as there's no official Epilot Terraform provider yet
# You'd need to use the HTTP provider or build a custom provider
```

---

## 6. Managing Epilot Resources with Terraform

### Challenge: No Official Epilot Provider

**Epilot doesn't have an official Terraform provider yet.**

Two approaches:

#### Option 1: HTTP Provider (Quick Start)

```hcl
# Use generic HTTP provider to call Epilot APIs
resource "http" "create_workflow" {
  url    = "https://workflows-definition.sls.epilot.io/v1/workflows"
  method = "POST"
  
  request_headers = {
    Authorization  = "Bearer ${var.epilot_token}"
    Content-Type   = "application/json"
    x-epilot-org-id = var.epilot_org_id
  }
  
  request_body = jsonencode({
    name = "Tarifabschluss Fulfillment"
    # ... rest of workflow definition
  })
}
```

**Limitations:**
- ❌ HTTP provider doesn't track state well
- ❌ Can't detect drift (changes made outside Terraform)
- ❌ Updates are tricky

#### Option 2: Custom Terraform Provider (Better, More Work)

Build a custom Terraform provider for Epilot:

```go
// terraform-provider-epilot/main.go
package main

import (
    "github.com/hashicorp/terraform-plugin-sdk/v2/plugin"
    "github.com/your-org/terraform-provider-epilot/epilot"
)

func main() {
    plugin.Serve(&plugin.ServeOpts{
        ProviderFunc: epilot.Provider,
    })
}
```

**Benefits:**
- ✅ Full Terraform integration
- ✅ State management
- ✅ Drift detection
- ✅ Proper resource lifecycle

**Effort:** ~40 hours to build initial version

#### Option 3: Terraform + Python Hybrid (Recommended for Now)

Use Terraform to orchestrate, Python to execute:

```hcl
# terraform/workflows.tf
resource "null_resource" "tarifabschluss_workflow" {
  triggers = {
    # Re-run if workflow definition changes
    workflow_hash = filemd5("${path.module}/../workflows/tarifabschluss.json")
  }
  
  provisioner "local-exec" {
    command = "python ${path.module}/../scripts/workflows/create_tarifabschluss_fulfillment.py"
    environment = {
      EPILOT_TOKEN  = var.epilot_token
      EPILOT_ORG_ID = var.epilot_org_id
    }
  }
}

# Capture output from Python script
data "external" "workflow_id" {
  depends_on = [null_resource.tarifabschluss_workflow]
  
  program = ["python", "-c", <<-EOT
    import json
    import os
    # Read workflow ID from a file or state
    with open('/tmp/workflow_id.json') as f:
        print(json.dumps(json.load(f)))
  EOT
  ]
}

output "tarifabschluss_id" {
  value = data.external.workflow_id.result.id
}
```

---

## 7. Blueprint-as-Code Pattern

### Creating Blueprints with Terraform

```hcl
# terraform/blueprints/stadtwerke-starter.tf

locals {
  blueprint_manifest = {
    id          = "stadtwerke-starter-kit"
    version     = "1.0.0"
    name        = "Stadtwerke Starter Kit"
    description = "Complete workflow and automation package for Stadtwerke"
    
    resources = [
      {
        type   = "workflow"
        id     = "wf-ausbau-glasfaser"
        source = file("${path.module}/../../workflows/ausbau_glasfaser.json")
      },
      {
        type   = "workflow"
        id     = "wf-tarifabschluss"
        source = file("${path.module}/../../workflows/tarifabschluss.json")
      },
      {
        type   = "automation"
        id     = "auto-invoice"
        source = file("${path.module}/../../automations/invoice.json")
      }
    ]
  }
}

# Deploy blueprint using Python script
resource "null_resource" "deploy_blueprint" {
  triggers = {
    manifest_hash = md5(jsonencode(local.blueprint_manifest))
  }
  
  provisioner "local-exec" {
    command = <<-EOT
      python scripts/blueprints/create_blueprint.py \
        --manifest '${jsonencode(local.blueprint_manifest)}'
    EOT
    
    environment = {
      EPILOT_TOKEN  = var.epilot_token
      EPILOT_ORG_ID = var.epilot_org_id
    }
  }
}
```

### Blueprint Versioning

```hcl
# terraform/variables.tf
variable "blueprint_version" {
  description = "Version of the Stadtwerke blueprint to deploy"
  type        = string
  default     = "1.0.0"
}

# terraform/blueprints.tf
locals {
  blueprints = {
    "1.0.0" = {
      workflows   = ["ausbau_v1", "tarifabschluss_v1"]
      automations = ["invoice_simple"]
    }
    "1.1.0" = {
      workflows   = ["ausbau_v2", "tarifabschluss_v1"]
      automations = ["invoice_simple", "invoice_reminder"]
    }
    "2.0.0" = {
      workflows   = ["ausbau_v2", "tarifabschluss_v2"]
      automations = ["invoice_advanced", "customer_notifications"]
    }
  }
  
  selected_blueprint = local.blueprints[var.blueprint_version]
}
```

---

## 8. Multi-Customer Deployment

### Terraform Workspaces for Multiple Stadtwerke

```bash
# Create workspace for each customer
terraform workspace new stadtwerke-wuelfrath
terraform workspace new stadtwerke-mettmann
terraform workspace new stadtwerke-duesseldorf

# List workspaces
terraform workspace list

# Switch workspace
terraform workspace select stadtwerke-wuelfrath

# Deploy to specific customer
terraform apply -var-file="customers/wuelfrath.tfvars"
```

### Customer-Specific Variables

```hcl
# customers/wuelfrath.tfvars
epilot_org_id     = "20000382"
customer_name     = "Stadtwerke Wülfrath"
blueprint_version = "1.1.0"

workflows_enabled = {
  ausbau_glasfaser = true
  tarifabschluss   = true
  grid_maintenance = false  # Not ready yet
}

custom_branding = {
  primary_color = "#0066CC"
  logo_url      = "https://stadtwerke-wuelfrath.de/logo.png"
}

# customers/mettmann.tfvars
epilot_org_id     = "20000999"
customer_name     = "Stadtwerke Mettmann"
blueprint_version = "2.0.0"  # They want latest

workflows_enabled = {
  ausbau_glasfaser = true
  tarifabschluss   = true
  grid_maintenance = true  # They need this
}
```

### Deployment Script

```bash
#!/bin/bash
# deploy_customer.sh

CUSTOMER=$1
if [ -z "$CUSTOMER" ]; then
    echo "Usage: ./deploy_customer.sh <customer-name>"
    exit 1
fi

# Switch to customer workspace
terraform workspace select "stadtwerke-$CUSTOMER" || terraform workspace new "stadtwerke-$CUSTOMER"

# Deploy
terraform apply -var-file="customers/$CUSTOMER.tfvars" -auto-approve

# Output deployment info
terraform output -json > "deployments/$CUSTOMER-$(date +%Y%m%d).json"
```

---

## 9. State Management

### What is Terraform State?

**terraform.tfstate file tracks what Terraform has created:**

```json
{
  "version": 4,
  "terraform_version": "1.6.0",
  "resources": [
    {
      "type": "null_resource",
      "name": "tarifabschluss_workflow",
      "instances": [
        {
          "attributes": {
            "id": "wfc5jpYf0r",
            "triggers": {
              "workflow_hash": "abc123..."
            }
          }
        }
      ]
    }
  ]
}
```

### Local vs Remote State

**Local state (default):**
```
terraform/
└── terraform.tfstate  ← On your laptop
```

**Problems:**
- ❌ Lost if laptop dies
- ❌ Can't collaborate (no shared state)
- ❌ Contains secrets

**Remote state (recommended):**
```hcl
# terraform/backend.tf
terraform {
  backend "s3" {
    bucket         = "epilot-terraform-state"
    key            = "stadtwerke/terraform.tfstate"
    region         = "eu-central-1"
    encrypt        = true
    dynamodb_table = "terraform-locks"
  }
}
```

**Benefits:**
- ✅ Backed up automatically
- ✅ Team can collaborate
- ✅ State locking (prevents conflicts)
- ✅ Encrypted

### State Management Commands

```bash
# Show current state
terraform state list

# Get details of specific resource
terraform state show null_resource.tarifabschluss_workflow

# Remove resource from state (careful!)
terraform state rm null_resource.old_workflow

# Import existing resource
terraform import null_resource.existing_workflow wfc5jpYf0r

# Pull remote state to local
terraform state pull > backup.tfstate

# Push local state to remote
terraform state push backup.tfstate
```

---

## 10. Practical Examples

### Example 1: Complete Stadtwerke Infrastructure

```hcl
# terraform/main.tf
terraform {
  required_version = ">= 1.0"
  
  backend "s3" {
    bucket = "epilot-terraform-state"
    key    = "stadtwerke/${var.customer_slug}/terraform.tfstate"
    region = "eu-central-1"
  }
}

# Variables
variable "customer_slug" {
  type = string
}

variable "epilot_org_id" {
  type = string
}

variable "epilot_token" {
  type      = string
  sensitive = true
}

variable "workflows_to_deploy" {
  type = map(bool)
  default = {
    ausbau_glasfaser = true
    tarifabschluss   = true
  }
}

# Workflows
module "ausbau_workflow" {
  source = "./modules/workflow"
  count  = var.workflows_to_deploy.ausbau_glasfaser ? 1 : 0
  
  name         = "Ausbau Glasfaser"
  definition   = file("${path.module}/../workflows/ausbau_glasfaser.json")
  epilot_token = var.epilot_token
  epilot_org_id = var.epilot_org_id
}

module "tarifabschluss_workflow" {
  source = "./modules/workflow"
  count  = var.workflows_to_deploy.tarifabschluss ? 1 : 0
  
  name         = "Tarifabschluss Fulfillment"
  definition   = file("${path.module}/../workflows/tarifabschluss.json")
  epilot_token = var.epilot_token
  epilot_org_id = var.epilot_org_id
}

# Automations (depend on workflows)
module "invoice_automation" {
  source = "./modules/automation"
  
  name              = "Create Invoice"
  trigger_workflow  = module.tarifabschluss_workflow[0].workflow_id
  automation_config = file("${path.module}/../automations/invoice.json")
  epilot_token      = var.epilot_token
  epilot_org_id     = var.epilot_org_id
}

# Outputs
output "deployed_workflows" {
  value = {
    ausbau         = try(module.ausbau_workflow[0].workflow_id, null)
    tarifabschluss = try(module.tarifabschluss_workflow[0].workflow_id, null)
  }
}

output "deployed_automations" {
  value = {
    invoice = module.invoice_automation.automation_id
  }
}
```

### Example 2: Reusable Workflow Module

```hcl
# terraform/modules/workflow/main.tf
variable "name" {
  type = string
}

variable "definition" {
  type = string
}

variable "epilot_token" {
  type      = string
  sensitive = true
}

variable "epilot_org_id" {
  type = string
}

# Create workflow using Python script
resource "null_resource" "workflow" {
  triggers = {
    # Re-create if definition changes
    definition_hash = md5(var.definition)
  }
  
  provisioner "local-exec" {
    command = <<-EOT
      python ${path.module}/../../../scripts/workflows/create_workflow_generic.py \
        --name '${var.name}' \
        --definition '${var.definition}'
    EOT
    
    environment = {
      EPILOT_TOKEN  = var.epilot_token
      EPILOT_ORG_ID = var.epilot_org_id
    }
  }
  
  # Store workflow ID
  provisioner "local-exec" {
    when    = destroy
    command = "echo 'Workflow ${self.triggers.workflow_id} deleted'"
  }
}

# Read workflow ID from output file
data "local_file" "workflow_id" {
  depends_on = [null_resource.workflow]
  filename   = "/tmp/workflow_${md5(var.name)}.txt"
}

output "workflow_id" {
  value = trimspace(data.local_file.workflow_id.content)
}
```

### Example 3: Multi-Environment Setup

```hcl
# terraform/environments/dev.tfvars
epilot_org_id      = "dev-org-123"
environment        = "development"
blueprint_version  = "2.0.0-beta"
enable_monitoring  = false

# terraform/environments/staging.tfvars
epilot_org_id      = "staging-org-456"
environment        = "staging"
blueprint_version  = "1.1.0"
enable_monitoring  = true

# terraform/environments/production.tfvars
epilot_org_id      = "20000382"
environment        = "production"
blueprint_version  = "1.1.0"
enable_monitoring  = true
enable_backups     = true

# Deploy to environment
terraform apply -var-file="environments/production.tfvars"
```

---

## 11. Migration Path: Python → Terraform

### Phase 1: Terraform Orchestration (Weeks 1-2)

Keep Python scripts, add Terraform wrapper:

```hcl
# Just wrap existing scripts
resource "null_resource" "deploy_all" {
  provisioner "local-exec" {
    command = "python scripts/workflows/create_tarifabschluss_fulfillment.py"
  }
}
```

### Phase 2: Terraform Modules (Weeks 3-4)

Extract reusable modules:

```hcl
# Reusable modules
module "workflow" {
  source = "./modules/workflow"
  # ...
}
```

### Phase 3: Custom Provider (Months 2-3)

Build Epilot Terraform provider:

```hcl
# Native Terraform resources
resource "epilot_workflow" "tarifabschluss" {
  name = "Tarifabschluss"
  # ...
}
```

**Recommendation:** Start with Phase 1, see if you need Phase 2/3.

---

## 12. Best Practices

### 1. Version Everything

```hcl
# Pin provider versions
terraform {
  required_version = "~> 1.6.0"
  
  required_providers {
    null = {
      source  = "hashicorp/null"
      version = "~> 3.2"
    }
  }
}
```

### 2. Use Modules for Reusability

```
terraform/
├── modules/
│   ├── workflow/
│   ├── automation/
│   └── customer-setup/
└── customers/
    ├── wuelfrath.tf
    └── mettmann.tf
```

### 3. Separate Environments

```bash
# Use workspaces OR separate directories
terraform/
├── dev/
├── staging/
└── production/
```

### 4. Secure Secrets

```hcl
# Never commit secrets!
variable "epilot_token" {
  sensitive = true
  # Set via: export TF_VAR_epilot_token="..."
  # Or use: terraform apply -var="epilot_token=..."
}
```

### 5. Document Infrastructure

```hcl
# Use comments and descriptions
variable "customer_name" {
  description = "Human-readable customer name for Stadtwerke"
  type        = string
  
  validation {
    condition     = can(regex("^Stadtwerke ", var.customer_name))
    error_message = "Customer name must start with 'Stadtwerke '."
  }
}
```

---

## 13. Practical Exercises

### Exercise 1: Set Up Basic Terraform

1. Install Terraform
2. Create `terraform/` directory
3. Write simple `main.tf` that prints "Hello"
4. Run `terraform init` and `terraform apply`

**Time:** 20 minutes  
**Difficulty:** ⭐

### Exercise 2: Wrap Python Script with Terraform

1. Take your `create_tarifabschluss_fulfillment.py`
2. Create Terraform config that runs it
3. Pass environment variables through Terraform
4. Capture output

**Time:** 1 hour  
**Difficulty:** ⭐⭐

### Exercise 3: Create Reusable Module

1. Build workflow module
2. Use it to deploy 2 different workflows
3. Output the workflow IDs
4. Test updates by changing workflow definition

**Time:** 2 hours  
**Difficulty:** ⭐⭐⭐

### Exercise 4: Multi-Customer Deployment

1. Set up workspaces for 2 customers
2. Create customer-specific `.tfvars` files
3. Deploy different blueprint versions to each
4. Verify in Epilot portal

**Time:** 2 hours  
**Difficulty:** ⭐⭐⭐

---

## 14. Terraform for Epilot Blueprints Summary

### Current State (Python Scripts)

```python
# Imperative, manual tracking
python scripts/workflows/create_tarifabschluss_fulfillment.py
# → Creates workflow wfc5jpYf0r
# → You track this ID manually

python scripts/automations/create_invoice_automation.py
# → Creates automation, links to workflow
# → You track automation ID manually
```

### Future State (Terraform)

```bash
# Declarative, automatic tracking
terraform apply
# → Creates/updates workflows
# → Creates/updates automations
# → Links them automatically
# → Tracks all IDs in tfstate
# → Idempotent (safe to re-run)

terraform plan
# → Shows exactly what will change
# → No surprises
```

### Recommended Approach for You

**Phase 1 (Now):** Keep Python scripts, add Terraform orchestration
**Phase 2 (Month 2):** Extract reusable Terraform modules
**Phase 3 (Later):** Consider building custom Epilot provider if managing 10+ customers

**Why?** 
- Your Python scripts work well
- Terraform adds orchestration & state management
- Don't over-engineer too early
- Can always migrate more later

---

## 15. Resources

### Learn Terraform

- **Official Tutorial** - https://learn.hashicorp.com/terraform
- **Terraform Best Practices** - https://www.terraform-best-practices.com/
- **Writing Custom Providers** - https://www.terraform.io/plugin

### Epilot-Specific

- **Blueprint API Docs** - https://docs.epilot.io/api/blueprint
- **Your Export Script** - `scripts/blueprints/export_blueprints.py`
- **Blueprint Examples** - `data/output/blueprints/` (after export)

### Community

- **Terraform Providers Registry** - https://registry.terraform.io/
- **Provider Development** - https://github.com/hashicorp/terraform-plugin-sdk
- **Example Providers** - Search GitHub for "terraform-provider-*"

---

## Summary: Your IaC Journey

**Where You Are:**
✅ Python scripts that work  
✅ Manual deployment process  
✅ Good for 1-2 customers  
❌ Hard to scale to 10+ customers  
❌ No drift detection  
❌ Manual state tracking

**Where Terraform Takes You:**
✅ Declarative infrastructure  
✅ Automatic state management  
✅ Easy multi-customer deployment  
✅ Drift detection built-in  
✅ Rollback is just `git revert + terraform apply`  
✅ Infrastructure changes are code reviews

**Timeline:**
- **Week 1:** Terraform basics, wrap existing scripts
- **Week 2-3:** Extract modules, manage 2-3 customers
- **Month 2:** Comfortable managing 5-10 customers
- **Month 3+:** Could build custom provider if needed

**Bottom Line:** Terraform is "version control for infrastructure." It lets you treat your Epilot workflows/automations/blueprints the same way you treat code in git. 🚀