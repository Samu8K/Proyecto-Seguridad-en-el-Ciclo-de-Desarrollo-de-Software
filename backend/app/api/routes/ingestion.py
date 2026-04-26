import hashlib
from datetime import datetime, timezone
from typing import Optional

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.models.finding import Finding, FindingStatus
from app.schemas.finding import FindingIngestRequest

router = APIRouter(prefix="/ingest", tags=["ingestion"])

SEVERITY_TO_CVSS = {
    "CRITICAL": 9.8,
    "HIGH": 7.2,
    "MEDIUM": 5.0,
    "LOW": 3.0,
    "INFO": 1.0,
}

IMPACT_WEIGHTS = {
    "CRITICAL": 1.0,
    "HIGH": 0.8,
    "MEDIUM": 0.6,
    "LOW": 0.3,
    "INFO": 0.1,
}

EXPLOITABILITY_WEIGHTS = {
    "HIGH": 1.0,
    "MEDIUM": 0.7,
    "LOW": 0.3,
}

TOOL_TYPE_WEIGHTS = {
    "SAST": 0.8,    # Alta confianza en SAST
    "DAST": 0.9,    # Alta confianza en DAST
    "SCA": 0.7,     # Buena confianza en SCA
    "IAST": 1.0,    # Máxima confianza en IAST
}

def _calculate_priority_score(
    severity: str,
    cvss_score: float | None,
    confidence: float | None,
    impact: str | None,
    exploitability: str | None,
    tool_type: str | None
) -> float:
    """Calcula un score de prioridad basado en múltiples factores"""

    # Base score de severidad
    base_score = SEVERITY_TO_CVSS.get(severity.upper(), 1.0)

    # Si hay CVSS específico, úsalo como base
    if cvss_score:
        base_score = cvss_score

    # Factor de impacto
    impact_factor = IMPACT_WEIGHTS.get((impact or "").upper(), 0.5)

    # Factor de explotabilidad
    exploitability_factor = EXPLOITABILITY_WEIGHTS.get((exploitability or "").upper(), 0.5)

    # Factor de confianza de la herramienta
    tool_factor = TOOL_TYPE_WEIGHTS.get((tool_type or "").upper(), 0.5)

    # Factor de confianza en la detección
    confidence_factor = confidence if confidence is not None else 0.8

    # Score final: combina todos los factores
    priority_score = (
        base_score * 0.4 +           # 40% severidad/CVSS
        impact_factor * 10 * 0.2 +   # 20% impacto
        exploitability_factor * 10 * 0.2 +  # 20% explotabilidad
        tool_factor * 10 * 0.1 +     # 10% confianza herramienta
        confidence_factor * 10 * 0.1 # 10% confianza detección
    )

    return round(priority_score, 2)


def _is_false_positive(file_path: str, severity: str, tool_type: Optional[str]) -> bool:
    """Determina si una vulnerabilidad es falso positivo"""
    path = file_path.lower()

    # Reglas básicas
    if "test" in path or "mock" in path:
        return True

    if severity.upper() == "INFO":
        return True

    # Para herramientas específicas
    if tool_type == "SCA" and "dev" in path:
        return True

    return False


@router.post("/", status_code=202)
async def ingest_findings(payload: FindingIngestRequest, db: AsyncSession = Depends(get_db)):
    stats = {"inserted": 0, "updated": 0, "false_positives": 0}

    for finding in payload.findings:
        # Determinar información de herramienta (global o específica)
        tool_info = finding.tool or payload.tool_info
        tool_name = tool_info.name if tool_info else None
        tool_type = tool_info.type if tool_info else None

        # Determinar contexto (global o específico)
        context_info = finding.context or payload.context

        # Calcular si es falso positivo
        status = FindingStatus.FALSE_POSITIVE if _is_false_positive(
            finding.file_path, finding.severity, tool_type
        ) else FindingStatus.OPEN

        if status == FindingStatus.FALSE_POSITIVE:
            stats["false_positives"] += 1

        # Calcular priority score inteligente
        cvss_score = finding.cvss.base_score if finding.cvss else None
        priority_score = _calculate_priority_score(
            finding.severity,
            cvss_score,
            finding.confidence,
            finding.impact,
            finding.exploitability,
            tool_type
        )

        fingerprint = hashlib.sha256(
            f"{payload.project_id}|{finding.cwe_id or ''}|{finding.file_path}|{finding.line_number}".encode()
        ).hexdigest()

        # Check if finding already exists
        existing = await db.execute(select(Finding).where(Finding.fingerprint == fingerprint))
        existing_finding = existing.scalar_one_or_none()

        if existing_finding:
            # Update existing finding
            existing_finding.status = FindingStatus.OPEN
            existing_finding.updated_at = datetime.now(timezone.utc)
            # Update priority score if improved
            if priority_score > (existing_finding.priority_score or 0):
                existing_finding.priority_score = priority_score
            stats["updated"] += 1
        else:
            # Create new finding with all metadata
            new_finding = Finding(
                tenant_id=payload.tenant_id,
                project_id=payload.project_id,
                scan_id=payload.scan_id,

                # Información básica
                title=finding.title,
                description=finding.description,
                severity=finding.severity,

                # Clasificación
                cwe_id=finding.cwe_id,
                owasp_top_10=finding.owasp_top_10,
                category=finding.category,

                # Ubicación
                file_path=finding.file_path,
                line_number=finding.line_number,
                code_snippet=finding.code_snippet,
                function_name=finding.function_name,
                class_name=finding.class_name,

                # Priorización
                cvss_vector=finding.cvss.vector if finding.cvss else None,
                cvss_base_score=cvss_score,
                cvss_temporal_score=finding.cvss.temporal_score if finding.cvss else None,
                cvss_environmental_score=finding.cvss.environmental_score if finding.cvss else None,
                confidence=finding.confidence,
                impact=finding.impact,
                exploitability=finding.exploitability,
                priority_score=priority_score,

                # Metadatos
                tags=finding.tags or [],
                references=finding.references or [],
                custom_fields=finding.custom_fields or {},

                # Información de herramienta
                tool_name=tool_name,
                tool_version=tool_info.version if tool_info else None,
                tool_type=tool_type,

                # Contexto
                commit_hash=context_info.commit_hash if context_info else None,
                branch=context_info.branch if context_info else None,
                author=context_info.author if context_info else None,
                repository_url=context_info.repository_url if context_info else None,
                scan_date=context_info.scan_date if context_info else None,

                # Estado
                fingerprint=fingerprint,
                status=status,
                extra_data=finding.model_dump(),
            )
            db.add(new_finding)
            stats["inserted"] += 1

    await db.commit()
    return {"status": "accepted", "stats": stats}
