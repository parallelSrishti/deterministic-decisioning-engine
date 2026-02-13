"""FastAPI application entry point."""

import uuid

from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from app.db.database import get_db, init_db
from app.engine.rules import RULE_VERSION, evaluate_application
from app.models.audit import Audit
from app.schemas.request import ApplicationRequest
from app.schemas.response import DecisionResponse

app = FastAPI(title="Deterministic Decisioning Engine", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup() -> None:
    """Register models and create database tables on startup."""
    #import app.models.audit  # noqa: F401 — register Audit on Base.metadata
    init_db()


@app.get("/health")
def health_check() -> dict:
    """Service availability check."""
    return {"status": "ok"}


@app.post("/apply", response_model=DecisionResponse, tags=["decisioning"])
def apply(request: ApplicationRequest, db: Session = Depends(get_db)) -> DecisionResponse:
    """Evaluate application and persist audit record."""
    result = evaluate_application(request)
    rule_version = result["rule_version"]

    audit_uuid = uuid.uuid4()
    request_payload = request.model_dump()
    response_payload = {
        "decision": result["decision"],
        "score": result["score"],
        "reason_codes": result["reason_codes"],
        "explanation": result["explanation"],
        "rule_version": rule_version,
    }

    audit = Audit(
        id=audit_uuid,
        rule_version=RULE_VERSION,
        request_json=request_payload,
        response_json=response_payload,
        decision=result["decision"],
        score=result["score"],
    )
    try:
        db.add(audit)
        db.commit()
        db.refresh(audit)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Database write failed: {e}") from e

    return DecisionResponse(
        audit_id=str(audit_uuid),
        decision=result["decision"],
        score=result["score"],
        reason_codes=result["reason_codes"],
        explanation=result["explanation"],
        rule_version=rule_version,
    )


@app.get("/audit/{audit_id}", tags=["audit"])
def get_audit(audit_id: str, db: Session = Depends(get_db)) -> dict:
    """Retrieve a stored audit record by ID. No recomputation."""
    try:
        audit_uuid = uuid.UUID(audit_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid audit_id")

    record = db.query(Audit).filter(Audit.id == audit_uuid).first()
    if not record:
        raise HTTPException(status_code=404, detail="Audit not found")

    return {
        "audit_id": str(record.id),
        "request_json": record.request_json,
        "response_json": record.response_json,
        "rule_version": record.rule_version,
        "created_at": record.created_at.isoformat(),
        "decision": record.decision,
        "score": record.score,
    }
