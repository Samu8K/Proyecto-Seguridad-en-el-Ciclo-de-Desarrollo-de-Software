from datetime import datetime
from uuid import UUID
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.models.finding import Finding, FindingHistory, FindingStatus
from app.schemas.finding import FindingResponse, FindingStatusUpdate

router = APIRouter(prefix="/metrics", tags=["metrics"])

@router.get("/dashboard")
async def dashboard_metrics(db: AsyncSession = Depends(get_db)):
    total_query = select(func.count()).select_from(Finding)
    total = await db.scalar(total_query)

    open_query = select(func.count()).where(Finding.status == FindingStatus.OPEN)
    open_count = await db.scalar(open_query)

    in_progress_query = select(func.count()).where(Finding.status == FindingStatus.IN_PROGRESS)
    in_progress = await db.scalar(in_progress_query)

    resolved_query = select(func.count()).where(Finding.status == FindingStatus.RESOLVED)
    resolved = await db.scalar(resolved_query)

    by_severity = {}
    for sev in ["CRITICAL", "HIGH", "MEDIUM", "LOW"]:
        cnt = await db.scalar(select(func.count()).where(Finding.severity == sev))
        by_severity[sev] = cnt

    return {
        "total": total,
        "open": open_count,
        "in_progress": in_progress,
        "resolved": resolved,
        "by_severity": by_severity
    }

@router.get("/findings", response_model=List[FindingResponse])
async def list_findings(
    skip: int = 0,
    limit: int = 50,
    status: FindingStatus = None,
    db: AsyncSession = Depends(get_db)
):
    query = select(Finding)
    if status:
        query = query.where(Finding.status == status)
    query = query.offset(skip).limit(limit).order_by(Finding.created_at.desc())
    result = await db.execute(query)
    findings = result.scalars().all()
    return findings

@router.patch("/findings/{finding_id}/status", response_model=FindingResponse)
async def update_finding_status(
    finding_id: UUID,
    payload: FindingStatusUpdate,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(Finding).where(Finding.id == finding_id))
    finding = result.scalar_one_or_none()
    if not finding:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Finding not found")

    old_status = finding.status
    finding.status = payload.status
    finding.updated_at = datetime.utcnow()

    history = FindingHistory(
        finding_id=finding.id,
        action="status_update",
        old_value={"status": old_status.value},
        new_value={"status": payload.status.value},
        changed_by="system"
    )
    db.add(history)

    await db.commit()
    await db.refresh(finding)
    return finding
