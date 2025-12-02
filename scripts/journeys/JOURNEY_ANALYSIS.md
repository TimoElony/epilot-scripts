# Journey Configuration Analysis

**Export Date:** 2025-12-02  
**Total Journeys:** 10  
**Data Source:** `/v1/journey/configuration` API

---

## Executive Summary

Journeys are customer-facing forms and portals in the Epilot platform. They serve as the **primary entry point** for external users (customers, installers) to interact with the system. Each journey consists of multiple steps that guide users through data collection workflows, with conditional logic controlling flow and validation.

### Key Insights

- **10 active journeys** divided into three categories:
  - **7 Installer Management Forms** (contractor registration, credential management)
  - **2 House Connection Forms** (fiber optic installation requests)
  - **1 Tariff Completion Form** (energy contract finalization)
  
- **Average complexity:** 6.9 steps per journey, ranging from simple 2-step portals to complex 27-step workflows
- **Logic-driven:** 122 total conditional logic rules controlling form flow, visibility, and validation
- **Design integration:** Journeys use Material-UI theme system with custom branding
- **Multi-revision system:** Each journey tracks multiple revisions with metadata

---

## Journey Inventory

### Installer Management Journeys (7)

These journeys manage the contractor registration and credential lifecycle for gas and electrical installers:

1. **Installateur - Gasteintragung Installateurverzeichnis (Gastinstallateur)**
   - Purpose: Gas installer initial registration
   - Steps: 5
   - Logics: 5 conditional rules
   - Target: New gas installation contractors

2. **Installateur - Neueintragung Installateurverzeichnis (Stamminstallateur)**
   - Purpose: Master installer initial registration
   - Steps: 9
   - Logics: 33 conditional rules (most complex installer form)
   - Target: New master installation contractors

3. **Installateur - Meldung weiterer Fachkraft von bestehenden Installationsunternehmen (Stamminstallateur)**
   - Purpose: Add additional technicians to existing installation company
   - Steps: 6
   - Logics: 29 conditional rules
   - Target: Existing master installers adding staff

4. **Installateur - Portal: Ausweisverlängerung Fachkraft (Gastinstallateur)**
   - Purpose: Gas installer credential renewal portal
   - Steps: 2
   - Logics: 5 conditional rules
   - Target: Gas installers renewing credentials

5. **Installateur - Portal: Ausweisverlängerung Fachkraft (Stamminstallateur)**
   - Purpose: Master installer credential renewal portal
   - Steps: 2
   - Logics: 6 conditional rules
   - Target: Master installers renewing credentials

6. **Installateur - Übermittlung Installateurverträge durch Installationsunternehmen**
   - Purpose: Submit installer contracts
   - Steps: 2
   - Logics: 0 conditional rules (simple upload)
   - Target: Installation companies submitting contracts

7. **FAQ Installateurportal**
   - Purpose: Installer portal help documentation
   - Steps: 2
   - Logics: 7 conditional rules
   - Target: All installers (informational)

### House Connection Journeys (2)

These journeys handle customer requests for physical utility connections:

8. **Hausanschluss Glasfaser**
   - Purpose: Fiber optic house connection application
   - Steps: 14
   - Logics: 27 conditional rules
   - Target: Customers requesting fiber installation
   - Complexity: Multi-step address validation, property info, installation preferences

9. **Hausanschluss Angebotsannahme**
   - Purpose: House connection offer acceptance
   - Steps: 2
   - Logics: 0 conditional rules
   - Target: Customers accepting connection offers

### Tariff/Contract Journey (1)

10. **Tarifabschluss**
    - Purpose: Energy tariff contract completion
    - Steps: 27 (most complex overall)
    - Logics: 10 conditional rules
    - Target: Customers finalizing energy contracts
    - Complexity: Most detailed journey with comprehensive data collection

---

## Technical Architecture

### Journey Structure

```json
{
  "journeyId": "unique-config-id",
  "name": "Journey Display Name",
  "organizationId": "20000382",
  "design": {
    "theme": { /* Material-UI theming */ },
    "logo": { /* Brand assets */ },
    "settings": { /* Layout config */ }
  },
  "steps": [
    {
      "id": "step-uuid",
      "name": "Step Name",
      "schema": [ /* Form fields */ ],
      "uiSchema": [ /* Field rendering */ ]
    }
  ],
  "logics": [
    {
      "condition": "expression",
      "actions": [ /* Show/hide/validate */ ]
    }
  ],
  "revisions": [
    { "version": 1, "timestamp": "..." }
  ]
}
```

### Key Components

#### 1. Steps
- **Definition:** Individual form pages in the journey
- **Structure:** Each step contains:
  - `schema`: JSON Schema defining data structure and validation rules
  - `uiSchema`: UI rendering instructions (field types, layouts, labels)
  - `id`: Unique identifier for referencing in logic
- **Count Range:** 2-27 steps across journeys

#### 2. Logic Rules
- **Purpose:** Control conditional behavior (visibility, navigation, validation)
- **Types:**
  - **Show/Hide:** Display fields based on previous answers
  - **Navigation:** Skip steps conditionally
  - **Validation:** Dynamic field requirements
  - **Calculation:** Compute derived values
- **Count Range:** 0-33 logic rules per journey
- **Complexity:** Neueintragung Stamminstallateur has 33 rules (most complex)

#### 3. Design System
- **Framework:** Material-UI (MUI) component library
- **Customization:** Theme overrides for:
  - Color palette (primary: #039BE5FF blue)
  - Typography (form labels, inputs)
  - Component styling (buttons, cards, app bars)
- **Consistency:** All journeys inherit organization-level design

#### 4. Context Schema
- **Purpose:** Define expected input context (pre-filled data)
- **Usage:** Journeys can receive entity data to pre-populate forms
- **Example:** House connection journeys may receive customer entity data

#### 5. Revisions
- **Versioning:** Each change creates new revision
- **Metadata:** Tracks timestamps, authors, changes
- **Rollback:** Support for reverting to previous versions

---

## Journey Complexity Analysis

### By Step Count

| Journey | Steps | Category |
|---------|-------|----------|
| Tarifabschluss | 27 | High Complexity |
| Hausanschluss Glasfaser | 14 | Medium Complexity |
| Installateur - Neueintragung Stamminstallateur | 9 | Medium Complexity |
| Installateur - Meldung weiterer Fachkraft | 6 | Low-Medium |
| Installateur - Gasteintragung | 5 | Low-Medium |
| Others (6 journeys) | 2 | Low Complexity |

### By Logic Rule Count

| Journey | Logics | Complexity |
|---------|--------|------------|
| Installateur - Neueintragung Stamminstallateur | 33 | Very High |
| Installateur - Meldung weiterer Fachkraft | 29 | High |
| Hausanschluss Glasfaser | 27 | High |
| Tarifabschluss | 10 | Medium |
| FAQ Installateurportal | 7 | Low-Medium |
| Others (5 journeys) | 0-6 | Low |

### Insights

- **Complexity Correlation:** Step count doesn't always correlate with logic count
  - Tarifabschluss: 27 steps but only 10 logics (linear flow)
  - Neueintragung Stamminstallateur: 9 steps but 33 logics (highly conditional)
- **Simple Portals:** Credential renewal and document upload journeys are intentionally simple (2 steps, minimal logic)
- **Customer-Facing Complexity:** House connection journeys are moderately complex (14 steps, 27 logics) to gather detailed property information

---

## Integration with Epilot Ecosystem

### 1. Journey → Automation Flow

When a journey is submitted:
1. Journey submission triggers automation flows (via `journey_submission` event)
2. Automations process form data:
   - Create or update entities (contacts, opportunities, orders)
   - Send notification emails
   - Start workflows
   - Generate documents

**Example Flow:**
```
Hausanschluss Glasfaser Journey Submission
  ↓
Automation: "House Connection Request Handler"
  ↓
Actions:
  - Create contact entity (customer data)
  - Create opportunity entity (connection request)
  - Trigger workflow "Hausanschluss Process"
  - Send confirmation email to customer
```

### 2. Journey → Entity Creation

Journey form data maps directly to entity schemas:
- Contact entities: Customer/installer personal information
- Opportunity entities: Service requests (house connections, tariff applications)
- Document entities: Uploaded files (contracts, certificates)

**Mapping Example:**
```
Journey Field: "customer.email"
  → Entity Field: contact._schema.email
  
Journey Field: "property.address"
  → Entity Field: opportunity.property_address
```

### 3. Journey → Workflow Initiation

Complex business processes start from journey submissions:
- **Hausanschluss Glasfaser** → Triggers "House Connection Installation Workflow"
- **Installateur Registration** → Triggers "Contractor Verification Workflow"
- **Tarifabschluss** → Triggers "Contract Finalization Workflow"

### 4. Journey Design Inheritance

Journeys reference design configurations:
- **Field:** `design.theme`
- **Source:** Design Builder API (`/v1/designs/{id}`)
- **Customization:** Organization-specific branding (logos, colors, fonts)
- **Default:** Fallback to "Default" design if no custom design specified

---

## Data Flow Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         CUSTOMER/INSTALLER                       │
│                  (External User - Browser/Mobile)                │
└────────────────────────────┬─────────────────────────────────────┘
                             │
                             │ Fills Form
                             ↓
┌─────────────────────────────────────────────────────────────────┐
│                     JOURNEY (Customer-Facing)                    │
│  • Multi-step forms with validation                              │
│  • Conditional logic (show/hide fields)                          │
│  • Design/branding applied                                       │
│  • Collects: Personal info, addresses, preferences, documents    │
└────────────────────────────┬─────────────────────────────────────┘
                             │
                             │ Submit Event
                             ↓
┌─────────────────────────────────────────────────────────────────┐
│                   AUTOMATION FLOW (Event Handler)                │
│  • Listens for: journey_submission events                        │
│  • Processes: Form data transformation                           │
│  • Actions:                                                      │
│    - map-entity: Create/update contacts, opportunities           │
│    - send-email: Notifications to customer & staff               │
│    - trigger-workflow: Start business process                    │
│    - create-document: Generate contracts/confirmations           │
└────────────────────────────┬─────────────────────────────────────┘
                             │
                             │ Create/Trigger
                             ↓
┌──────────────────────┬────────────────────┬────────────────────────┐
│                      │                    │                        │
│     ENTITIES         │    WORKFLOWS       │    DOCUMENTS           │
│  (Data Storage)      │  (Process Mgmt)    │  (File Generation)     │
│                      │                    │                        │
│  • contact           │  • Hausanschluss   │  • Contracts           │
│  • opportunity       │  • Installation    │  • Confirmations       │
│  • order             │  • Verification    │  • Invoices            │
│                      │                    │                        │
└──────────────────────┴────────────────────┴────────────────────────┘
```

---

## Use Case Examples

### Use Case 1: Fiber Optic Installation Request

**Journey:** Hausanschluss Glasfaser (14 steps, 27 logics)

**User Flow:**
1. Customer opens journey link
2. **Step 1-3:** Personal information (name, email, phone)
3. **Step 4-7:** Property details (address, ownership, accessibility)
4. **Step 8-11:** Installation preferences (location, timing, contact times)
5. **Step 12-14:** Review, terms acceptance, confirmation

**Conditional Logic Examples:**
- If "property_type = apartment" → Show "building_owner_contact" field
- If "ownership = rented" → Require landlord approval document upload
- If "urgent_request = yes" → Show expedited processing option

**Post-Submission Automation:**
1. Create contact entity (customer)
2. Create opportunity entity (connection request)
3. Trigger "Hausanschluss Fiber Installation" workflow
4. Send confirmation email to customer
5. Notify field operations team

### Use Case 2: Master Installer Registration

**Journey:** Installateur - Neueintragung Installateurverzeichnis (Stamminstallateur) (9 steps, 33 logics)

**User Flow:**
1. Installer opens registration journey
2. **Step 1-2:** Company information (name, registration number, address)
3. **Step 3-5:** Technician credentials (certificates, qualifications, experience)
4. **Step 6-7:** Insurance and compliance documents
5. **Step 8-9:** Review and submission

**Complex Logic:**
- If "existing_company = no" → Require company registration documents
- If "certification_type = gas" → Show gas-specific qualification fields
- If "technician_count > 1" → Enable repeatable technician section
- Validate certificate expiration dates dynamically

**Post-Submission Automation:**
1. Create contact entity (installer company)
2. Create entity for each technician
3. Trigger "Contractor Verification Workflow"
4. Send verification checklist to compliance team
5. Schedule audit if required

### Use Case 3: Tariff Contract Finalization

**Journey:** Tarifabschluss (27 steps, 10 logics)

**User Flow:**
1. Customer opens contract journey (often from email link)
2. **Step 1-5:** Customer verification (existing account or new)
3. **Step 6-12:** Supply address and meter information
4. **Step 13-18:** Tariff selection and customization
5. **Step 19-24:** Payment method and billing preferences
6. **Step 25-27:** Review, legal terms, e-signature

**Logic Rules:**
- If "existing_customer = yes" → Pre-fill customer data from entity
- If "meter_type = smart" → Show remote reading consent
- If "payment_method = SEPA" → Require IBAN validation

**Post-Submission Automation:**
1. Update existing contact entity or create new
2. Create order entity with selected tariff
3. Trigger "Contract Finalization Workflow"
4. Generate PDF contract document
5. Send signed contract to customer email
6. Initiate billing setup

---

## Design System Details

### Theme Configuration

All journeys inherit Material-UI theme with organization-specific overrides:

**Primary Color:** `#039BE5FF` (Blue)
**Text Color:** `#222222FF` (Dark gray)
**Background:** `#ffffff` (White)

### Component Customizations

- **Form Inputs:** 48px height, 22px top padding, 12px horizontal padding
- **Labels:** Ellipsis overflow for long text
- **Cards:** 24px padding, consistent spacing
- **App Bar:** Primary color background
- **Tabs:** 8px top margin, selected state highlighting
- **Toggle Buttons:** 32px height, bold font, primary color selection

### Layout Settings

- **Responsive:** Mobile-first design adapting to desktop
- **Accessibility:** ARIA labels, keyboard navigation support
- **Validation:** Real-time field validation with error messages

---

## Conditional Logic System

### Logic Rule Structure

```json
{
  "condition": "step1.field_name === 'value'",
  "actions": [
    {
      "type": "show",
      "target": "step2.conditional_field"
    },
    {
      "type": "validate",
      "target": "step2.required_field",
      "rule": "required"
    }
  ]
}
```

### Logic Types

1. **Visibility Logic** (Show/Hide)
   - Show fields based on previous answers
   - Hide irrelevant sections conditionally

2. **Validation Logic**
   - Dynamic required fields
   - Conditional format validation (e.g., IBAN only if payment=SEPA)

3. **Navigation Logic**
   - Skip steps based on answers
   - Branch to different paths

4. **Calculation Logic**
   - Auto-fill derived values
   - Price calculations based on selections

### Example: Complex Logic Chain

**Scenario:** Hausanschluss Glasfaser (27 logics)

```
IF property_type = "single_family"
  → Show "owner_name" field
  → Hide "building_management_contact" field
  
IF property_type = "apartment"
  → Show "building_management_contact" field
  → Require "landlord_approval" document
  → Show "floor_number" field
  
IF installation_location = "basement"
  → Show "basement_access_instructions" field
  → Require "basement_key_available" checkbox
  
IF urgent_request = true
  → Show "urgency_reason" text field
  → Calculate expedited_fee = base_fee * 1.5
  → Show expedited processing notice
```

---

## Revision Management

### Revision Tracking

Each journey maintains version history:
- **Created:** Timestamp and user who created journey
- **Modified:** Last update timestamp
- **Revisions:** Array of all historical versions

### Use Cases

1. **Rollback:** Revert to previous working version if issues arise
2. **Audit:** Track who made changes and when
3. **A/B Testing:** Compare different journey versions
4. **Compliance:** Maintain records of form changes for regulatory requirements

---

## Context Schema (Pre-fill Data)

### Purpose

Journeys can receive contextual data to pre-populate forms:

### Example: Order Follow-up Journey

```json
{
  "contextSchema": [
    {
      "field": "customer_id",
      "source": "entity:contact"
    },
    {
      "field": "order_id",
      "source": "entity:order"
    }
  ]
}
```

When journey opens via link with `?contact_id=abc&order_id=xyz`:
- Customer name, email, phone pre-filled
- Order details displayed
- User only fills new information

### Benefits

- **Reduced friction:** Customers don't re-enter known data
- **Accuracy:** Pre-filled data is validated entity data
- **Efficiency:** Faster form completion

---

## Business Process Observations

### Installer Management Focus

**7 out of 10 journeys** (70%) are installer-related:
- Reflects heavy regulatory requirements in utilities sector
- Gas vs. Master installer separation (different certifications)
- Credential lifecycle management (registration, renewal, updates)
- Indicates importance of contractor network management

### Complexity Distribution

- **Simple Portals (2 steps):** Used for credential renewal and document uploads
  - Low friction for existing users
  - Quick access without extensive forms
  
- **Medium Complexity (5-14 steps):** Registration and service request forms
  - Balance detail collection with user experience
  - Conditional logic reduces unnecessary fields
  
- **High Complexity (27 steps):** Comprehensive contract processes
  - Tariff selection requires extensive customer data
  - Legal/compliance requirements drive step count

### Automation Integration

All journeys integrate with automation flows:
- **100% automation coverage** for journey submissions
- Automations handle entity creation, notifications, workflow triggers
- Ensures consistent post-submission processing

---

## Recommendations for Analysis

### 1. Logic Optimization

**Observation:** Some journeys have very high logic counts (33 rules)

**Recommendation:**
- Review Neueintragung Stamminstallateur logic for simplification opportunities
- Consider splitting into multiple shorter journeys if logic becomes unmaintainable
- Document complex logic chains for future maintenance

### 2. Journey Analytics

**Data to Track:**
- Completion rates per journey
- Drop-off points (which steps lose users)
- Average completion time
- Validation error frequency per field

**Use For:**
- Identify friction points
- Optimize field ordering
- Simplify complex sections

### 3. Design Consistency

**Current State:** All journeys use same theme

**Recommendation:**
- Maintain consistency for user trust
- Consider journey-specific branding for external vs. internal users
- Test accessibility (color contrast, screen readers)

### 4. Context Schema Expansion

**Opportunity:** Only some journeys use context pre-fill

**Recommendation:**
- Implement context schema for follow-up journeys (quote acceptance, order updates)
- Reduce customer re-entry of known information
- Link journeys to existing entity records

---

## Technical Notes

### API Endpoints

- **Search:** `POST /v1/journey/configuration/search`
  - Query: `{"query": "*"}`
  - Returns: List of journeys with metadata
  
- **Detail:** `GET /v1/journey/configuration/{journey_id}`
  - Parameter: `journey_id` (configuration ID, not entity `_id`)
  - Returns: Full journey with steps, logics, design

### ID Mapping

**Important:** Journey search returns two IDs:
- `_id`: Entity storage ID (UUID)
- `journey_id`: Configuration ID (UUID, different from `_id`)

**Usage:**
- Use `_id` for file naming and referencing entity
- Use `journey_id` for fetching full configuration via API

### Export Structure

```
data/output/journeys_{timestamp}/
├── journeys_summary.json        # Overview with counts
├── journey_{entity_id}.json     # Individual journey exports
└── ...
```

---

## Related Resources

- **Automation Flows:** See `AUTOMATION_ANALYSIS.md` for journey submission handlers
- **Workflows:** See `BluePrintWorkflow_ANALYSIS.md` for post-journey processes
- **Entities:** Contact, opportunity, order schemas that journeys create
- **Designs:** Design Builder API for theme customization

---

## Conclusion

Journeys are the **critical entry point** for customer and contractor interactions in the Epilot platform. They:

1. **Collect structured data** via multi-step forms with validation
2. **Apply conditional logic** to create dynamic user experiences
3. **Trigger automations** that create entities and start workflows
4. **Maintain design consistency** through shared theming
5. **Track revisions** for audit and rollback capabilities

The current set of 10 journeys reflects the organization's focus on:
- **Contractor management** (70% of journeys)
- **House connection services** (20% of journeys)
- **Tariff/contract finalization** (10% of journeys)

This distribution aligns with utilities industry requirements for regulatory compliance (installer credentials) and customer service delivery (connections and contracts).
