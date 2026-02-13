# Product Requirements Document (PRD)

## 1. Product Overview
- **Project Title**: Deterministic Decisioning Engine (MVP)
- **Version**: 1.0
- **Last Updated**: 2026-02-12
- **Owner**: Srishti

---

## 2. Problem Statement

Automated decision systems frequently suffer from:
- Non-reproducible outcomes due to hidden state or probabilistic models
- Opaque rejection logic without structured explanations
- Inconsistent or incomplete audit storage of input/output payloads

This MVP addresses these issues by implementing a fully deterministic, rule-based decision engine with persistent audit logging and structured explainability, without machine learning or external integrations.

---

## 3. Goals & Objectives

### Business Goals
- Demonstrate deterministic system architecture within 7 days
- Provide audit-grade persistence using PostgreSQL (Railway-managed)
- Enable reproducible decision outputs for identical inputs

### User Goals
- Submit an application and receive a structured decision
- Understand why a decision was made
- Retrieve a stored audit record by ID

---

## 4. Success Metrics

- 100% deterministic output reproducibility (same input → identical decision & score)
- 100% decision requests persist to database with full payload
- <500ms response time under single-user local testing
- All audit records retrievable via API endpoint

---

## 5. Target Users & Personas

### Primary Persona: Technical Evaluator
- **Demographics**: Engineer, Product Manager, or Reviewer
- **Pain Points**: Black-box systems, lack of traceability
- **Goals**: Assess architectural clarity and reproducibility
- **Technical Proficiency**: High

### Secondary Persona: Architecture Reviewer
- **Demographics**: Hiring manager or technical interviewer
- **Pain Points**: Overly complex prototypes
- **Goals**: Evaluate system boundaries and discipline
- **Technical Proficiency**: High

---

## 6. Features & Requirements

### Must-Have Features (P0)

#### 1. Deterministic Decision Endpoint
- Description: Accept structured input and return rule-based decision output
- User Story: As a reviewer, I want to submit inputs so that I can observe deterministic outputs
- Acceptance Criteria:
  - [ ] Identical input produces identical decision and score
  - [ ] Score is between 0–1000
  - [ ] Decision is APPROVE, REVIEW, or REJECT
  - [ ] Response includes reason codes and explanation
- Success Metric: Determinism validated across repeated submissions

#### 2. Audit Persistence (PostgreSQL)
- Description: Store full request and response payloads with rule version
- User Story: As a reviewer, I want audit logs so that I can verify traceability
- Acceptance Criteria:
  - [ ] request_json stored as JSONB
  - [ ] response_json stored as JSONB
  - [ ] rule_version stored with record
  - [ ] Timestamp recorded in UTC
- Success Metric: 100% decision events retrievable

#### 3. Audit Retrieval Endpoint
- Description: Retrieve stored decision record by audit ID
- User Story: As a reviewer, I want to fetch historical decisions so that I can validate stored outputs
- Acceptance Criteria:
  - [ ] Returns stored payload (not recomputed)
  - [ ] Returns rule_version
  - [ ] Returns created_at timestamp
- Success Metric: Retrieval success rate 100%

#### 4. Streamlit Demo UI
- Description: Python-based UI interacting with FastAPI endpoints
- User Story: As a reviewer, I want a simple UI so that I can test without Postman
- Acceptance Criteria:
  - [ ] Submits payload to /apply
  - [ ] Displays decision and score
  - [ ] Fetches audit record by ID
  - [ ] Includes determinism validation check
- Success Metric: End-to-end demo flow functional

---

### Should-Have Features (P1)
- Structured explanation template formatting
- Basic input validation rules
- Clear error response schema

---

### Nice-to-Have Features (P2)
- Simulation endpoint for synthetic batch testing
- Decision distribution summary metrics

---

## 7. Explicitly OUT OF SCOPE

- Machine learning models
- Authentication or user accounts
- Multi-tenant architecture
- External bureau integrations
- Rate limiting
- CI/CD pipelines
- Production scaling guarantees
- Compliance certification claims

---

## 8. User Scenarios

### Scenario 1: Application Submission
- **Context**: Reviewer tests system
- **Steps**:
  1. Submit application via Streamlit UI
  2. FastAPI validates input
  3. Deterministic engine computes decision
  4. System stores audit record in PostgreSQL
  5. Response returned to UI
- **Expected Outcome**: Structured decision + audit_id returned
- **Edge Cases**:
  - Invalid numeric range → 400 response
  - Missing field → validation error

---

## 9. Dependencies & Constraints

### Technical Constraints
- PostgreSQL hosted on Railway
- FastAPI backend
- Streamlit UI (Python-only)
- SQLAlchemy ORM

### Business Constraints
- Solo-built MVP
- 3–4 day build window

### External Dependencies
- Railway PostgreSQL service

---

## 10. Timeline & Milestones

- **MVP**: 3–4 days
  - FastAPI endpoints
  - PostgreSQL persistence
  - Streamlit demo UI
- **V1.0 (Extended)**:
  - Simulation endpoint
  - Enhanced rule categories

---

## 11. Risks & Assumptions

### Risks
- Railway connection misconfiguration → Mitigation: Validate DATABASE_URL before deployment
- Scope creep → Mitigation: Strict OUT OF SCOPE section

### Assumptions
- Single-user demo context
- No concurrent scaling required

---

## 12. Non-Functional Requirements

- **Performance**: <500ms local response time
- **Security**: Not publicly exposed in production
- **Accessibility**: Basic Streamlit accessibility support
- **Scalability**: Not designed for horizontal scaling

---

## 13. References & Resources

- TECH_STACK.md
- APP_FLOW.md
- BACKEND_STRUCTURE.md
