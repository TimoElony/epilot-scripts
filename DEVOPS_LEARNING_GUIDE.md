# DevOps Learning Guide: CI/CD for Epilot Platform

**Target Audience:** TypeScript/React developer (you!) learning DevOps practices  
**Context:** Managing Epilot workflows, automations, and blueprints across multiple Stadtwerke customers  
**Your Level:** Strong in frontend, new to infrastructure & deployment automation

---

## Table of Contents

1. [DevOps Fundamentals](#1-devops-fundamentals)
2. [CI/CD Pipelines](#2-cicd-pipelines)
3. [GitHub Actions for This Repo](#3-github-actions-for-this-repo)
4. [Environment Management](#4-environment-management)
5. [Secrets & Security](#5-secrets--security)
6. [Deployment Strategies](#6-deployment-strategies)
7. [Monitoring & Logging](#7-monitoring--logging)
8. [Rollback Procedures](#8-rollback-procedures)

---

## 1. DevOps Fundamentals

### What is DevOps? (For Frontend Developers)

**Your mental model (Frontend):**
```
Write code → Git push → Vercel/Netlify auto-deploys → Live
```

**DevOps extends this to backend/infrastructure:**
```
Write code → Git push → Tests run → Build → Deploy to staging → Manual approval → Deploy to prod
```

### Key DevOps Concepts

| Concept | Your TS/React Equivalent | Example in This Repo |
|---------|-------------------------|---------------------|
| **CI (Continuous Integration)** | ESLint on commit, PR checks | Pytest runs on every push |
| **CD (Continuous Deployment)** | Vercel auto-deploy | Deploy workflows to Epilot on merge |
| **Infrastructure as Code** | Terraform config files | Workflow JSON definitions |
| **Environment Variables** | `.env` files, Vite config | `EPILOT_TOKEN`, `EPILOT_ORG_ID` |
| **Secrets Management** | GitHub Secrets | API tokens stored securely |
| **Build Artifacts** | `dist/` folder from Vite | Exported workflow/automation JSON |
| **Deployment Stages** | dev/preview/production | Staging Epilot org → Production org |

---

## 2. CI/CD Pipelines

### What Runs When You Push Code?

```
┌─────────────────────────────────────────────────────────────┐
│ Developer pushes code to GitHub                              │
└────────────────┬────────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────────┐
│ STAGE 1: Code Quality Checks (runs in parallel)             │
├─────────────────────────────────────────────────────────────┤
│ ✓ Linting (flake8)        - Check code style               │
│ ✓ Type checking (mypy)    - Verify type hints              │
│ ✓ Security scan (bandit)  - Find vulnerabilities           │
│ ✓ Format check (black)    - Ensure consistent formatting   │
└────────────────┬────────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────────┐
│ STAGE 2: Tests (runs after quality checks pass)             │
├─────────────────────────────────────────────────────────────┤
│ ✓ Unit tests              - Test individual functions      │
│ ✓ Integration tests       - Test API client                │
│ ✓ Coverage report         - Ensure 80%+ coverage           │
└────────────────┬────────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────────┐
│ STAGE 3: Build & Validate                                   │
├─────────────────────────────────────────────────────────────┤
│ ✓ Syntax validation       - All Python files compile       │
│ ✓ Dependency check        - requirements.txt is valid      │
│ ✓ Documentation exists    - READMEs are present            │
└────────────────┬────────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────────┐
│ STAGE 4: Deploy to Staging (main branch only)               │
├─────────────────────────────────────────────────────────────┤
│ ✓ Export workflows        - scripts/workflows/export*      │
│ ✓ Deploy to test org      - Epilot staging organization    │
│ ✓ Run smoke tests         - Basic workflow creation        │
└────────────────┬────────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────────┐
│ STAGE 5: Deploy to Production (manual approval)             │
├─────────────────────────────────────────────────────────────┤
│ ⏸  Manual approval        - Click "Approve" in GitHub      │
│ ✓ Deploy to prod org      - Epilot production org          │
│ ✓ Verify deployment       - Check workflow IDs created     │
│ ✓ Create git tag          - Mark successful deployment     │
└─────────────────────────────────────────────────────────────┘
```

### Your sinai-app CI/CD (for comparison)

```typescript
// You probably have this pattern with Vercel/Netlify:
git push → Build React app → Deploy to preview URL → Merge to main → Deploy to production URL
```

**This repo does similar, but for Epilot API resources instead of web pages.**

---

## 3. GitHub Actions for This Repo

### Example Pipeline File

See the GitHub Actions workflow configuration below. This would live in `.github/workflows/ci.yml`:

```yaml
# GitHub Actions CI/CD Pipeline for Epilot Scripts
# This file would go in: .github/workflows/ci.yml

name: CI/CD Pipeline

on:
  push:
    branches: [ main, master, develop ]
  pull_request:
    branches: [ main, master ]

jobs:
  # Job 1: Test Python code
  test:
    runs-on: ubuntu-latest
    
    steps:
    - name: Checkout code
      uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
    
    - name: Cache dependencies
      uses: actions/cache@v3
      with:
        path: ~/.cache/pip
        key: ${{ runner.os }}-pip-${{ hashFiles('requirements.txt') }}
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        pip install pytest pytest-cov pytest-asyncio mypy black flake8
    
    - name: Run linting (flake8)
      run: |
        flake8 lib/ scripts/ --count --select=E9,F63,F7,F82 --show-source --statistics
    
    - name: Run type checking (mypy)
      run: |
        mypy lib/ --ignore-missing-imports
    
    - name: Run tests with coverage
      run: |
        pytest tests/ --cov=lib --cov-report=xml --cov-report=term
      env:
        EPILOT_ORG_ID: "test-org"
        EPILOT_TOKEN: "test-token"
    
    - name: Upload coverage to Codecov
      uses: codecov/codecov-action@v3
      with:
        file: ./coverage.xml

  # Job 2: Deploy to staging (only on main branch)
  deploy-staging:
    runs-on: ubuntu-latest
    needs: [test]
    if: github.ref == 'refs/heads/main'
    
    steps:
    - name: Deploy workflows to Epilot staging
      run: |
        python scripts/deploy_all_workflows.py --env staging
      env:
        EPILOT_TOKEN: ${{ secrets.EPILOT_STAGING_TOKEN }}
        EPILOT_ORG_ID: ${{ secrets.EPILOT_STAGING_ORG_ID }}
```

### Understanding GitHub Actions Syntax

**For TypeScript developers:**

```yaml
# YAML is like JSON but with indentation instead of braces
jobs:
  test:              # Like: const test = {
    runs-on: ubuntu-latest
    steps:           # Like: steps: [
      - name: Test   #   { name: "Test", ... }
        run: pytest  # ]
```

**Key concepts:**

| GitHub Actions Term | Your Mental Model | Example |
|-------------------|------------------|---------|
| **Workflow** | Entire CI/CD pipeline | `.github/workflows/ci.yml` |
| **Job** | Independent task (can run parallel) | `test`, `deploy`, `build` |
| **Step** | Single command in a job | `pip install`, `pytest` |
| **Runner** | Virtual machine that runs jobs | `ubuntu-latest`, `windows-latest` |
| **Action** | Reusable component | `actions/checkout@v3` |
| **Secret** | Encrypted environment variable | `${{ secrets.EPILOT_TOKEN }}` |

---

## 4. Environment Management

### Multiple Environments Pattern

```
Development (Local)
    │
    ├─ Your laptop
    ├─ Test data only
    └─ Epilot organization: "Dev" or personal

Staging (Pre-production)
    │
    ├─ GitHub Actions runner
    ├─ Mirror of production
    └─ Epilot organization: "Stadtwerke Wülfrath - Staging"

Production (Live)
    │
    ├─ Manual deployment
    ├─ Real customer data
    └─ Epilot organization: "Stadtwerke Wülfrath" (20000382)
```

### Environment Variables Pattern

```python
# config/epilot_config.py (enhanced for multiple environments)

import os
from typing import Literal

Environment = Literal["development", "staging", "production"]

ENVIRONMENTS = {
    "development": {
        "org_id": "dev-org",
        "api_base": "https://entity.sls.epilot.io/v1",
        "token_env_var": "EPILOT_DEV_TOKEN"
    },
    "staging": {
        "org_id": os.getenv("EPILOT_STAGING_ORG_ID"),
        "api_base": "https://entity.sls.epilot.io/v1",
        "token_env_var": "EPILOT_STAGING_TOKEN"
    },
    "production": {
        "org_id": "20000382",  # Real Stadtwerke Wülfrath
        "api_base": "https://entity.sls.epilot.io/v1",
        "token_env_var": "EPILOT_PROD_TOKEN"
    }
}

def get_config(env: Environment) -> dict:
    """Get configuration for specific environment."""
    config = ENVIRONMENTS[env]
    config["token"] = os.getenv(config["token_env_var"])
    
    if not config["token"]:
        raise ValueError(f"Missing token for {env} environment")
    
    return config
```

**Usage in scripts:**

```python
# scripts/workflows/create_tarifabschluss_fulfillment.py
import sys
from config.epilot_config import get_config

# Read from CLI argument or default to development
env = sys.argv[1] if len(sys.argv) > 1 else "development"
config = get_config(env)

client = EpilotClient(config["token"], config["org_id"])
```

---

## 5. Secrets & Security

### Never Commit Secrets!

**❌ BAD (your sinai-app might have this pattern):**
```typescript
// Don't do this!
const API_KEY = "sk-1234567890abcdef";
```

**✅ GOOD:**
```python
import os
API_KEY = os.getenv("EPILOT_TOKEN")
```

### Setting Up GitHub Secrets

1. **Go to GitHub repo → Settings → Secrets and variables → Actions**

2. **Add secrets:**
   ```
   Name: EPILOT_STAGING_TOKEN
   Value: Bearer eyJ0eXAiOiJKV1...

   Name: EPILOT_STAGING_ORG_ID
   Value: 20000382

   Name: EPILOT_PROD_TOKEN
   Value: Bearer eyJ0eXAiOiJKV1...

   Name: EPILOT_PROD_ORG_ID
   Value: 20000382
   ```

3. **Use in workflow:**
   ```yaml
   - name: Deploy
     env:
       EPILOT_TOKEN: ${{ secrets.EPILOT_PROD_TOKEN }}
     run: python scripts/deploy.py
   ```

### Local Development (.env file)

```bash
# .env (add to .gitignore!)
EPILOT_TOKEN=Bearer eyJ0eXAiOiJKV1QiLCJhbGc...
EPILOT_ORG_ID=20000382

# For multiple environments
EPILOT_DEV_TOKEN=Bearer xxx...
EPILOT_STAGING_TOKEN=Bearer yyy...
EPILOT_PROD_TOKEN=Bearer zzz...
```

**Load in Python:**
```python
from dotenv import load_dotenv
load_dotenv()  # Reads .env file into os.environ
```

---

## 6. Deployment Strategies

### Strategy 1: Blue-Green Deployment

```
Production (Blue)              Staging (Green)
    ↓                               ↓
Running workflows           Test new workflows
v1.0 (current)              v1.1 (candidate)
    ↓                               ↓
Users see this              Nobody sees this yet
    ↓                               ↓
         ← Switch traffic →
                 ↓
         New production (Green becomes Blue)
```

**For Epilot:**
- **Blue**: Stadtwerke Wülfrath production org
- **Green**: Staging org or test org
- **Switch**: Deploy new workflow, update entity references

### Strategy 2: Canary Deployment

```
100% users → Old workflow (wfABC123)
                    ↓
 90% users → Old workflow
 10% users → New workflow (wfXYZ789)  ← Test with small group
                    ↓
  0% users → Old workflow
100% users → New workflow  ← Full rollout
```

**For your Epilot use case:**
1. Deploy new workflow alongside old one
2. Create 10% of new opportunities with new workflow
3. Monitor for errors
4. Gradually increase to 100%
5. Archive old workflow

### Strategy 3: Feature Flags

```python
# Feature flag pattern
ENABLE_NEW_INVOICE_AUTOMATION = os.getenv("FF_NEW_INVOICE", "false") == "true"

if ENABLE_NEW_INVOICE_AUTOMATION:
    automation_id = "new-automation-id"
else:
    automation_id = "old-automation-id"
```

---

## 7. Monitoring & Logging

### What to Monitor

```
┌────────────────────────────────────────┐
│ APPLICATION LEVEL                      │
├────────────────────────────────────────┤
│ ✓ Workflow execution success rate     │
│ ✓ Automation trigger failures          │
│ ✓ API call latency                     │
│ ✓ Error logs from scripts              │
└────────────────────────────────────────┘
         ↓
┌────────────────────────────────────────┐
│ INFRASTRUCTURE LEVEL                   │
├────────────────────────────────────────┤
│ ✓ GitHub Actions run time              │
│ ✓ Deployment success/failure           │
│ ✓ Secret expiration warnings           │
└────────────────────────────────────────┘
```

### Structured Logging Pattern

```python
import logging
import json

# Setup structured logger
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Log workflow creation
logger.info("Workflow created", extra={
    "workflow_id": "wfABC123",
    "workflow_name": "Tarifabschluss",
    "environment": "production",
    "user": "deploy-bot"
})

# Log errors with context
try:
    result = await client.post(url, data)
except Exception as e:
    logger.error("Workflow creation failed", extra={
        "error": str(e),
        "url": url,
        "payload_size": len(json.dumps(data))
    }, exc_info=True)
```

### Monitoring Tools

| Tool | Purpose | Setup Difficulty | Cost |
|------|---------|-----------------|------|
| **GitHub Actions Logs** | CI/CD pipeline monitoring | ⭐ Built-in | Free |
| **Sentry** | Error tracking | ⭐⭐ Easy | Free tier available |
| **Datadog** | Full observability | ⭐⭐⭐⭐ Complex | $$$ |
| **CloudWatch** (if on AWS) | Logs and metrics | ⭐⭐⭐ Medium | $ |
| **Epilot Portal** | Workflow execution tracking | ⭐ Built-in | Included |

**Recommendation for you:** Start with GitHub Actions logs + Sentry for errors.

---

## 8. Rollback Procedures

### Quick Rollback Checklist

```
❌ Something broke in production!

1. ⏸  STOP: Don't deploy anything else
2. 📊 CHECK: What changed? (git log, deployment history)
3. 🔄 ROLLBACK: Revert to last known good version
4. ✅ VERIFY: Test that rollback worked
5. 🔍 DEBUG: Find root cause in safe environment
6. 🐛 FIX: Create fix in staging first
7. 🚀 DEPLOY: Fix to production once verified
```

### Rollback Workflow in Epilot

**Scenario:** New workflow deployed has a bug

```python
# scripts/rollback_workflow.py
import asyncio
from lib.api_client import EpilotClient
from lib.auth import load_env

async def rollback_workflow(old_workflow_id: str, new_workflow_id: str):
    """
    Rollback from new workflow to old workflow.
    
    Strategy:
    1. List all entities using new workflow
    2. Update them to use old workflow
    3. Disable new workflow (don't delete yet - keep for debugging)
    """
    env = load_env()
    client = EpilotClient(env['token'], env['org_id'])
    
    # Find affected entities
    search_url = f"{ENTITY_API}/entity:search"
    result = await client.post(search_url, {
        "q": f"workflow:{new_workflow_id}",
        "hydrate": False
    })
    
    affected_entities = result.get('results', [])
    print(f"Found {len(affected_entities)} entities with new workflow")
    
    # Update each entity
    for entity in affected_entities:
        entity['_schema'] = entity.get('_schema', 'opportunity')
        entity['workflow_id'] = old_workflow_id
        
        update_url = f"{ENTITY_API}/entity/{entity['_schema']}/{entity['_id']}"
        await client.put(update_url, entity)
        print(f"✅ Rolled back entity {entity['_id']}")
    
    # Disable new workflow (keep for investigation)
    workflow_url = f"{WORKFLOW_API}/workflows/{new_workflow_id}"
    await client.put(workflow_url, {
        "enabled": False,
        "name": f"[DISABLED] {workflow_data['name']}"
    })
    
    print(f"✅ Rollback complete. {len(affected_entities)} entities restored.")

# Usage
asyncio.run(rollback_workflow(
    old_workflow_id="wfOLD123",  # Last known good
    new_workflow_id="wfNEW456"   # Broken version
))
```

---

## 9. Practical Exercises

### Exercise 1: Set Up GitHub Actions

1. Create `.github/workflows/test.yml`
2. Add a simple test job
3. Push to GitHub and watch it run
4. Fix any failures

**Time:** 30 minutes  
**Difficulty:** ⭐⭐

### Exercise 2: Multi-Environment Configuration

1. Enhance `config/epilot_config.py` with environment support
2. Create `.env.staging` and `.env.production`
3. Test script in each environment
4. Verify secrets are not in git

**Time:** 45 minutes  
**Difficulty:** ⭐⭐

### Exercise 3: Implement Rollback Script

1. Export current production workflows (backup)
2. Deploy a test workflow to staging
3. Write rollback script to restore old workflow
4. Test rollback in staging

**Time:** 1 hour  
**Difficulty:** ⭐⭐⭐

### Exercise 4: Add Monitoring

1. Set up Sentry account (free tier)
2. Add Sentry SDK to Python scripts
3. Trigger an error intentionally
4. See it appear in Sentry dashboard

**Time:** 30 minutes  
**Difficulty:** ⭐⭐

---

## 10. DevOps Best Practices for This Repo

### Checklist for Production-Ready DevOps

- [ ] **Version Control**
  - [ ] All secrets in `.gitignore`
  - [ ] Git tags for each deployment
  - [ ] Protected main branch (require PR reviews)

- [ ] **Testing**
  - [ ] Unit tests for all API client functions
  - [ ] Integration tests for workflow creation
  - [ ] 80%+ code coverage

- [ ] **CI/CD**
  - [ ] GitHub Actions pipeline configured
  - [ ] Automated tests on every PR
  - [ ] Staging deployment on main branch merge
  - [ ] Manual approval for production

- [ ] **Security**
  - [ ] Secrets stored in GitHub Secrets or AWS Secrets Manager
  - [ ] No API tokens in code
  - [ ] Regular dependency updates (Dependabot)
  - [ ] Security scanning (Bandit, Snyk)

- [ ] **Monitoring**
  - [ ] Structured logging in all scripts
  - [ ] Error tracking (Sentry)
  - [ ] Deployment notifications (Slack/Discord)

- [ ] **Documentation**
  - [ ] Deployment runbook (this guide!)
  - [ ] Rollback procedures documented
  - [ ] Environment setup guide
  - [ ] Troubleshooting guide

---

## 11. Next Steps

**Week 1:**
1. Set up GitHub Actions for automated testing
2. Configure environment variables for staging/production
3. Add structured logging to 3 scripts

**Week 2:**
4. Implement rollback script
5. Set up Sentry error tracking
6. Create deployment documentation

**Week 3:**
7. Test full CI/CD pipeline end-to-end
8. Deploy to staging environment
9. Practice rollback procedure

**Week 4:**
10. Deploy to production with monitoring
11. Set up alerts for failures
12. Document lessons learned

---

## 12. Resources

### Books
- **"The Phoenix Project"** - DevOps novel (entertaining + educational)
- **"Accelerate"** - Research-backed DevOps practices

### Online Courses
- **GitHub Actions Tutorial** - https://docs.github.com/actions
- **AWS DevOps** - https://aws.amazon.com/devops/
- **Docker for Developers** - https://docker-curriculum.com/

### Tools to Learn
1. **GitHub Actions** (CI/CD) - Start here! ⭐
2. **Docker** (Containerization) - Next priority ⭐⭐
3. **Kubernetes** (Orchestration) - Later ⭐⭐⭐⭐
4. **Terraform** (Infrastructure as Code) - See TERRAFORM_GUIDE.md ⭐⭐⭐

### Communities
- **r/devops** - Reddit community
- **DevOps Slack** - https://devopschat.co/
- **GitHub Community** - https://github.community/

---

## Summary: Your DevOps Journey

**Current State:**  
✅ Strong TypeScript/React developer  
✅ Understands git, environment variables, API calls  
❌ New to CI/CD, deployment automation, infrastructure

**After This Guide:**  
✅ Understand CI/CD pipelines  
✅ Can set up GitHub Actions  
✅ Know environment management patterns  
✅ Can deploy safely with rollback procedures  
✅ Ready to learn Terraform (next guide)

**Timeline:**
- **Week 1:** Understand concepts, set up basic pipeline
- **Week 2-3:** Implement full CI/CD for this repo
- **Month 2:** Comfortable with deployments, monitoring
- **Month 3:** Teaching others, contributing to infrastructure

You're already 60% there thanks to your development experience. DevOps is just "development of the deployment process" - it's programming, which you already know! 🚀
