from pydantic import BaseModel, ConfigDict, Field
from typing import Optional, List, Dict, Any
from uuid import UUID
from datetime import datetime
from app.models.finding import FindingStatus

class ScanToolInfo(BaseModel):
    """Información de la herramienta que detectó la vulnerabilidad"""
    name: str  # Ej: "semgrep", "sonarcloud", "owasp-zap"
    version: Optional[str] = None
    type: str  # "SAST", "DAST", "SCA", "IAST", "DAST"

class CVSSInfo(BaseModel):
    """Información completa de CVSS"""
    vector: Optional[str] = None  # Ej: "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H"
    base_score: Optional[float] = None
    temporal_score: Optional[float] = None
    environmental_score: Optional[float] = None

class ContextInfo(BaseModel):
    """Información contextual de la detección"""
    commit_hash: Optional[str] = None
    branch: Optional[str] = None
    author: Optional[str] = None
    repository_url: Optional[str] = None
    scan_date: Optional[datetime] = None

class FindingIngestItem(BaseModel):
    """Item de vulnerabilidad con información completa para priorización"""
    # Información básica
    title: str
    description: Optional[str] = None
    severity: str  # CRITICAL, HIGH, MEDIUM, LOW, INFO

    # Clasificación
    cwe_id: Optional[str] = None
    owasp_top_10: Optional[str] = None  # Ej: "A01:2021-Broken Access Control"
    category: Optional[str] = None  # Ej: "Injection", "XSS", "Auth", etc.

    # Ubicación
    file_path: str
    line_number: int
    code_snippet: Optional[str] = None
    function_name: Optional[str] = None
    class_name: Optional[str] = None

    # Priorización
    cvss: Optional[CVSSInfo] = None
    confidence: Optional[float] = Field(None, ge=0.0, le=1.0)  # Confianza en la detección
    impact: Optional[str] = None  # HIGH, MEDIUM, LOW
    exploitability: Optional[str] = None  # HIGH, MEDIUM, LOW

    # Metadatos adicionales
    tags: Optional[List[str]] = None
    references: Optional[List[str]] = None  # URLs de referencia
    custom_fields: Optional[Dict[str, Any]] = None

    # Información de la herramienta
    tool: Optional[ScanToolInfo] = None

    # Contexto
    context: Optional[ContextInfo] = None

class FindingIngestRequest(BaseModel):
    """Request completo de ingestión"""
    tenant_id: str
    project_id: str
    scan_id: Optional[str] = None  # ID único del escaneo
    tool_info: Optional[ScanToolInfo] = None  # Info global de la herramienta
    context: Optional[ContextInfo] = None  # Contexto global
    findings: List[FindingIngestItem]

class FindingStatusUpdate(BaseModel):
    status: FindingStatus
    comment: Optional[str] = None
    assigned_to: Optional[str] = None
    due_date: Optional[datetime] = None

class FindingResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    tenant_id: str
    project_id: str
    scan_id: Optional[str]
    title: str
    description: Optional[str]
    severity: str
    cwe_id: Optional[str]
    owasp_top_10: Optional[str]
    category: Optional[str]
    file_path: str
    line_number: int
    code_snippet: Optional[str]
    function_name: Optional[str]
    class_name: Optional[str]
    cvss_vector: Optional[str]
    cvss_base_score: Optional[float]
    cvss_temporal_score: Optional[float]
    cvss_environmental_score: Optional[float]
    confidence: Optional[float]
    impact: Optional[str]
    exploitability: Optional[str]
    priority_score: Optional[float]
    tags: Optional[List[str]]
    references: Optional[List[str]]
    tool_name: Optional[str]
    tool_type: Optional[str]
    commit_hash: Optional[str]
    branch: Optional[str]
    author: Optional[str]
    status: FindingStatus
    assigned_to: Optional[str]
    due_date: Optional[datetime]
    created_at: datetime
    updated_at: datetime
