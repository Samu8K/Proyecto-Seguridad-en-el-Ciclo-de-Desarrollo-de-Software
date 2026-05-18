from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.db.session import get_db
from app.models.challenge import Challenge, UserProgress, Hint, Lesson, DifficultyLevel
from app.schemas.challenge import (
    ChallengeResponse, ChallengeCreate, ChallengeDetailResponse,
    UserProgressResponse, UserProgressCreate, LessonResponse, LessonCreate,
    DashboardStatsResponse, HintCreateSchema
)
from uuid import UUID
from datetime import datetime
from typing import List

router = APIRouter(prefix="/api/challenges", tags=["challenges"])

# ==================== CHALLENGES ====================

@router.get("/", response_model=List[ChallengeResponse])
async def get_challenges(
    difficulty: str = Query(None),
    vulnerability_type: str = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """Obtener lista de desafíos con filtros opcionales"""
    query = db.query(Challenge).filter(Challenge.is_active == True)
    
    if difficulty:
        query = query.filter(Challenge.difficulty == difficulty)
    if vulnerability_type:
        query = query.filter(Challenge.vulnerability_type == vulnerability_type)
    
    challenges = query.order_by(Challenge.difficulty_order).offset(skip).limit(limit).all()
    return challenges

@router.get("/by-difficulty", response_model=dict)
async def get_challenges_by_difficulty(db: Session = Depends(get_db)):
    """Obtener desafíos organizados por nivel de dificultad"""
    challenges = db.query(Challenge).filter(Challenge.is_active == True).all()
    
    result = {
        "BEGINNER": [],
        "INTERMEDIATE": [],
        "ADVANCED": []
    }
    
    for challenge in challenges:
        result[challenge.difficulty].append(ChallengeResponse.from_orm(challenge))
    
    return result

@router.get("/{challenge_id}", response_model=ChallengeDetailResponse)
async def get_challenge(challenge_id: UUID, db: Session = Depends(get_db)):
    """Obtener detalles completos de un desafío"""
    challenge = db.query(Challenge).filter(Challenge.id == challenge_id).first()
    
    if not challenge:
        raise HTTPException(status_code=404, detail="Challenge not found")
    
    hints = db.query(Hint).filter(Hint.challenge_id == challenge_id).order_by(Hint.level).all()
    
    result = ChallengeResponse.from_orm(challenge)
    return {**result.dict(), "hints": hints}

@router.post("/", response_model=ChallengeResponse)
async def create_challenge(challenge: ChallengeCreate, db: Session = Depends(get_db)):
    """Crear nuevo desafío (Admin)"""
    db_challenge = Challenge(**challenge.dict())
    db.add(db_challenge)
    db.commit()
    db.refresh(db_challenge)
    return db_challenge

@router.put("/{challenge_id}", response_model=ChallengeResponse)
async def update_challenge(
    challenge_id: UUID,
    challenge_update: dict,
    db: Session = Depends(get_db)
):
    """Actualizar desafío (Admin)"""
    db_challenge = db.query(Challenge).filter(Challenge.id == challenge_id).first()
    
    if not db_challenge:
        raise HTTPException(status_code=404, detail="Challenge not found")
    
    for key, value in challenge_update.items():
        if value is not None:
            setattr(db_challenge, key, value)
    
    db_challenge.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(db_challenge)
    return db_challenge

# ==================== HINTS ====================

@router.get("/{challenge_id}/hints", response_model=List[HintCreateSchema])
async def get_hints(challenge_id: UUID, db: Session = Depends(get_db)):
    """Obtener pistas de un desafío"""
    hints = db.query(Hint).filter(
        Hint.challenge_id == challenge_id
    ).order_by(Hint.level).all()
    
    return hints

@router.post("/{challenge_id}/hints", response_model=HintCreateSchema)
async def add_hint(
    challenge_id: UUID,
    hint: HintCreateSchema,
    db: Session = Depends(get_db)
):
    """Añadir pista a un desafío (Admin)"""
    db_hint = Hint(challenge_id=challenge_id, **hint.dict())
    db.add(db_hint)
    db.commit()
    db.refresh(db_hint)
    return db_hint

# ==================== USER PROGRESS ====================

@router.get("/user/{user_id}/progress", response_model=List[UserProgressResponse])
async def get_user_progress(user_id: str, db: Session = Depends(get_db)):
    """Obtener progreso del usuario en todos los desafíos"""
    progress_list = db.query(UserProgress).filter(
        UserProgress.user_id == user_id
    ).all()
    return progress_list

@router.get("/user/{user_id}/challenge/{challenge_id}/progress", response_model=UserProgressResponse)
async def get_challenge_progress(
    user_id: str,
    challenge_id: UUID,
    db: Session = Depends(get_db)
):
    """Obtener progreso en un desafío específico"""
    progress = db.query(UserProgress).filter(
        UserProgress.user_id == user_id,
        UserProgress.challenge_id == challenge_id
    ).first()
    
    if not progress:
        raise HTTPException(status_code=404, detail="Progress not found")
    
    return progress

@router.post("/user/{user_id}/challenge/{challenge_id}/start", response_model=UserProgressResponse)
async def start_challenge(
    user_id: str,
    challenge_id: UUID,
    db: Session = Depends(get_db)
):
    """Comenzar un desafío"""
    # Verificar que el desafío existe
    challenge = db.query(Challenge).filter(Challenge.id == challenge_id).first()
    if not challenge:
        raise HTTPException(status_code=404, detail="Challenge not found")
    
    # Verificar si ya existe progreso
    existing_progress = db.query(UserProgress).filter(
        UserProgress.user_id == user_id,
        UserProgress.challenge_id == challenge_id
    ).first()
    
    if existing_progress:
        return existing_progress
    
    # Crear nuevo progreso
    progress = UserProgress(user_id=user_id, challenge_id=challenge_id)
    db.add(progress)
    db.commit()
    db.refresh(progress)
    return progress

@router.post("/user/{user_id}/challenge/{challenge_id}/submit")
async def submit_answer(
    user_id: str,
    challenge_id: UUID,
    submission: dict,
    db: Session = Depends(get_db)
):
    """Enviar respuesta a un desafío"""
    progress = db.query(UserProgress).filter(
        UserProgress.user_id == user_id,
        UserProgress.challenge_id == challenge_id
    ).first()
    
    if not progress:
        raise HTTPException(status_code=404, detail="Progress not found")
    
    challenge = db.query(Challenge).filter(Challenge.id == challenge_id).first()
    
    # Actualizar progreso
    progress.attempts += 1
    progress.user_answer = submission.get("answer", "")
    
    # Validación simple (en producción esto sería más sofisticado)
    if submission.get("answer", "").lower() in challenge.expected_result.lower() if challenge.expected_result else False:
        progress.is_correct = True
        progress.is_completed = True
        progress.completed_at = datetime.utcnow()
    
    db.commit()
    db.refresh(progress)
    
    return {
        "progress": UserProgressResponse.from_orm(progress),
        "is_correct": progress.is_correct,
        "message": "Correcto! Excelente trabajo." if progress.is_correct else "Intenta de nuevo. Recuerda revisar las pistas."
    }

@router.post("/user/{user_id}/challenge/{challenge_id}/request-hint")
async def request_hint(
    user_id: str,
    challenge_id: UUID,
    db: Session = Depends(get_db)
):
    """Solicitar una pista para un desafío"""
    progress = db.query(UserProgress).filter(
        UserProgress.user_id == user_id,
        UserProgress.challenge_id == challenge_id
    ).first()
    
    if not progress:
        raise HTTPException(status_code=404, detail="Progress not found")
    
    # Obtener siguiente pista
    hint = db.query(Hint).filter(
        Hint.challenge_id == challenge_id,
        Hint.level == progress.hints_requested + 1
    ).first()
    
    if not hint:
        return {
            "message": "No hay más pistas disponibles",
            "hint": None
        }
    
    progress.hints_requested += 1
    db.commit()
    
    return {
        "message": f"Pista {progress.hints_requested}",
        "hint": HintCreateSchema.from_orm(hint)
    }

# ==================== LESSONS ====================

@router.get("/lessons", response_model=List[LessonResponse])
async def get_lessons(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """Obtener lecciones educativas"""
    lessons = db.query(Lesson).order_by(Lesson.order).offset(skip).limit(limit).all()
    return lessons

@router.get("/lessons/{lesson_id}", response_model=LessonResponse)
async def get_lesson(lesson_id: UUID, db: Session = Depends(get_db)):
    """Obtener detalles de una lección"""
    lesson = db.query(Lesson).filter(Lesson.id == lesson_id).first()
    
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")
    
    return lesson

@router.post("/lessons", response_model=LessonResponse)
async def create_lesson(lesson: LessonCreate, db: Session = Depends(get_db)):
    """Crear nueva lección (Admin)"""
    db_lesson = Lesson(**lesson.dict())
    db.add(db_lesson)
    db.commit()
    db.refresh(db_lesson)
    return db_lesson

# ==================== DASHBOARD STATS ====================

@router.get("/stats/dashboard", response_model=DashboardStatsResponse)
async def get_dashboard_stats(db: Session = Depends(get_db)):
    """Obtener estadísticas del dashboard"""
    total_challenges = db.query(func.count(Challenge.id)).scalar()
    
    # Por dificultad
    by_difficulty = {}
    for diff in ["BEGINNER", "INTERMEDIATE", "ADVANCED"]:
        count = db.query(func.count(Challenge.id)).filter(Challenge.difficulty == diff).scalar()
        by_difficulty[diff] = count
    
    # Por tipo de vulnerabilidad
    by_vuln_type = {}
    vuln_types = db.query(Challenge.vulnerability_type).distinct().all()
    for (vuln_type,) in vuln_types:
        count = db.query(func.count(Challenge.id)).filter(Challenge.vulnerability_type == vuln_type).scalar()
        by_vuln_type[vuln_type] = count
    
    # Usuarios únicos
    total_users = db.query(func.count(func.distinct(UserProgress.user_id))).scalar()
    
    # Completaciones
    total_completions = db.query(func.count(UserProgress.id)).filter(UserProgress.is_completed == True).scalar()
    
    # Tasa de éxito
    total_attempts = db.query(func.count(UserProgress.id)).scalar()
    success_rate = (total_completions / total_attempts * 100) if total_attempts > 0 else 0
    
    return {
        "total_challenges": total_challenges,
        "challenges_by_difficulty": by_difficulty,
        "total_users": total_users,
        "total_completions": total_completions,
        "average_success_rate": round(success_rate, 2),
        "challenges_by_vulnerability_type": by_vuln_type
    }

@router.get("/stats/user/{user_id}")
async def get_user_stats(user_id: str, db: Session = Depends(get_db)):
    """Obtener estadísticas personales del usuario"""
    total_attempts = db.query(func.count(UserProgress.id)).filter(
        UserProgress.user_id == user_id
    ).scalar()
    
    completed = db.query(func.count(UserProgress.id)).filter(
        UserProgress.user_id == user_id,
        UserProgress.is_completed == True
    ).scalar()
    
    success_rate = (completed / total_attempts * 100) if total_attempts > 0 else 0
    
    return {
        "total_attempts": total_attempts,
        "completed": completed,
        "success_rate": round(success_rate, 2)
    }
