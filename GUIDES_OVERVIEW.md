# Learning Guides - Quick Reference

This repository contains **5 comprehensive learning guides** to take you from TypeScript/React developer to Python/DevOps engineer.

## 📚 Available Guides

| Guide | Focus | Time | Difficulty | Start When |
|-------|-------|------|-----------|------------|
| [PYTHON_LEARNING_GUIDE.md](./PYTHON_LEARNING_GUIDE.md) | Python for TS devs | 3-4 weeks | ⭐⭐ | **Now** |
| [DEVOPS_LEARNING_GUIDE.md](./DEVOPS_LEARNING_GUIDE.md) | CI/CD & deployment | 3-4 weeks | ⭐⭐⭐ | After Python basics |
| [TERRAFORM_GUIDE.md](./TERRAFORM_GUIDE.md) | Infrastructure as Code | 2-3 weeks | ⭐⭐⭐⭐ | After DevOps basics |
| [DOCKER_GUIDE.md](./DOCKER_GUIDE.md) | Containerization | 2 weeks | ⭐⭐⭐ | Parallel with DevOps |
| [MONITORING_GUIDE.md](./MONITORING_GUIDE.md) | Observability & ops | 2-3 weeks | ⭐⭐⭐ | When in production |

## 🗺️ How to Use These Guides

### Option 1: Full Roadmap (16 weeks)
**Best for:** Mastering everything, managing 10+ customers

Follow [LEARNING_ROADMAP.md](./LEARNING_ROADMAP.md) for complete 16-week curriculum.

### Option 2: Quick Start (4 weeks)
**Best for:** Getting productive fast, 1-2 customers

1. **Week 1-2:** Python basics only (PYTHON_LEARNING_GUIDE.md)
2. **Week 3:** Basic CI/CD (DEVOPS_LEARNING_GUIDE.md sections 1-3)
3. **Week 4:** Logging (MONITORING_GUIDE.md sections 1-3)

### Option 3: À la Carte
**Best for:** Specific skills as needed

Pick individual guides based on immediate needs:
- Need to modify Python scripts? → PYTHON_LEARNING_GUIDE.md
- Need to automate deployments? → DEVOPS_LEARNING_GUIDE.md
- Need to manage many customers? → TERRAFORM_GUIDE.md
- Need containers? → DOCKER_GUIDE.md
- Need production monitoring? → MONITORING_GUIDE.md

## 📖 What's In Each Guide

### PYTHON_LEARNING_GUIDE.md
**Perfect if:** You know TypeScript, new to Python

**Covers:**
- Python vs TypeScript comparison
- Async/await (same as TS!)
- Type hints (TS annotations transfer)
- List comprehensions (Python superpower)
- Dataclasses (better than TS interfaces)
- Context managers (new concept)
- Generators & yield

**Special feature:** Side-by-side code comparisons using YOUR sinai-app code

### DEVOPS_LEARNING_GUIDE.md
**Perfect if:** You push code and hope it works

**Covers:**
- CI/CD fundamentals
- GitHub Actions setup
- Environment management (dev/staging/prod)
- Secrets management
- Deployment strategies
- Rollback procedures
- Multi-environment configuration

**Includes:** Complete GitHub Actions workflow file

### TERRAFORM_GUIDE.md
**Perfect if:** Managing workflows manually feels tedious

**Covers:**
- What is IaC?
- Terraform basics
- Epilot blueprints as code
- Multi-customer deployment
- State management
- Terraform vs Python scripts
- When to use which

**Special feature:** Blueprints are Epilot's built-in IaC - learn both!

### DOCKER_GUIDE.md
**Perfect if:** "Works on my machine" problems

**Covers:**
- Containerization basics
- Dockerfile for Python
- Multi-stage builds
- Docker Compose for dev
- CI/CD with Docker
- Production deployment
- Security best practices

**Includes:** Complete Dockerfile and docker-compose.yml

### MONITORING_GUIDE.md
**Perfect if:** Things break and you don't know why

**Covers:**
- The 3 pillars (logs, metrics, traces)
- Structured logging
- Prometheus & Grafana
- OpenTelemetry tracing
- Error tracking (Sentry)
- Alerting strategies
- Epilot-specific monitoring

**Includes:** Complete observability stack configuration

## 🎯 Choose Your Learning Path

### Path: "I just need Python"
```
Read: PYTHON_LEARNING_GUIDE.md
Time: 2-4 weeks
Result: Can modify and create Python scripts
```

### Path: "I need to deploy safely"
```
Read: PYTHON_LEARNING_GUIDE.md → DEVOPS_LEARNING_GUIDE.md → DOCKER_GUIDE.md
Time: 6-8 weeks
Result: Automated testing, safe deployments, containerized apps
```

### Path: "I'm managing multiple customers"
```
Read: All guides in order
Time: 12-16 weeks
Result: Full DevOps engineer, scale to dozens of customers
```

## 🚀 Quick Start (Next 30 Minutes)

1. **Read:** [LEARNING_ROADMAP.md](./LEARNING_ROADMAP.md) (10 min)
   - Understand the big picture
   - Choose your path

2. **Skim:** [PYTHON_LEARNING_GUIDE.md](./PYTHON_LEARNING_GUIDE.md) introduction (5 min)
   - See how Python compares to TypeScript
   - Realize 80% transfers

3. **Do:** Run one Python script (10 min)
   ```bash
   cd /home/timoe/epilot-scripts
   source env/bin/activate
   python scripts/utilities/list_all_apis.py
   ```

4. **Modify:** Change something in that script (5 min)
   - Add a print statement
   - Change a variable
   - See your change work

**Congrats! You just did Python development! 🎉**

## 📊 Learning Time Investment

| Skill Level | Time Required | Guides Needed |
|-------------|---------------|---------------|
| **Basic** - Can read/modify code | 20-30 hours | Python guide only |
| **Competent** - Can build features | 50-60 hours | Python + DevOps |
| **Proficient** - Can architect systems | 80-100 hours | All guides |
| **Expert** - Can teach others | 150+ hours | All + experience |

## 🎓 By the Numbers

**Total content:**
- **5 guides**
- **~15,000 words** of documentation
- **50+ code examples**
- **25+ exercises**
- **92 hours** of learning material

**What you get:**
- Python programming
- CI/CD pipelines
- Infrastructure as code
- Containerization
- Production monitoring
- Multi-customer management
- Professional DevOps skills

## 💡 Pro Tips

1. **Don't read sequentially** - Jump to what you need
2. **Do the exercises** - Reading alone doesn't work
3. **Compare to what you know** - Use your TS experience
4. **Break things safely** - Test environments exist for this
5. **Document as you learn** - Future you will thank you

## 🆘 When You're Stuck

**First:** Search within the guides (Ctrl+F is your friend)

**Then:** Check these sections:
- Python issues? → PYTHON_LEARNING_GUIDE.md "Troubleshooting"
- Deployment issues? → DEVOPS_LEARNING_GUIDE.md "Rollback Procedures"
- Terraform questions? → TERRAFORM_GUIDE.md "Best Practices"
- Container problems? → DOCKER_GUIDE.md "Cheat Sheet"
- Production issues? → MONITORING_GUIDE.md "Debugging"

**Still stuck?** Ask with:
- What you're trying to do
- What you expected
- What actually happened
- Error messages (full text)
- What you've already tried

## 🌟 Success Stories

**After 2 weeks:** "I can modify Python scripts confidently"  
**After 1 month:** "I set up automated testing with GitHub Actions"  
**After 2 months:** "I deployed my first workflow via Docker"  
**After 3 months:** "I'm managing 5 Stadtwerke customers with Terraform"  
**After 4 months:** "I'm teaching my team DevOps practices"

## 📅 Recommended Schedule

**Part-time (5 hours/week):**
- Month 1-2: Python
- Month 3-4: DevOps + Docker
- Month 5-6: Terraform
- Month 7: Monitoring

**Full-time (40 hours/week):**
- Week 1-2: Python
- Week 3-4: DevOps + Docker
- Week 5-6: Terraform
- Week 7-8: Monitoring

## 🎯 Next Step

**Right now, open:** [PYTHON_LEARNING_GUIDE.md](./PYTHON_LEARNING_GUIDE.md)

**Start reading:** Section 1 - "Python Learning Guide: Using This Repository"

**Time required:** 10 minutes to understand the approach

**After that:** Do Exercise 1 (30 minutes)

---

## 📋 Full Table of Contents

### PYTHON_LEARNING_GUIDE.md
1. Python Learning Guide Overview
2. What You're Already Using
3. What You Can Learn
4. Learning Path
5. Exercises
6. Resources
7. Assessment

### DEVOPS_LEARNING_GUIDE.md
1. DevOps Fundamentals
2. CI/CD Pipelines
3. GitHub Actions
4. Environment Management
5. Secrets & Security
6. Deployment Strategies
7. Monitoring & Logging
8. Rollback Procedures

### TERRAFORM_GUIDE.md
1. What is Terraform?
2. Why Use Terraform for Epilot?
3. Epilot Blueprints Explained
4. Terraform vs Python Scripts
5. Terraform Basics
6. Managing Epilot Resources
7. Blueprint-as-Code Pattern
8. Multi-Customer Deployment
9. State Management
10. Practical Examples

### DOCKER_GUIDE.md
1. What is Docker?
2. Why Docker for This Repo?
3. Docker Basics
4. Dockerizing Python Scripts
5. Multi-Stage Builds
6. Docker Compose
7. CI/CD with Docker
8. Production Deployment

### MONITORING_GUIDE.md
1. Observability Fundamentals
2. The Three Pillars
3. Structured Logging
4. Metrics & Dashboards
5. Tracing & Performance
6. Error Tracking
7. Alerting Strategies
8. Epilot-Specific Monitoring

### LEARNING_ROADMAP.md
- Complete learning path
- Phase-by-phase breakdown
- Time estimates
- Progress tracking
- Success metrics

---

**You've got this! Start with Python, build from there. 🚀**
