import hashlib
from datetime import datetime, timezone
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.finding import Finding, FindingStatus
from app.services.scoring import RiskScoringService
from app.services.correlation import CorrelationService
from app.services.ml.fp_detector import FalsePositiveDetector
from app.services.event_service import EventService
from app.realtime.ws_manager import manager
import logging

logger = logging.getLogger(__name__)

class IngestionService:
    def __init__(self, fp_model=None):
        self.fp_model = fp_model or FalsePositiveDetector()

    def _generate_fingerprint(self, project_id: str, finding: dict) -> str:
        payload = f"{project_id}|{finding.get('cwe_id')}|{finding.get('file_path')}|{finding.get('code_snippet', '')}"
        return hashlib.sha256(payload.encode()).hexdigest()

    async def process_report(self, db: AsyncSession, tenant_id: str, project_id: str, findings: list) -> dict:
        stats = {"inserted": 0, "updated": 0, "false_positives": 0}
        for f in findings:
            fp = self._generate_fingerprint(project_id, f)
            is_fp = await self.fp_model.predict(f)
            status = FindingStatus.FALSE_POSITIVE if is_fp else FindingStatus.OPEN
            if is_fp:
                stats["false_positives"] += 1

            cvss = RiskScoringService.calculate(f["severity"])
            corr_id = CorrelationService.generate_group(f)

            stmt = insert(Finding).values(
                tenant_id=tenant_id,
                project_id=project_id,
                fingerprint=fp,
                title=f["title"],
                severity=f["severity"],
                cwe_id=f.get("cwe_id"),
                file_path=f["file_path"],
                line_number=f["line_number"],
                metadata=f,
                status=status,
                cvss_score=cvss
            ).on_conflict_do_update(
                index_elements=["fingerprint"],
                set_={
                    "status": FindingStatus.OPEN,
                    "updated_at": datetime.now(timezone.utc)
                }
            )
            result = await db.execute(stmt)
            stats["inserted" if result.rowcount == 1 else "updated"] += 1

            await EventService.publish(db, "FINDING_PROCESSED", f)
            await manager.broadcast({"type": "NEW_FINDING", "data": {**f, "cvss_score": cvss, "status": status.value}})

        await db.commit()
        logger.info(f"Ingestion stats: {stats}")
        return stats
