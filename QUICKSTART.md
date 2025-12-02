# 🚀 Quick Start Guide

## Step 1: Set Up Your Environment

Your Python environment is already configured! Dependencies installed:
- ✅ httpx (HTTP client)
- ✅ python-dotenv (environment variables)

## Step 2: Add Your API Token

```powershell
# Copy the example file
copy .env.example .env

# Open and edit .env
notepad .env
```

Add your Epilot API token (get it from https://portal.epilot.cloud/):
```
EPILOT_API_TOKEN=your_actual_token_here
```

## Step 3: Test Everything Works

```powershell
# Test connection (will validate your token)
python scripts/utilities/test_connection.py

# List all available Epilot APIs
python scripts/utilities/list_all_apis.py
```

## Step 4: Try Your First Script

```powershell
# List entities in your Epilot account
python scripts/entities/list_entities.py

# Create a contact
python scripts/entities/create_entity.py --schema contact --title "Test Contact"
```

## 📝 Common Commands

### Entities
```powershell
# List all entities
python scripts/entities/list_entities.py

# List contacts only
python scripts/entities/list_entities.py --schema contact

# Create a new entity
python scripts/entities/create_entity.py --schema contact --title "John Doe"
```

### Customers (CSV Import)
```powershell
# Create a CSV file: data/input/customers.csv
# Format: first_name,last_name,email,phone

# Import customers
python scripts/customers/import_customers_csv.py data/input/customers.csv
```

### Orders
```powershell
# Create an order
python scripts/orders/create_order.py --customer-id abc123 --title "Order #001" --amount 299.99
```

## 🎯 What You Can Do

1. **Use existing scripts** in `scripts/` folder
2. **Modify them** for your specific needs
3. **Create new scripts** following the same pattern
4. **Process CSV files** from `data/input/`
5. **Ask Copilot** to help create custom scripts

## 💡 Tips

- All scripts use the `lib/` modules for consistency
- Put input files in `data/input/`
- Results are saved to `data/output/`
- Your `.env` file is gitignored for security
- Each script has `--help` for usage info

## 🆘 Need Help?

Ask GitHub Copilot! Examples:
- "Create a script to export all contacts to CSV"
- "Make a script that updates customer phone numbers"
- "How do I search for entities by name?"

---

**You're all set! Start with `test_connection.py` and then explore from there.** 🎉
