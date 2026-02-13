# Application Flow Documentation

## 1. Entry Points

### Primary Entry Points

- **Streamlit Web UI (Local or Deployed)**  
  User accesses the Streamlit interface to submit applications and view results.

- **Direct API Access (FastAPI Docs)**  
  Access via `/docs` (OpenAPI UI) for direct API testing.

- **Direct API Calls**  
  REST access to:
  - POST /apply
  - GET /audit/{audit_id}
  - GET /health

### Secondary Entry Points

- None in MVP (no marketing pages, OAuth, deep links, or external integrations).

---

## 2. Core User Flows

### Flow 1: Submit Application

**Goal**: Receive deterministic decision output  
**Entry Point**: Streamlit UI form  
**Frequency**: Multiple test submissions during demo

#### Happy Path

1. **Screen: Application Form**
   - Elements:
     - income_monthly (number input)
     - dti (decimal input)
     - employment_months (number input)
     - age (number input)
     - has_defaults (checkbox)
     - Submit button
   - User Action: Fill inputs and click “Evaluate”

2. **System Action: Validation**
   - Server-side validation via FastAPI (Pydantic)
   - Validation rules:
     - age ≥ 18
     - dti between 0.0–5.0
     - income_monthly ≥ 0
     - employment_months ≥ 0

3. **System Action: Deterministic Rule Evaluation**
   - Apply rule engine
   - Generate score (0–1000)
   - Assign decision (APPROVE / REVIEW / REJECT)
   - Generate reason codes
   - Generate explanation text

4. **System Action: Audit Persistence**
   - Store request_json (JSONB)
   - Store response_json (JSONB)
   - Store decision
   - Store score
   - Store rule_version
   - Store created_at timestamp (UTC)
   - Generate audit_id (UUID)

5. **Screen: Result Display**
   - Displays:
     - Decision
     - Score
     - Reason codes
     - Explanation
     - audit_id
   - Option to retrieve audit record

**Success State**: Structured response displayed and audit_id returned

---

#### Error States

- **Invalid Input (400)**
  - Display: Inline validation error message
  - Action: User corrects and resubmits

- **Server Error (500)**
  - Display: Generic error message
  - Action: Retry submission

---

#### Edge Cases

- Duplicate submissions → Generates separate audit records
- Same payload submitted twice → Identical decision & score
- Large numeric input → Rejected via validation

---

### Flow 2: Retrieve Audit Record

**Goal**: Verify stored decision  
**Entry Point**: Result screen audit button or manual ID entry

#### Happy Path

1. **Screen: Audit Retrieval Trigger**
   - User clicks “View Audit Record”

2. **System Action**
   - GET /audit/{audit_id}
   - Query PostgreSQL

3. **Screen: Audit Display**
   - Shows:
     - Stored request payload
     - Stored response payload
     - rule_version
     - created_at timestamp

**Success State**: Stored record displayed (not recomputed)

---

#### Error States

- **Invalid ID Format**
  - Display: Validation error

- **Audit Not Found (404)**
  - Display: “Audit record not found”

---

### Flow 3: Health Check

**Goal**: Verify backend availability  
**Entry Point**: GET /health

**Response**:
{ "status": "ok" }

Used for deployment validation and system status checks.

---

## 3. Navigation Map

Streamlit UI

Application Form  
   ↓  
Result Display  
   ↓  
Audit Record View  

API Docs (/docs) – Direct testing interface

---

## 4. Screen Inventory

### Screen: Application Form
- **Route**: Streamlit root
- **Access**: Public
- **Purpose**: Submit application payload
- **Key Elements**:
  - Numeric inputs
  - Checkbox
  - Submit button
- **State Variants**:
  - Default
  - Validation Error
  - Submitting (loading state)

---

### Screen: Result Display
- **Route**: Same page after submission
- **Access**: Public
- **Purpose**: Display decision output
- **Key Elements**:
  - Decision metric
  - Score metric
  - Reason codes
  - Explanation
  - audit_id
- **State Variants**:
  - Success
  - Server Error

---

### Screen: Audit Record Display
- **Route**: Same UI section
- **Access**: Public
- **Purpose**: Display stored audit record
- **Key Elements**:
  - request_json
  - response_json
  - rule_version
  - timestamp
- **State Variants**:
  - Found
  - Not Found (404)

---

## 5. Decision Points

### Decision: Input Validation

IF input fails validation  
THEN return 400 with error message  
ELSE proceed to rule engine

---

### Decision: Score Threshold

IF score ≥ 720  
THEN decision = APPROVE  
ELSE IF score ≥ 600  
THEN decision = REVIEW  
ELSE decision = REJECT

---

### Decision: Audit Record Exists

IF audit_id exists in database  
THEN return stored record  
ELSE return 404

---

## 6. Error Handling

### 400 – Validation Error
- Display inline message
- Preserve user input

### 404 – Audit Not Found
- Display not-found message

### 500 – Internal Error
- Display generic retry message

---

## 7. Responsive Behavior

### Mobile
- Single-column layout
- Full-width inputs
- Scroll-based interaction

### Desktop
- Centered layout
- Metrics displayed side-by-side

---

## 8. Animations & Transitions

- Button click → Loading spinner
- Result display → Instant render
- No complex animations in MVP

---

**Last Updated**: 2026-02-12
