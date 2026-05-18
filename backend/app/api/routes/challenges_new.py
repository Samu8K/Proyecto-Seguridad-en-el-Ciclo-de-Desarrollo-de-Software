"""
API Routes para Secure Coding Dojo - Desafíos Educativos
Proporciona endpoints para obtener desafíos, gestionar progreso y estadísticas
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.db.session import get_db
from app.models.challenge import (
    Challenge, UserProgress, Lesson, UserLessonProgress, 
    DifficultyLevel, VulnerabilityType
)
from uuid import UUID
from datetime import datetime
from typing import List, Dict, Any
import json

router = APIRouter(prefix="/api/challenges", tags=["challenges"])

# ==================== CHALLENGES ====================

@router.get("/")
async def get_all_challenges(
    difficulty: str = Query(None),
    vulnerability_type: str = Query(None),
    db: Session = Depends(get_db)
):
    """Obtener lista de todos los desafíos con filtros opcionales"""
    query = db.query(Challenge).filter(Challenge.is_active == True)
    
    if difficulty:
        query = query.filter(Challenge.difficulty == difficulty)
    if vulnerability_type:
        query = query.filter(Challenge.vulnerability_type == vulnerability_type)
    
    challenges = query.order_by(Challenge.difficulty_order).all()
    
    return {
        "total": len(challenges),
        "challenges": [
            {
                "id": str(c.id),
                "title": c.title,
                "short_title": c.short_title,
                "description": c.description,
                "difficulty": c.difficulty,
                "vulnerability_type": c.vulnerability_type,
                "icon": c.icon,
                "color": c.color,
                "cvss_score": c.cvss_score,
                "owasp_top_10": c.owasp_top_10,
            }
            for c in challenges
        ]
    }

@router.get("/by-difficulty")
async def get_challenges_by_difficulty(db: Session = Depends(get_db)):
    """Obtener desafíos organizados por nivel de dificultad"""
    challenges = db.query(Challenge).filter(Challenge.is_active == True).all()
    
    result = {
        "BEGINNER": [],
        "INTERMEDIATE": [],
        "ADVANCED": []
    }
    
    for challenge in challenges:
        challenge_data = {
            "id": str(challenge.id),
            "title": challenge.title,
            "short_title": challenge.short_title,
            "description": challenge.description,
            "difficulty": challenge.difficulty,
            "vulnerability_type": challenge.vulnerability_type,
            "icon": challenge.icon,
            "color": challenge.color,
            "cvss_score": challenge.cvss_score,
            "owasp_top_10": challenge.owasp_top_10,
        }
        result[challenge.difficulty].append(challenge_data)
    
    return result

@router.get("/{challenge_id}")
async def get_challenge_details(
    challenge_id: UUID,
    db: Session = Depends(get_db)
):
    """Obtener detalles completos de un desafío educativo"""
    challenge = db.query(Challenge).filter(Challenge.id == challenge_id).first()
    
    if not challenge:
        raise HTTPException(status_code=404, detail="Challenge not found")
    
    return {
        "id": str(challenge.id),
        "title": challenge.title,
        "short_title": challenge.short_title,
        "description": challenge.description,
        "difficulty": challenge.difficulty,
        "vulnerability_type": challenge.vulnerability_type,
        "attack_type": challenge.attack_type,
        "icon": challenge.icon,
        "color": challenge.color,
        
        # Contenido educativo completo
        "vulnerability_explanation": challenge.vulnerability_explanation,
        "attack_explanation": challenge.attack_explanation,
        "real_world_impact": challenge.real_world_impact,
        "countermeasures": challenge.countermeasures,
        "best_practices": challenge.best_practices,
        "learning_objectives": challenge.learning_objectives,
        "references": challenge.references,
        
        # Código
        "vulnerable_code": challenge.vulnerable_code,
        "vulnerable_code_language": challenge.vulnerable_code_language,
        "vulnerable_code_explanation": challenge.vulnerable_code_explanation,
        "secure_code": challenge.secure_code,
        "secure_code_language": challenge.secure_code_language,
        "secure_code_explanation": challenge.secure_code_explanation,
        
        # Información técnica
        "cvss_score": challenge.cvss_score,
        "owasp_top_10": challenge.owasp_top_10,
        "cwe_id": challenge.cwe_id,
        "cwe_description": challenge.cwe_description,
        
        # Pistas progresivas
        "hints": {
            "level_1": challenge.hint_1,
            "level_2": challenge.hint_2,
            "level_3": challenge.hint_3,
        }
    }

# ==================== USER PROGRESS ====================

@router.post("/progress/start")
async def start_challenge(
    challenge_id: UUID,
    user_id: str,
    db: Session = Depends(get_db)
):
    """Registrar que un usuario inició un desafío"""
    
    # Verificar que desafío existe
    challenge = db.query(Challenge).filter(Challenge.id == challenge_id).first()
    if not challenge:
        raise HTTPException(status_code=404, detail="Challenge not found")
    
    # Buscar progreso existente
    progress = db.query(UserProgress).filter(
        UserProgress.user_id == user_id,
        UserProgress.challenge_id == challenge_id
    ).first()
    
    # Si existe, devolver el existente
    if progress:
        return {
            "id": str(progress.id),
            "status": "resumed",
            "attempts": progress.attempts,
            "hints_used": progress.hints_used,
        }
    
    # Crear nuevo progreso
    progress = UserProgress(
        user_id=user_id,
        challenge_id=challenge_id,
        started_at=datetime.utcnow(),
        attempts=0,
        hints_used=0,
        user_answer="",
        time_spent_seconds=0
    )
    
    db.add(progress)
    db.commit()
    db.refresh(progress)
    
    return {
        "id": str(progress.id),
        "status": "started",
        "attempts": 0,
        "hints_used": 0,
    }

@router.post("/progress/submit-answer")
async def submit_answer(
    challenge_id: UUID,
    user_id: str,
    answer: str,
    time_spent: int,
    db: Session = Depends(get_db)
):
    """Enviar respuesta para un desafío"""
    
    # Obtener progreso
    progress = db.query(UserProgress).filter(
        UserProgress.user_id == user_id,
        UserProgress.challenge_id == challenge_id
    ).first()
    
    if not progress:
        raise HTTPException(status_code=404, detail="Progress not found")
    
    # Incrementar intentos
    progress.attempts += 1
    progress.user_answer = answer
    progress.time_spent_seconds = time_spent
    
    # Marcar como completado (simplificado - en producción sería más complejo)
    progress.is_completed = True
    progress.completed_at = datetime.utcnow()
    progress.is_correct = True  # El usuario lo completa si lo entiende
    progress.score = max(100 - (progress.attempts * 10), 10)  # Puntuación basada en intentos
    
    db.commit()
    db.refresh(progress)
    
    return {
        "id": str(progress.id),
        "status": "submitted",
        "attempts": progress.attempts,
        "is_completed": progress.is_completed,
        "score": progress.score,
        "message": "¡Desafío completado! Felicidades por tu aprendizaje."
    }

@router.get("/progress/{user_id}")
async def get_user_progress(
    user_id: str,
    db: Session = Depends(get_db)
):
    """Obtener progreso del usuario en todos los desafíos"""
    
    progress_list = db.query(UserProgress).filter(
        UserProgress.user_id == user_id
    ).all()
    
    completed = len([p for p in progress_list if p.is_completed])
    total = db.query(Challenge).filter(Challenge.is_active == True).count()
    
    return {
        "user_id": user_id,
        "completed_challenges": completed,
        "total_challenges": total,
        "completion_percentage": round((completed / total * 100) if total > 0 else 0, 1),
        "total_score": sum([p.score for p in progress_list if p.is_completed]),
        "progress": [
            {
                "challenge_id": str(p.challenge_id),
                "is_completed": p.is_completed,
                "attempts": p.attempts,
                "hints_used": p.hints_used,
                "score": p.score,
                "time_spent_seconds": p.time_spent_seconds,
            }
            for p in progress_list
        ]
    }

@router.get("/progress/{user_id}/{challenge_id}")
async def get_challenge_progress(
    user_id: str,
    challenge_id: UUID,
    db: Session = Depends(get_db)
):
    """Obtener progreso del usuario en un desafío específico"""
    
    progress = db.query(UserProgress).filter(
        UserProgress.user_id == user_id,
        UserProgress.challenge_id == challenge_id
    ).first()
    
    if not progress:
        return {
            "status": "not_started",
            "attempts": 0,
            "hints_used": 0,
            "is_completed": False,
        }
    
    return {
        "status": "in_progress" if not progress.is_completed else "completed",
        "attempts": progress.attempts,
        "hints_used": progress.hints_used,
        "is_completed": progress.is_completed,
        "score": progress.score,
        "time_spent_seconds": progress.time_spent_seconds,
    }

@router.post("/progress/use-hint")
async def use_hint(
    challenge_id: UUID,
    user_id: str,
    hint_level: int,  # 1, 2, o 3
    db: Session = Depends(get_db)
):
    """Registrar que un usuario usó una pista"""
    
    progress = db.query(UserProgress).filter(
        UserProgress.user_id == user_id,
        UserProgress.challenge_id == challenge_id
    ).first()
    
    if not progress:
        raise HTTPException(status_code=404, detail="Progress not found")
    
    # Obtener pista
    challenge = db.query(Challenge).filter(Challenge.id == challenge_id).first()
    
    hint_map = {
        1: challenge.hint_1,
        2: challenge.hint_2,
        3: challenge.hint_3,
    }
    
    if hint_level not in hint_map:
        raise HTTPException(status_code=400, detail="Invalid hint level")
    
    progress.hints_used += 1
    db.commit()
    
    return {
        "hint": hint_map[hint_level],
        "hint_level": hint_level,
        "total_hints_used": progress.hints_used,
    }

# ==================== STATISTICS ====================

@router.get("/stats/global")
async def get_global_statistics(db: Session = Depends(get_db)):
    """Obtener estadísticas globales de todos los usuarios"""
    
    total_users = db.query(func.count(func.distinct(UserProgress.user_id))).scalar()
    total_completions = db.query(func.count(UserProgress.id)).filter(
        UserProgress.is_completed == True
    ).scalar()
    total_attempts = db.query(func.sum(UserProgress.attempts)).scalar() or 0
    total_hints_used = db.query(func.sum(UserProgress.hints_used)).scalar() or 0
    
    # Desafíos más intentados
    most_attempted = db.query(
        Challenge.title,
        func.count(UserProgress.id).label('count')
    ).join(
        UserProgress, Challenge.id == UserProgress.challenge_id
    ).group_by(Challenge.id).order_by(func.count(UserProgress.id).desc()).limit(5).all()
    
    # Tasa de éxito por dificultad
    success_by_difficulty = {}
    for difficulty in ['BEGINNER', 'INTERMEDIATE', 'ADVANCED']:
        total = db.query(func.count(UserProgress.id)).join(
            Challenge, UserProgress.challenge_id == Challenge.id
        ).filter(Challenge.difficulty == difficulty).scalar() or 0
        
        completed = db.query(func.count(UserProgress.id)).filter(
            Challenge.difficulty == difficulty,
            UserProgress.is_completed == True
        ).scalar() or 0
        
        success_by_difficulty[difficulty] = {
            "total_attempts": total,
            "completed": completed,
            "success_rate": round((completed / total * 100) if total > 0 else 0, 1)
        }
    
    return {
        "total_users": total_users or 0,
        "total_completions": total_completions or 0,
        "total_attempts": total_attempts,
        "total_hints_used": total_hints_used,
        "average_attempts_per_challenge": round((total_attempts / (total_completions or 1)), 1),
        "most_attempted_challenges": [
            {"title": title, "attempts": count}
            for title, count in most_attempted
        ],
        "success_by_difficulty": success_by_difficulty,
    }

# ==================== LESSONS ====================

@router.get("/lessons/")
async def get_all_lessons(
    difficulty: str = Query(None),
    db: Session = Depends(get_db)
):
    """Obtener todas las lecciones disponibles"""
    
    query = db.query(Lesson).filter(Lesson.is_active == True)
    
    if difficulty:
        query = query.filter(Lesson.difficulty == difficulty)
    
    lessons = query.order_by(Lesson.order).all()
    
    return {
        "total": len(lessons),
        "lessons": [
            {
                "id": str(l.id),
                "title": l.title,
                "description": l.description,
                "difficulty": l.difficulty,
                "order": l.order,
            }
            for l in lessons
        ]
    }

@router.get("/lessons/{lesson_id}")
async def get_lesson_details(
    lesson_id: UUID,
    db: Session = Depends(get_db)
):
    """Obtener detalles completos de una lección"""
    
    lesson = db.query(Lesson).filter(Lesson.id == lesson_id).first()
    
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")
    
    return {
        "id": str(lesson.id),
        "title": lesson.title,
        "description": lesson.description,
        "content": lesson.content,
        "difficulty": lesson.difficulty,
        "key_concepts": lesson.key_concepts,
        "code_examples": lesson.code_examples,
        "video_url": lesson.video_url,
        "order": lesson.order,
    }

@router.post("/lessons/{lesson_id}/complete")
async def complete_lesson(
    lesson_id: UUID,
    user_id: str,
    db: Session = Depends(get_db)
):
    """Marcar una lección como completada"""
    
    # Verificar que lección existe
    lesson = db.query(Lesson).filter(Lesson.id == lesson_id).first()
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")
    
    # Buscar progreso
    progress = db.query(UserLessonProgress).filter(
        UserLessonProgress.user_id == user_id,
        UserLessonProgress.lesson_id == lesson_id
    ).first()
    
    if progress:
        progress.is_completed = True
        progress.completed_at = datetime.utcnow()
    else:
        progress = UserLessonProgress(
            user_id=user_id,
            lesson_id=lesson_id,
            is_completed=True,
            completed_at=datetime.utcnow()
        )
        db.add(progress)
    
    db.commit()
    
    return {
        "status": "completed",
        "lesson_id": str(lesson_id),
        "completed_at": progress.completed_at.isoformat(),
    }

# ==================== HEALTH CHECK ====================

@router.get("/health")
async def health_check():
    """Health check del API"""
    return {"status": "ok", "service": "challenges"}
