import uuid
from datetime import datetime
from sqlalchemy import String, Integer, DateTime, Enum, ForeignKey, JSON, Float, Text
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
    scan_id: Mapped[str | None] = mapped_column(String(100), index=True)

    # Información básica
    title: Mapped[str] = mapped_column(String(500))
    description: Mapped[str | None] = mapped_column(Text)
    severity: Mapped[str] = mapped_column(String(20))

    # Clasificación
    cwe_id: Mapped[str | None] = mapped_column(String(20))
    owasp_top_10: Mapped[str | None] = mapped_column(String(50))
    category: Mapped[str | None] = mapped_column(String(100))

    # Ubicación
    file_path: Mapped[str] = mapped_column(String(500))
    line_number: Mapped[int]
    code_snippet: Mapped[str | None] = mapped_column(Text)
    function_name: Mapped[str | None] = mapped_column(String(200))
    class_name: Mapped[str | None] = mapped_column(String(200))

    # Priorización
    cvss_vector: Mapped[str | None] = mapped_column(String(200))
    cvss_base_score: Mapped[float | None] = mapped_column(Float)
    cvss_temporal_score: Mapped[float | None] = mapped_column(Float)
    cvss_environmental_score: Mapped[float | None] = mapped_column(Float)
    confidence: Mapped[float | None] = mapped_column(Float)
    impact: Mapped[str | None] = mapped_column(String(20))
    exploitability: Mapped[str | None] = mapped_column(String(20))
    priority_score: Mapped[float | None] = mapped_column(Float)  # Score calculado

    # Metadatos
    tags: Mapped[list[str]] = mapped_column(JSON, default=list)
    references: Mapped[list[str]] = mapped_column(JSON, default=list)
    custom_fields: Mapped[dict] = mapped_column(JSON, default=dict)

    # Información de herramienta
    tool_name: Mapped[str | None] = mapped_column(String(100))
    tool_version: Mapped[str | None] = mapped_column(String(50))
    tool_type: Mapped[str | None] = mapped_column(String(20))

    # Contexto
    commit_hash: Mapped[str | None] = mapped_column(String(100))
    branch: Mapped[str | None] = mapped_column(String(100))
    author: Mapped[str | None] = mapped_column(String(100))
    repository_url: Mapped[str | None] = mapped_column(String(500))
    scan_date: Mapped[datetime | None] = mapped_column(DateTime)

    # Estado y tracking
    fingerprint: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    hash_version: Mapped[int] = mapped_column(default=1)
    status: Mapped[FindingStatus] = mapped_column(Enum(FindingStatus), default=FindingStatus.OPEN)
    assigned_to: Mapped[str | None] = mapped_column(String(100))
    due_date: Mapped[datetime | None] = mapped_column(DateTime)

    # Auditoría
    extra_data: Mapped[dict] = mapped_column(JSON, default=dict)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relaciones
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
