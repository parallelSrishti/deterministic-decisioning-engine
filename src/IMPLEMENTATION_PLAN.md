# IMPLEMENTATION_PLAN.md
**Deterministic Decisioning Engine (MVP)**

> Solo-developer implementation plan  
> Timeline: 3–4 days  
> Stack: FastAPI + PostgreSQL (Railway) + SQLAlchemy + Streamlit  

---

## 1. Overview

### Project Summary

**Name:** Deterministic Decisioning Engine (MVP)  
**Timeline:** 3–4 days  
**Team:** 1 developer  
**Database:** PostgreSQL (Railway-managed)  
**UI:** Streamlit (Python-only)  

### Build Philosophy

**Ship Determinism First**  
Core value is reproducible, explainable decision logic.

**API-First Architecture**  
All logic resides in FastAPI. Streamlit is a thin client.

**Audit-Grade Persistence**  
Every decision stores full request + response payload with rule_version.

**No Infrastructure Over-Engineering**  
No Docker, no CI/CD, no migrations tooling, no scaling work.

---

## 2. Explicitly Out of Scope

❌ Authentication  
❌ JWT  
❌ Multi-user system  
❌ Redis / caching  
❌ Background workers  
❌ CI/CD  
❌ Production hardening  
❌ Load balancing  
❌ Monitoring stack  
❌ ML models  

---

## 3. Phase 1: Foundation (Day 1)

### Goal
FastAPI running and connected to Railway PostgreSQL.

---

### Step 1.1 – Backend Setup

- Create virtual environment
- Install:
  - fastapi
  - uvicorn
  - sqlalchemy
  - psycopg (driver used by SQLAlchemy)
  - pydantic
- Create project structure:
  - app/main.py
  - app/models/
  - app/db/
  - app/engine/
  - app/schemas/

**Success Criteria:**
- GET /health returns status ok
- FastAPI docs available at /docs

---

### Step 1.2 – Railway PostgreSQL Setup

- Create Railway project
- Add PostgreSQL service
- Copy DATABASE_URL
- Store as environment variable locally

**Validation Step:**
- SQLAlchemy engine connects successfully
- Test simple SELECT 1 query

**Success Criteria:**
- Backend connects to Railway database
- No local SQLite usage anywhere

---

## 4. Phase 2: Persistence Layer (Day 1–2)

### Goal
Create audit table and persistence logic.

---

### Step 2.1 – Audit Table Design

Table: audits

Fields:
- id (UUID, primary key)
- created_at (TIMESTAMPTZ, UTC)
- rule_version (TEXT)
- request_json (JSONB)
- response_json (JSONB)
- decision (TEXT)
- score (INTEGER)

---

### Step 2.2 – SQLAlchemy Model

- Define declarative model
- Ensure JSONB columns used
- Add indexes:
  - created_at
  - decision

**Success Criteria:**
- Table auto-created on startup
- Insert and query operations work

---

## 5. Phase 3: Deterministic Engine (Day 2)

### Goal
Implement pure, reproducible rule engine.

### Requirements

- No randomness
- No time-based logic
- No database dependency
- Pure function evaluation

### Decision Thresholds

- score ≥ 720 → APPROVE
- 600–719 → REVIEW
- < 600 → REJECT

**Validation Task:**
- Submit identical input 100 times
- Verify identical score + decision

**Success Criteria:**
- Determinism confirmed

---

## 6. Phase 4: API Endpoints (Day 2–3)

### POST /apply

Flow:
1. Validate input (Pydantic)
2. Run deterministic engine
3. Persist full audit record
4. Return structured response with audit_id

Response must include:
- decision
- score
- reason_codes
- explanation
- rule_version
- audit_id

---

### GET /audit/{audit_id}

Flow:
1. Query database
2. Return stored record
3. No recomputation

Return:
- request_json
- response_json
- created_at
- rule_version

---

### GET /health

Return:
{ "status": "ok" }

---

## 7. Phase 5: Streamlit UI (Day 3)

### Goal
Provide thin demo client.

### UI Components

- Application form
- Result display section
- Audit retrieval section
- Determinism check button

### Behavior

- Form submits via HTTP to FastAPI
- Results rendered visibly
- Audit displayed from stored record

**Success Criteria:**
- Full end-to-end demo flow works
- No backend logic duplicated in Streamlit

---

## 8. Phase 6: Validation & Testing (Day 4)

### API Tests

- Valid application
- Invalid age
- Invalid DTI
- Negative income
- Duplicate identical submissions

---

### Determinism Test

- Same payload → identical output
- Only audit_id differs

---

### Audit Integrity Test

- Retrieve audit
- Confirm response matches original stored payload

---

## 9. Timeline Breakdown

| Day | Focus | Deliverable |
|-----|--------|------------|
| 1 | FastAPI + Railway DB | Connected backend |
| 2 | Engine + Audit Model | Deterministic logic + persistence |
| 3 | API Endpoints + UI | End-to-end flow |
| 4 | Testing + Polish | Stable demo-ready system |

Total effort: ~20–28 hours

---

## 10. Risk Mitigation

### Risk: Railway connection misconfiguration
Mitigation: Validate DATABASE_URL before building engine logic.

### Risk: Scope creep
Mitigation: Daily review of out-of-scope list.

### Risk: Non-deterministic behavior
Mitigation: Strict pure function design + repeated test loop.

---

## 11. MVP Success Criteria

MVP is complete when:

- POST /apply persists record
- GET /audit/{audit_id} returns stored payload
- Determinism verified
- Streamlit demo works locally
- No runtime crashes
- No SQLite anywhere in codebase

---

## 12. Post-MVP Extensions (Not During Build)

- API versioning
- ML scoring model
- Authentication
- Role-based access
- Connection pooling optimization
- Deployment to Railway as backend service

---

**Last Updated:** 2026-02-12
