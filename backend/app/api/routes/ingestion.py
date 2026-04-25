from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.deps import get_db, get_current_user
from app.services.ingestion import IngestionService
from app.schemas.finding import FindingIngestRequest
from app.models.user import User

router = APIRouter(prefix="/ingest", tags=["ingestion"])

@router.post("/", status_code=202)
async def ingest_findings(
    payload: FindingIngestRequest,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.tenant_id != payload.tenant_id and current_user.role != "admin":
        raise HTTPException(403, "Not authorized for this tenant")

    service = IngestionService()
    # Para respuesta rápida, ejecutar en background si es pesado, pero aquí lo hacemos directo
    result = await service.process_report(db, payload.tenant_id, payload.project_id, payload.findings)
    return {"status": "accepted", "stats": result}
