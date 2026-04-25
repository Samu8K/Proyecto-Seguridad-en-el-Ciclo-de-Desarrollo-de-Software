from pydantic import BaseModel
from typing import Optional, List, Dict
from uuid import UUID
from datetime import datetime
from app.models.finding import FindingStatus

class FindingIngestItem(BaseModel):
    title: str
    severity: str
    cwe_id: Optional[str] = None
    file_path: str
    line_number: int
    code_snippet: Optional[str] = None

class FindingIngestRequest(BaseModel):
    tenant_id: str
    project_id: str
    findings: List[FindingIngestItem]

class FindingResponse(BaseModel):
    id: UUID
    tenant_id: str
    project_id: str
    title: str
    severity: str
    cvss_score: Optional[float]
    file_path: str
    line_number: int
    status: FindingStatus
    created_at: datetime
    updated_at: datetime
