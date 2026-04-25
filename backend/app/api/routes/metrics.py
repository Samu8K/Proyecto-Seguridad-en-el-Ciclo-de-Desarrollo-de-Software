from fastapi import APIRouter, Depends
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.deps import get_db, get_current_user
from app.models.finding import Finding, FindingStatus
from app.models.user import User

router = APIRouter(prefix="/metrics", tags=["metrics"])

@router.get("/dashboard")
async def dashboard_metrics(db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
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

@router.get("/findings")
async def list_findings(
    skip: int = 0,
    limit: int = 50,
    status: FindingStatus = None,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    query = select(Finding)
    if status:
        query = query.where(Finding.status == status)
    query = query.offset(skip).limit(limit).order_by(Finding.created_at.desc())
    result = await db.execute(query)
    findings = result.scalars().all()
    return findings
