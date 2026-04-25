import uuid
from datetime import datetime, timezone
from sqlalchemy import String, Integer, DateTime, Enum, ForeignKey, JSON, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base
import enum

class FindingStatus(str, enum.Enum):
    OPEN = "OPEN"
    IN_PROGRESS = "IN_PROGRESS"
    RESOLVED = "RESOLVED"
    FALSE_POSITIVE = "FALSE_POSITIVE"
    ACCEPTED_RISK = "ACCEPTED_RISK"

class Finding(Base):
    __tablename__ = "findings"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    tenant_id: Mapped[str] = mapped_column(String(50), index=True)
    project_id: Mapped[str] = mapped_column(String(100), index=True)
    title: Mapped[str] = mapped_column(String(500))
    severity: Mapped[str] = mapped_column(String(20))
    cwe_id: Mapped[str | None] = mapped_column(String(20))
    cvss_score: Mapped[float | None] = mapped_column(Float)
    file_path: Mapped[str] = mapped_column(String(500))
    line_number: Mapped[int]
    fingerprint: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    hash_version: Mapped[int] = mapped_column(default=1)
    metadata: Mapped[dict] = mapped_column(JSON, default={})
    status: Mapped[FindingStatus] = mapped_column(Enum(FindingStatus), default=FindingStatus.OPEN)
    created_at: Mapped[datetime] = mapped_column(default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    history: Mapped[list["FindingHistory"]] = relationship(back_populates="finding")

class FindingHistory(Base):
    __tablename__ = "findings_history"
    id: Mapped[int] = mapped_column(primary_key=True)
    finding_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("findings.id"))
    action: Mapped[str]
    old_value: Mapped[dict] = mapped_column(JSON)
    new_value: Mapped[dict] = mapped_column(JSON)
    changed_by: Mapped[str]
    changed_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    finding: Mapped["Finding"] = relationship(back_populates="history")
