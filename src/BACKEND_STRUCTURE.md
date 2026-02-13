# Backend Structure Documentation

## 1. Architecture Overview

### System Type
API-first deterministic decision service with audit-grade persistence.

### Architectural Pattern
Layered architecture with clear separation of concerns:

Client Layer (Streamlit)
        ↓
API Layer (FastAPI)
        ↓
Domain Layer (Deterministic Rule Engine)
        ↓
Persistence Layer (PostgreSQL - Railway)

### Core Characteristics

- Deterministic (no randomness, no ML)
- Stateless HTTP request/response cycle
- Synchronous processing
- Single-instance deployment (MVP scope)
- Audit-grade persistence

---

## 2. Component Breakdown

### 2.1 API Layer (FastAPI)

Responsibilities:
- HTTP request handling
- Input validation (Pydantic)
- Response serialization
- Error handling
- OpenAPI documentation generation

Endpoints:

- POST /apply
- GET /audit/{audit_id}
- GET /health

All endpoints public in MVP scope.

---

### 2.2 Domain Layer (Decision Engine)

Characteristics:
- Pure Python module
- Deterministic evaluation logic
- No external dependencies
- No database awareness

Responsibilities:
- Evaluate input payload
- Generate risk score (0–1000)
- Map score to decision (APPROVE / REVIEW / REJECT)
- Generate reason codes
- Render explanation template

Decision Thresholds:

- score ≥ 720 → APPROVE
- 600 ≤ score < 720 → REVIEW
- score < 600 → REJECT

---

### 2.3 Persistence Layer (PostgreSQL - Railway)

Database Type:
- PostgreSQL (managed via Railway)

Primary Table: `audits`

Columns:
- id (UUID, Primary Key)
- created_at (TIMESTAMPTZ, UTC)
- rule_version (TEXT)
- request_json (JSONB)
- response_json (JSONB)
- decision (TEXT)
- score (INTEGER)

Design Principles:
- Full request/response stored
- No recomputation on retrieval
- Append-only audit model
- Rule version tracked per record

---

## 3. Data Flow

### Application Submission Flow

1. Client sends POST /apply
2. FastAPI validates request via Pydantic
3. Domain engine evaluates decision deterministically
4. API constructs response object
5. Record persisted in PostgreSQL
6. Structured response returned to client

---

### Audit Retrieval Flow

1. Client sends GET /audit/{audit_id}
2. API queries PostgreSQL
3. Stored record returned
4. No recomputation of decision logic

---

## 4. Validation Strategy

### Input Validation (Pydantic)

- income_monthly ≥ 0
- dti between 0.0 and 5.0
- employment_months ≥ 0
- age ≥ 18
- has_defaults boolean

Invalid input → 400/422 response

### Business Logic Evaluation

Validation ≠ Evaluation.

Applications that pass schema validation may still result in REJECT based on rule logic.

---

## 5. Error Handling Model

HTTP Status Codes:

- 200 → Successful evaluation
- 400 → Validation error
- 404 → Audit record not found
- 500 → Internal server error

Error Format:

{ 
  "error": "Error type",
  "details": "Context-specific message"
}

Stack traces logged server-side only.

---

## 6. Determinism Guarantees

System guarantees:

- No random number generators
- No time-dependent logic in evaluation
- No external API calls
- Pure function rule evaluation
- Identical input → identical output

Determinism validated via repeated test submissions.

---

## 7. Environment Configuration

Required Environment Variables:

- DATABASE_URL → Railway PostgreSQL connection string

Optional:

- API_BASE → Used by Streamlit client

Deployment Model:

- FastAPI served via Uvicorn
- PostgreSQL hosted on Railway
- Streamlit runs locally or separately deployed

---

## 8. Non-Functional Considerations (MVP Scope)

### Performance
- Single-user demo context
- <500ms response time locally
- No connection pooling optimization

### Scalability
- No horizontal scaling
- No read replicas
- No load balancing

### Observability
- Basic console logging
- No distributed tracing
- No metrics aggregation

---

## 9. Explicitly Out of Scope

Infrastructure:
- Redis caching
- Background workers
- Message queues
- Auto-scaling

Security:
- Authentication
- Authorization
- Rate limiting
- WAF
- TLS enforcement

Compliance:
- GDPR mechanisms
- SOC2 alignment
- Regulatory certifications

---

## 10. Future Extension Points

- Introduce ML scoring model alongside deterministic engine
- Add API versioning
- Add connection pooling
- Add multi-tenant architecture
- Introduce role-based authentication

---

**Last Updated**: 2026-02-12
