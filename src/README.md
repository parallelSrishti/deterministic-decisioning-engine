# Deterministic Decisioning Engine (MVP)

A solo-built, API-first prototype demonstrating how deterministic financial decision systems can be designed with built-in explainability, audit persistence, and strict reproducibility guarantees.

This is a systems architecture prototype — not a production fintech platform.

---

## 1. Overview

The Deterministic Decisioning Engine:

- Accepts structured application inputs
- Applies fixed, rule-based deterministic logic
- Generates structured decisions and risk scores
- Persists complete request/response audit records
- Guarantees identical output for identical input

All decision events are stored with rule version tracking to ensure traceability.

---

## 2. Problem Statement

Many automated decision systems lack:

1. Reproducibility (hidden state, probabilistic models)
2. Structured explanation outputs
3. Complete audit storage of input/output payloads

This prototype explores how those concerns can be addressed using:

- Deterministic rule logic
- API-first architecture
- PostgreSQL audit persistence
- Explicit rule version tracking

No machine learning is used.

---

## 3. MVP Scope

### Included

- Deterministic rule engine
- Score generation (0–1000)
- Decision mapping (APPROVE / REVIEW / REJECT)
- Structured reason codes
- Template-based explanation generation
- PostgreSQL (Railway-managed) audit persistence
- Full request + response JSON storage (JSONB)
- FastAPI REST API
- Streamlit demo UI (Python-only)
- Determinism validation mechanism

### Explicitly Excluded

- Authentication / user accounts
- Machine learning models
- External bureau integrations
- Multi-tenancy
- Rate limiting
- CI/CD pipelines
- Production hardening
- Regulatory compliance claims

---

## 4. Architecture

### Tech Stack

- Backend: FastAPI (Python 3.10+)
- Database: PostgreSQL (Railway-managed)
- ORM: SQLAlchemy
- Frontend: Streamlit (Python-only client)
- Communication: REST (JSON over HTTP)

---

### High-Level Flow

Streamlit UI  
      ↓  
POST /apply (FastAPI)  
      ↓  
Input Validation (Pydantic)  
      ↓  
Deterministic Rule Engine  
      ↓  
Persist to PostgreSQL (JSONB audit record)  
      ↓  
Structured Response Returned  

Audit retrieval:

Client → GET /audit/{audit_id} → Return stored record (no recomputation)

---

## 5. API Endpoints

### POST /apply

Evaluates structured application input.

**Input Fields**

- income_monthly
- dti
- employment_months
- age
- has_defaults

**Response Fields**

- audit_id (UUID)
- decision (APPROVE / REVIEW / REJECT)
- score (0–1000)
- reason_codes
- explanation
- rule_version

---

### GET /audit/{audit_id}

Retrieves stored audit record.

Returns:

- request_json
- response_json
- rule_version
- created_at

Decision is never recomputed on retrieval.

---

### GET /health

Returns:

{ "status": "ok" }

---

## 6. Determinism Guarantee

The system guarantees:

- No randomness
- No time-based evaluation logic
- No external API dependencies
- Pure rule evaluation
- Identical input → identical decision & score

Only audit_id and timestamp differ across identical submissions.

---

## 7. Running Locally

### 1. Set Environment Variable

Export your Railway PostgreSQL connection string:

```bash
export DATABASE_URL="your_railway_postgres_connection_string"
```

### 2. Run Backend

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Access API docs at:

```
http://127.0.0.1:8000/docs
```

### 3. Run Streamlit UI

```bash
streamlit run ui/streamlit_app.py
```

---

## 8. Repository Documentation

The full documentation suite includes:

- PRD.md — Product requirements
- APP_FLOW.md — User interaction flows
- TECH_STACK.md — Technology decisions
- BACKEND_STRUCTURE.md — Backend architecture
- FRONTEND_GUIDELINES.md — UI design constraints
- IMPLEMENTATION_PLAN.md — Build roadmap

All documents are structurally aligned and reflect the current architecture.

---

## 9. Non-Goals

This project is not:

- A real credit scoring engine
- A licensed financial product
- A production-ready system
- A regulatory-certified platform
- A SaaS deployment

It is a deterministic systems design prototype built for architectural clarity and technical evaluation.

---

**Last Updated:** 2026-02-12
