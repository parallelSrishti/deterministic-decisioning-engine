"""SQLAlchemy model for the audits table."""

import uuid

from sqlalchemy import Column, DateTime, Index, Integer, String, func
from sqlalchemy.dialects.postgresql import JSONB, UUID

from app.db.database import Base


class Audit(Base):
    __tablename__ = "audits"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    rule_version = Column(String, nullable=False)
    request_json = Column(JSONB, nullable=False)
    response_json = Column(JSONB, nullable=False)
    decision = Column(String, nullable=False)
    score = Column(Integer, nullable=False)

    __table_args__ = (
        Index("ix_audits_created_at", "created_at"),
        Index("ix_audits_decision", "decision"),
    )
