"""
Servicio de Ejercicios - Gestión completa de ejercicios educativos
Proporciona lógica para crear, recuperar, validar y evaluar ejercicios
"""

from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.challenge import Challenge, UserProgress, DifficultyLevel, VulnerabilityType
from uuid import UUID
from datetime import datetime
import json


class ExerciseService:
    """Servicio para gestionar ejercicios educativos"""
    
    @staticmethod
    def get_all_exercises(
        db: Session,
        difficulty: Optional[str] = None,
        vulnerability_type: Optional[str] = None,
        is_active: bool = True
    ) -> List[Challenge]:
        """Obtener todos los ejercicios con filtros opcionales"""
        query = db.query(Challenge).filter(Challenge.is_active == is_active)
        
        if difficulty:
            query = query.filter(Challenge.difficulty == difficulty)
        if vulnerability_type:
            query = query.filter(Challenge.vulnerability_type == vulnerability_type)
        
        return query.order_by(Challenge.difficulty_order).all()
    
    @staticmethod
    def get_exercise_by_id(db: Session, exercise_id: UUID) -> Optional[Challenge]:
        """Obtener un ejercicio específico por ID"""
        return db.query(Challenge).filter(Challenge.id == exercise_id).first()
    
    @staticmethod
    def get_exercise_details(db: Session, exercise_id: UUID) -> Optional[Dict[str, Any]]:
        """
        Obtener detalles completos de un ejercicio para educación
        Incluye explicaciones, código y pistas
        """
        exercise = ExerciseService.get_exercise_by_id(db, exercise_id)
        if not exercise:
            return None
        
        return {
            "id": str(exercise.id),
            "title": exercise.title,
            "short_title": exercise.short_title,
            "description": exercise.description,
            "difficulty": exercise.difficulty,
            "vulnerability_type": exercise.vulnerability_type,
            "attack_type": exercise.attack_type,
            
            # Educación
            "vulnerability_explanation": exercise.vulnerability_explanation,
            "attack_explanation": exercise.attack_explanation,
            "real_world_impact": exercise.real_world_impact,
            "countermeasures": exercise.countermeasures,
            "best_practices": exercise.best_practices,
            "learning_objectives": exercise.learning_objectives,
            
            # Código
            "vulnerable_code": exercise.vulnerable_code,
            "vulnerable_code_language": exercise.vulnerable_code_language,
            "vulnerable_code_explanation": exercise.vulnerable_code_explanation,
            "secure_code": exercise.secure_code,
            "secure_code_language": exercise.secure_code_language,
            "secure_code_explanation": exercise.secure_code_explanation,
            
            # Técnica
            "cvss_score": exercise.cvss_score,
            "owasp_top_10": exercise.owasp_top_10,
            "cwe_id": exercise.cwe_id,
            "cwe_description": exercise.cwe_description,
            
            # Visualización
            "icon": exercise.icon,
            "color": exercise.color,
            "references": exercise.references,
        }
    
    @staticmethod
    def get_exercises_by_difficulty(db: Session) -> Dict[str, List[Dict[str, Any]]]:
        """Obtener ejercicios organizados por nivel de dificultad"""
        exercises = ExerciseService.get_all_exercises(db)
        
        result = {
            "BEGINNER": [],
            "INTERMEDIATE": [],
            "ADVANCED": []
        }
        
        for exercise in exercises:
            exercise_data = {
                "id": str(exercise.id),
                "title": exercise.title,
                "short_title": exercise.short_title,
                "description": exercise.description,
                "difficulty": exercise.difficulty,
                "vulnerability_type": exercise.vulnerability_type,
                "icon": exercise.icon,
                "color": exercise.color,
                "cvss_score": exercise.cvss_score,
                "owasp_top_10": exercise.owasp_top_10,
            }
            result[exercise.difficulty].append(exercise_data)
        
        return result
    
    @staticmethod
    def get_exercises_by_vulnerability_type(db: Session) -> Dict[str, List[Dict[str, Any]]]:
        """Obtener ejercicios organizados por tipo de vulnerabilidad"""
        exercises = ExerciseService.get_all_exercises(db)
        
        result = {}
        for exercise in exercises:
            vuln_type = exercise.vulnerability_type
            if vuln_type not in result:
                result[vuln_type] = []
            
            exercise_data = {
                "id": str(exercise.id),
                "title": exercise.title,
                "difficulty": exercise.difficulty,
                "cvss_score": exercise.cvss_score,
                "icon": exercise.icon,
            }
            result[vuln_type].append(exercise_data)
        
        return result
    
    @staticmethod
    def get_owasp_top_10_summary(db: Session) -> Dict[str, Any]:
        """Obtener resumen de OWASP Top 10 cubierto en los ejercicios"""
        exercises = ExerciseService.get_all_exercises(db)
        
        owasp_coverage = {}
        for exercise in exercises:
            owasp = exercise.owasp_top_10
            if owasp not in owasp_coverage:
                owasp_coverage[owasp] = {
                    "count": 0,
                    "vulnerabilities": [],
                    "severity": exercise.cvss_score
                }
            owasp_coverage[owasp]["count"] += 1
            owasp_coverage[owasp]["vulnerabilities"].append(exercise.vulnerability_type)
        
        return owasp_coverage
    
    @staticmethod
    def get_user_progress_on_exercise(
        db: Session, 
        user_id: str, 
        exercise_id: UUID
    ) -> Optional[Dict[str, Any]]:
        """Obtener progreso del usuario en un ejercicio específico"""
        progress = db.query(UserProgress).filter(
            UserProgress.user_id == user_id,
            UserProgress.challenge_id == exercise_id
        ).first()
        
        if not progress:
            return None
        
        return {
            "is_completed": progress.is_completed,
            "attempts": progress.attempts,
            "hints_used": progress.hints_used,
            "score": progress.score,
            "time_spent_seconds": progress.time_spent_seconds,
            "is_correct": progress.is_correct,
            "started_at": progress.started_at.isoformat(),
            "completed_at": progress.completed_at.isoformat() if progress.completed_at else None,
        }
    
    @staticmethod
    def get_user_all_progress(db: Session, user_id: str) -> Dict[str, Any]:
        """Obtener progreso del usuario en todos los ejercicios"""
        progress_list = db.query(UserProgress).filter(
            UserProgress.user_id == user_id
        ).all()
        
        stats = {
            "total_attempted": len(progress_list),
            "total_completed": sum(1 for p in progress_list if p.is_completed),
            "total_correct": sum(1 for p in progress_list if p.is_correct),
            "total_hints_used": sum(p.hints_used for p in progress_list),
            "total_time_seconds": sum(p.time_spent_seconds for p in progress_list),
            "average_score": sum(p.score for p in progress_list) / len(progress_list) if progress_list else 0,
            "exercises": []
        }
        
        for progress in progress_list:
            stats["exercises"].append({
                "exercise_id": str(progress.challenge_id),
                "is_completed": progress.is_completed,
                "score": progress.score,
                "attempts": progress.attempts,
            })
        
        return stats
    
    @staticmethod
    def create_user_progress(
        db: Session,
        user_id: str,
        exercise_id: UUID
    ) -> UserProgress:
        """Crear registro de progreso para un usuario"""
        progress = UserProgress(
            user_id=user_id,
            challenge_id=exercise_id,
            started_at=datetime.utcnow()
        )
        db.add(progress)
        db.commit()
        return progress
    
    @staticmethod
    def update_user_progress(
        db: Session,
        user_id: str,
        exercise_id: UUID,
        **updates
    ) -> Optional[UserProgress]:
        """Actualizar progreso del usuario"""
        progress = db.query(UserProgress).filter(
            UserProgress.user_id == user_id,
            UserProgress.challenge_id == exercise_id
        ).first()
        
        if not progress:
            return None
        
        for key, value in updates.items():
            if hasattr(progress, key):
                setattr(progress, key, value)
        
        progress.updated_at = datetime.utcnow()
        db.commit()
        return progress
    
    @staticmethod
    def record_hint_usage(
        db: Session,
        user_id: str,
        exercise_id: UUID,
        hint_number: int
    ) -> Optional[UserProgress]:
        """Registrar uso de pista"""
        progress = db.query(UserProgress).filter(
            UserProgress.user_id == user_id,
            UserProgress.challenge_id == exercise_id
        ).first()
        
        if not progress:
            return None
        
        progress.hints_used = max(hint_number, progress.hints_used)
        progress.updated_at = datetime.utcnow()
        db.commit()
        return progress
    
    @staticmethod
    def complete_exercise(
        db: Session,
        user_id: str,
        exercise_id: UUID,
        is_correct: bool,
        score: int
    ) -> Optional[UserProgress]:
        """Marcar ejercicio como completado"""
        progress = db.query(UserProgress).filter(
            UserProgress.user_id == user_id,
            UserProgress.challenge_id == exercise_id
        ).first()
        
        if not progress:
            return None
        
        progress.is_completed = True
        progress.is_correct = is_correct
        progress.score = score
        progress.completed_at = datetime.utcnow()
        progress.updated_at = datetime.utcnow()
        
        db.commit()
        return progress
    
    @staticmethod
    def get_leaderboard(db: Session, limit: int = 10) -> List[Dict[str, Any]]:
        """Obtener tabla de posiciones de usuarios"""
        users_stats = db.query(
            UserProgress.user_id,
            func.count(UserProgress.id).label("total_attempts"),
            func.sum(func.cast(UserProgress.is_completed, type_=int)).label("completed"),
            func.avg(UserProgress.score).label("avg_score"),
            func.sum(UserProgress.time_spent_seconds).label("total_time")
        ).group_by(UserProgress.user_id).order_by(
            func.sum(func.cast(UserProgress.is_completed, type_=int)).desc(),
            func.avg(UserProgress.score).desc()
        ).limit(limit).all()
        
        leaderboard = []
        for rank, stat in enumerate(users_stats, 1):
            leaderboard.append({
                "rank": rank,
                "user_id": stat.user_id,
                "completed": stat.completed or 0,
                "average_score": float(stat.avg_score or 0),
                "total_time_seconds": stat.total_time or 0,
            })
        
        return leaderboard
    
    @staticmethod
    def get_difficulty_distribution(db: Session, user_id: str) -> Dict[str, int]:
        """Obtener distribución de intentos por dificultad"""
        results = db.query(
            Challenge.difficulty,
            func.count(UserProgress.id).label("count")
        ).join(
            UserProgress, Challenge.id == UserProgress.challenge_id
        ).filter(
            UserProgress.user_id == user_id
        ).group_by(Challenge.difficulty).all()
        
        return {result[0]: result[1] for result in results}
