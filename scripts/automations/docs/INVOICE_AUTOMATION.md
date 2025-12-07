# First Invoice Automation - Tarifabschluss Workflow

## Overview
Automatically sends invoice email to customers when the "Erste Rechnung erstellen" step is completed in the Tarifabschluss fulfillment workflow.

## Automation Details

**ID:** `76918838-eedd-48ef-8990-ff813a8db4a4`  
**Name:** Tarifabschluss: Erste Rechnung automatisch versenden  
**Status:** ✅ Enabled  
**Workflow:** Tarifabschluss - Vertragserfüllung (`wfc5jpYf0r`)

## Trigger

**Type:** Entity Operation  
**Entity Schema:** `automation_step`  
**Operation:** Update (status change)  
**Conditions:**
- Step ID equals `step-first-invoice`
- Step status equals `DONE`

## Action

**Type:** Send Email  
**Recipients:**
- **To:** Customer email from order (`{{order._relations.contacts.email}}`)
- **CC:** `buchhaltung@stadtwerke-wuelfrath.de`

## Email Content

### Subject
```
Ihre Rechnung von Stadtwerke Wülfrath - {{order._title}}
```

### Key Elements

1. **Invoice Header**
   - Stadtwerke Wülfrath branding
   - Product/tariff name

2. **Invoice Details**
   - Invoice number: `R-{{order._id}}-001`
   - Invoice date (current date)
   - Customer number
   - Contract number
   - Billing period (1 month from delivery date)

3. **Itemized Charges**
   - Product/tariff monthly charge
   - Base fee (Grundgebühr): 9.90 EUR
   - Subtotal
   - VAT (19%)
   - **Total amount with VAT**

4. **Payment Information**
   - Payment method: SEPA direct debit
   - Due date: 14 days from invoice date
   - Auto-debit notification

5. **Customer Portal Link**
   - Link to view invoice online
   - Portal access information

6. **Footer**
   - Contact information
   - Company details
   - Legal information (VAT ID, tax number, etc.)

## Invoice Calculation

```
Subtotal = Product Price + Base Fee
VAT (19%) = Subtotal × 0.19
Total = Subtotal × 1.19
```

**Example:**
- Tariff: 49.90 EUR
- Base fee: 9.90 EUR
- Subtotal: 59.80 EUR
- VAT (19%): 11.36 EUR
- **Total: 71.16 EUR**

## Email Template Features

### Professional Styling
- Branded header with company colors
- Responsive table layout
- Clear typography and spacing
- Action button for portal access

### Dynamic Content
Uses Epilot template variables:
- `{{order.products.name}}` - Product/tariff name
- `{{order.products.price_amount}}` - Monthly price
- `{{order._relations.contacts.email}}` - Customer email
- `{{order.delivery_date}}` - Service start date
- `{{_now | date: 'DD.MM.YYYY'}}` - Current date formatted

### Calculations
- Automatic VAT calculation (19%)
- Date arithmetic for billing period
- Currency formatting

## Usage Flow

```
Tarifabschluss Journey Submitted
    ↓
Order & Opportunity Created
    ↓
Workflow Started (wfc5jpYf0r)
    ↓
... (Steps 1-22) ...
    ↓
Step 23: "Erste Rechnung erstellen"
    ↓
Staff marks step as DONE ✓
    ↓
🤖 AUTOMATION TRIGGERED
    ↓
Email sent to customer
Email CC'd to buchhaltung@stadtwerke-wuelfrath.de
```

## Benefits

✅ **Automatic** - No manual email sending required  
✅ **Consistent** - Professional, branded invoice format every time  
✅ **Timely** - Invoice sent immediately upon completion  
✅ **Trackable** - CC to accounting ensures oversight  
✅ **Customer-friendly** - Includes portal link and payment details  
✅ **Compliant** - Includes all required legal information

## Testing

To test this automation:

1. Start a Tarifabschluss workflow on an order
2. Progress through to step 23 ("Erste Rechnung erstellen")
3. Mark the step as DONE
4. Check customer email and buchhaltung@stadtwerke-wuelfrath.de inbox
5. Verify invoice content and formatting

## Customization

To modify the invoice template:

1. Update the automation via API:
   ```bash
   python scripts/automations/create_invoice_automation.py
   ```

2. Or edit manually in Epilot portal:
   ```
   https://portal.epilot.cloud/app/automations/76918838-eedd-48ef-8990-ff813a8db4a4
   ```

3. Key areas to customize:
   - Email styling (CSS)
   - Invoice line items
   - Company branding
   - Legal footer text
   - Payment terms

## Related Automations

This is the **3rd supporting automation** for Tarifabschluss workflow:

1. ✅ Customer activation notification (step-service-activation)
2. ✅ Staff approval reminders (manual trigger)
3. ✅ **First invoice email** (step-first-invoice) ← **NEW**

## Files

- **Script:** `scripts/automations/create_invoice_automation.py`
- **Output:** `scripts/automations/output/automation_invoice_76918838-eedd-48ef-8990-ff813a8db4a4.json`
- **Documentation:** `scripts/automations/docs/INVOICE_AUTOMATION.md` (this file)

---

**Created:** 2025-12-04  
**Workflow:** Tarifabschluss - Vertragserfüllung  
**Integration:** Epilot Automation API
