# Epilot API Scripts

A simple, organized repository for interacting with Epilot APIs using Python scripts.

## 🚀 Quick Start

### 1. Install Dependencies

```powershell
pip install -r requirements.txt
```

### 2. Configure Authentication

```powershell
# Copy the example env file
copy .env.example .env

# Edit .env and add your Epilot API token
notepad .env
```

Get your API token from: https://portal.epilot.cloud/

### 3. Test Connection

```powershell
python scripts/utilities/test_connection.py
```

### 4. List Available APIs

```powershell
python scripts/utilities/list_all_apis.py
```

## 📁 Repository Structure

```
epilot-scripts/
├── config/                      # Configuration files
│   └── epilot_config.py        # API URLs and settings
│
├── lib/                         # Reusable library code
│   ├── api_client.py           # HTTP client wrapper
│   └── auth.py                 # Authentication helpers
│
├── scripts/                     # Executable scripts
│   ├── entities/               # Entity management
│   │   ├── list_entities.py
│   │   └── create_entity.py
│   │
│   ├── customers/              # Customer operations
│   │   └── import_customers_csv.py
│   │
│   ├── orders/                 # Order management
│   │   └── create_order.py
│   │
│   └── utilities/              # Helper scripts
│       ├── list_all_apis.py
│       └── test_connection.py
│
└── data/                        # Data files
    ├── input/                   # Your CSV/input files
    └── output/                  # Script results
```

## 📝 Usage Examples

### List Entities

```powershell
# List all entities
python scripts/entities/list_entities.py

# Filter by schema
python scripts/entities/list_entities.py --schema contact

# Limit results
python scripts/entities/list_entities.py --limit 10
```

### Create an Entity

```powershell
# Simple entity
python scripts/entities/create_entity.py --schema contact --title "John Doe"

# With additional data
python scripts/entities/create_entity.py --schema product --title "Premium Plan" --data '{\"price\": 99.99}'
```

### Import Customers from CSV

```powershell
# Create a CSV file in data/input/customers.csv
python scripts/customers/import_customers_csv.py data/input/customers.csv
```

CSV format:
```csv
first_name,last_name,email,phone
John,Doe,john@example.com,555-0100
Jane,Smith,jane@example.com,555-0200
```

### Create an Order

```powershell
python scripts/orders/create_order.py --customer-id 12345 --title "New Order" --amount 299.99
```

## 🔧 Adding New Scripts

To add a new script:

1. Choose the appropriate directory (entities, customers, orders, etc.)
2. Create a new `.py` file
3. Follow this template:

```python
#!/usr/bin/env python3
"""
Script Description

Usage:
    python scripts/category/script_name.py
"""

import sys
import asyncio
from pathlib import Path

# Add lib to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from lib.auth import load_env
from lib.api_client import EpilotClient

async def main():
    load_env()
    client = EpilotClient()
    
    # Your code here
    result = await client.get("https://api-url/endpoint")
    print(result)

if __name__ == "__main__":
    asyncio.run(main())
```

## 🌐 Available Epilot APIs

The scripts can interact with all 37+ Epilot APIs:

- **Entity API** - Core data entities
- **Customer API** - Customer management
- **Order API** - Order processing
- **Product API** - Product catalog
- **Pricing API** - Pricing rules
- **Workflow API** - Workflow automation
- **Message API** - Messaging
- **File API** - File storage
- **User API** - User management
- And many more...

Run `python scripts/utilities/list_all_apis.py` to see the complete list.

## 🛠️ Maintenance

### Update Dependencies

```powershell
pip install --upgrade -r requirements.txt
```

### Version Control

This repository is ready for Git:

```powershell
git init
git add .
git commit -m "Initial commit: Epilot API scripts"
```

Your `.env` file is automatically ignored by `.gitignore` to protect your API tokens.

## 💡 Tips

1. **Start Simple**: Use the utility scripts to explore the API
2. **Copy & Modify**: Duplicate existing scripts and adapt them
3. **Use CSV Files**: Place input files in `data/input/`
4. **Check Outputs**: Review results in `data/output/`
5. **Ask Copilot**: Use GitHub Copilot to help create new scripts

## 📚 Resources

- [Epilot API Documentation](https://docs.epilot.io/)
- [Epilot Portal](https://portal.epilot.cloud/)
- [API Specifications](https://docs.epilot.io/openapi-specs/apis.json)

## ⚠️ Security

- **Never commit** your `.env` file
- **Rotate tokens** regularly
- **Use read-only tokens** when possible for testing
- **Review scripts** before running on production data

---

**Built with Python for simplicity and ease of use. Happy scripting! 🐍**
