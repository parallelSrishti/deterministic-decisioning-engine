# Technical Stack Documentation

## 1. Architecture Overview

### System Type
API-first deterministic decision service with audit-grade persistence.

### Architectural Style
Layered architecture:

Streamlit UI (Client Layer)
        ↓
FastAPI (Application Layer)
        ↓
Deterministic Rule Engine (Domain Layer)
        ↓
PostgreSQL (Persistence Layer - Railway)

### Deployment Model
Single-instance service suitable for demo or prototype environments.

---

## 2. Core Technologies

### Backend Framework
- **FastAPI (Python 3.10+)**
  - ASGI-based framework
  - Automatic OpenAPI documentation
  - Pydantic-based validation

### Database
- **PostgreSQL (Railway-managed)**
  - Remote managed database service
  - JSONB storage for request/response payloads
  - UTC timestamp support
  - ACID-compliant persistence

### ORM Layer
- **SQLAlchemy**
  - Database abstraction layer
  - Declarative models
  - Session management

### UI Layer
- **Streamlit**
  - Python-based demo interface
  - No client-side JavaScript required
  - Calls FastAPI endpoints via HTTP

### Validation
- **Pydantic**
  - Strict input validation
  - Type enforcement
  - Range validation

---

## 3. API Layer

### Endpoints

- **POST /apply**
  - Accept structured input
  - Run deterministic rule engine
  - Persist audit record
  - Return structured decision response

- **GET /audit/{audit_id}**
  - Retrieve stored request and response payload
  - Return rule_version and timestamp

- **GET /health**
  - Service availability check

### Communication Format
- JSON request/response
- HTTP status codes (200, 400, 404, 500)

---

## 4. Domain Layer (Decision Engine)

### Characteristics
- Pure Python module
- Deterministic evaluation logic
- No randomness
- No external API calls
- No time-dependent logic

### Scoring Model
- Score range: 0–1000
- Threshold-based decision mapping:
  - ≥ 720 → APPROVE
  - 600–719 → REVIEW
  - < 600 → REJECT

### Explainability
- Fixed reason codes
- Template-based explanation rendering
- Stored with each audit record

---

## 5. Persistence Layer

### Database Design

Single primary table: `audits`

Stores:
- id (UUID, primary key)
- created_at (TIMESTAMPTZ, UTC)
- rule_version (TEXT)
- request_json (JSONB)
- response_json (JSONB)
- decision (TEXT)
- score (INTEGER)

### Design Principles
- Full payload storage (no recomputation on retrieval)
- Rule version tracking
- Append-only audit model

---

## 6. Environment Configuration

### Required Environment Variables
- DATABASE_URL (Railway PostgreSQL connection string)
- API_BASE (for Streamlit UI, optional)

### Local Development
- FastAPI served via Uvicorn
- Streamlit served locally
- PostgreSQL accessed remotely via Railway

---

## 7. Logging & Error Handling

### Logging
- Basic Python logging
- Console-level output suitable for demo

### Error Handling
- 400 → Validation errors
- 404 → Audit record not found
- 500 → Unexpected internal errors

No distributed tracing or monitoring in MVP.

---

## 8. Security Posture (MVP Scope)

Included:
- Strict input validation
- Controlled schema boundaries

Excluded:
- Authentication
- Authorization
- Role-based access control
- Rate limiting
- Encryption key management
- Production secrets rotation

Not intended for real financial data.

---

## 9. Scalability & Performance

Current Scope:
- Single-instance deployment
- No horizontal scaling
- No connection pooling optimization

Future Upgrade Path:
- Introduce connection pooling
- Add API versioning
- Add distributed deployment
- Introduce caching layer

---

## 10. Explicitly Out of Scope

- Machine learning models
- Bureau integrations
- Multi-tenant architecture
- CI/CD pipelines
- Observability tooling (Prometheus, Datadog, etc.)
- Production infrastructure hardening

---

## 11. Rationale

The chosen stack prioritizes:

- Architectural clarity
- Deterministic reproducibility
- Audit-grade persistence
- Minimal cognitive overhead for solo development
- Clean separation between UI, API, domain logic, and persistence

This ensures documentation integrity aligns with implementation reality.

---

**Last Updated**: 2026-02-12
