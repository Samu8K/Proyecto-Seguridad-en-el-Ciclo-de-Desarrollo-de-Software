import argparse
import asyncio
from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4

# Add the parent directory to the path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings
from app.db.base import Base
from app.models.finding import Finding, FindingHistory, FindingStatus

sample_findings = [
    {
        "title": "SQL Injection en formulario de login",
        "severity": "CRITICAL",
        "cwe_id": "CWE-89",
        "file_path": "src/auth/login.py",
        "line_number": 42,
        "cvss_score": 9.8,
    },
    {
        "title": "XSS en comentarios de usuarios",
        "severity": "HIGH",
        "cwe_id": "CWE-79",
        "file_path": "src/components/comments.jsx",
        "line_number": 156,
        "cvss_score": 7.2,
    },
    {
        "title": "Contraseña hardcodeada en configuración",
        "severity": "HIGH",
        "cwe_id": "CWE-798",
        "file_path": "src/config/database.py",
        "line_number": 8,
        "cvss_score": 8.1,
    },
    {
        "title": "Falta validación de entrada en API de reportes",
        "severity": "MEDIUM",
        "cwe_id": "CWE-20",
        "file_path": "src/api/reports.py",
        "line_number": 73,
        "cvss_score": 6.5,
    },
    {
        "title": "Información sensible en logs",
        "severity": "MEDIUM",
        "cwe_id": "CWE-532",
        "file_path": "src/utils/logger.py",
        "line_number": 31,
        "cvss_score": 5.3,
    },
    {
        "title": "Dependencia vulnerable en package.json",
        "severity": "LOW",
        "cwe_id": "CWE-1104",
        "file_path": "package.json",
        "line_number": 15,
        "cvss_score": 3.7,
    },
]


def create_engine():
    return create_async_engine(settings.DATABASE_URL)


async def init_db() -> None:
    engine = create_engine()
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("✅ Database tables created successfully.")


async def seed_data() -> None:
    engine = create_engine()
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    async with async_session() as db:
        for data in sample_findings:
            finding = Finding(
                id=uuid4(),
                tenant_id="default",
                project_id="aspm-demo",
                title=data["title"],
                severity=data["severity"],
                cwe_id=data["cwe_id"],
                file_path=data["file_path"],
                line_number=data["line_number"],
                fingerprint=f"{data['file_path']}:{data['line_number']}",
                hash_version=1,
                extra_data=data,
                status=FindingStatus.OPEN,
                cvss_base_score=data["cvss_score"],  # Updated field name
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow(),
            )
            db.add(finding)
        await db.commit()

    print(f"✅ {len(sample_findings)} vulnerabilidades de ejemplo agregadas!")


async def main() -> None:
    parser = argparse.ArgumentParser(description="Manage backend database tasks")
    parser.add_argument("command", choices=["init-db", "seed"], help="Tarea a ejecutar")
    args = parser.parse_args()

    if args.command == "init-db":
        await init_db()
    elif args.command == "seed":
        await seed_data()


if __name__ == "__main__":
    asyncio.run(main())
