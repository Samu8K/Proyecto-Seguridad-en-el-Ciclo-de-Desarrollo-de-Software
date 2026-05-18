import uuid
from datetime import datetime
from sqlalchemy import String, Integer, DateTime, Enum, ForeignKey, Float, Text, Boolean, Index, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base
import enum

class DifficultyLevel(str, enum.Enum):
    BEGINNER = "BEGINNER"
    INTERMEDIATE = "INTERMEDIATE"
    ADVANCED = "ADVANCED"

class VulnerabilityType(str, enum.Enum):
    SQL_INJECTION = "SQL_INJECTION"
    XSS = "XSS"
    CSRF = "CSRF"
    BROKEN_AUTH = "BROKEN_AUTH"
    IDOR = "IDOR"
    INSECURE_DESERIALIZE = "INSECURE_DESERIALIZE"
    COMMAND_INJECTION = "COMMAND_INJECTION"
    XXE = "XXE"
    INSECURE_CRYPTOGRAPHY = "INSECURE_CRYPTOGRAPHY"
    PATH_TRAVERSAL = "PATH_TRAVERSAL"

class AttackType(str, enum.Enum):
    INJECTION = "INJECTION"
    CROSS_SITE = "CROSS_SITE"
    AUTHENTICATION = "AUTHENTICATION"
    AUTHORIZATION = "AUTHORIZATION"
    SERIALIZATION = "SERIALIZATION"
    CRYPTO = "CRYPTO"
    TRAVERSAL = "TRAVERSAL"

class Challenge(Base):
    __tablename__ = "challenges"
    __table_args__ = (
        Index('idx_difficulty', 'difficulty'),
        Index('idx_vulnerability_type', 'vulnerability_type'),
    )

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    title: Mapped[str] = mapped_column(String(255), index=True)
    short_title: Mapped[str] = mapped_column(String(100))
    description: Mapped[str] = mapped_column(Text)
    difficulty: Mapped[DifficultyLevel] = mapped_column(Enum(DifficultyLevel))
    vulnerability_type: Mapped[VulnerabilityType] = mapped_column(Enum(VulnerabilityType))
    attack_type: Mapped[AttackType] = mapped_column(Enum(AttackType))
    
    # Contenido educativo detallado
    vulnerability_explanation: Mapped[str] = mapped_column(Text)
    attack_explanation: Mapped[str] = mapped_column(Text)
    real_world_impact: Mapped[str] = mapped_column(Text)
    countermeasures: Mapped[str] = mapped_column(Text)
    best_practices: Mapped[str] = mapped_column(Text)
    learning_objectives: Mapped[str] = mapped_column(Text)
    references: Mapped[str] = mapped_column(Text)
    
    # Código vulnerable
    vulnerable_code: Mapped[str] = mapped_column(Text)
    vulnerable_code_language: Mapped[str] = mapped_column(String(50))
    vulnerable_code_explanation: Mapped[str] = mapped_column(Text)
    
    # Código seguro
    secure_code: Mapped[str] = mapped_column(Text)
    secure_code_language: Mapped[str] = mapped_column(String(50))
    secure_code_explanation: Mapped[str] = mapped_column(Text)
    
    # Información técnica
    cvss_score: Mapped[float] = mapped_column(Float)
    owasp_top_10: Mapped[str] = mapped_column(String(10))
    cwe_id: Mapped[str] = mapped_column(String(20))
    cwe_description: Mapped[str] = mapped_column(Text)
    
    # Pistas progresivas
    hint_1: Mapped[str] = mapped_column(Text)
    hint_2: Mapped[str] = mapped_column(Text)
    hint_3: Mapped[str] = mapped_column(Text)
    
    # Test endpoint
    test_endpoint: Mapped[str] = mapped_column(String(255))
    test_payload: Mapped[str] = mapped_column(Text)
    expected_result: Mapped[str] = mapped_column(Text)
    
    # Metadatos visuales
    difficulty_order: Mapped[int] = mapped_column(Integer, default=0)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    icon: Mapped[str] = mapped_column(String(50), default="🔓")
    color: Mapped[str] = mapped_column(String(20), default="red")
    
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relaciones
    user_progress = relationship("UserProgress", backref="challenge", cascade="all, delete-orphan")



class UserProgress(Base):
    __tablename__ = "user_progress"
    __table_args__ = (
        Index('idx_user_challenge', 'user_id', 'challenge_id'),
    )

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    user_id: Mapped[str] = mapped_column(String(255), index=True)
    challenge_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("challenges.id"))
    
    # Progreso
    is_completed: Mapped[bool] = mapped_column(Boolean, default=False)
    attempts: Mapped[int] = mapped_column(Integer, default=0)
    hints_used: Mapped[int] = mapped_column(Integer, default=0)
    
    # Respuesta del usuario
    user_answer: Mapped[str] = mapped_column(Text)
    is_correct: Mapped[bool] = mapped_column(Boolean, default=False)
    score: Mapped[int] = mapped_column(Integer, default=0)
    
    # Tiempos
    started_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    completed_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    time_spent_seconds: Mapped[int] = mapped_column(Integer, default=0)
    
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Lesson(Base):
    __tablename__ = "lessons"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    title: Mapped[str] = mapped_column(String(255), index=True)
    description: Mapped[str] = mapped_column(Text)
    content: Mapped[str] = mapped_column(Text)
    
    difficulty: Mapped[DifficultyLevel] = mapped_column(Enum(DifficultyLevel))
    
    # Contenido educativo
    key_concepts: Mapped[str] = mapped_column(Text)
    code_examples: Mapped[str] = mapped_column(Text)
    video_url: Mapped[str] = mapped_column(String(500))
    
    order: Mapped[int] = mapped_column(Integer, default=0)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    
    # Relaciones
    user_progress = relationship("UserLessonProgress", backref="lesson", cascade="all, delete-orphan")


class UserLessonProgress(Base):
    __tablename__ = "user_lesson_progress"
    __table_args__ = (
        Index('idx_user_lesson', 'user_id', 'lesson_id'),
    )

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    user_id: Mapped[str] = mapped_column(String(255), index=True)
    lesson_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("lessons.id"))
    
    is_completed: Mapped[bool] = mapped_column(Boolean, default=False)
    completed_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    content: Mapped[str] = mapped_column(Text)
    level: Mapped[int] = mapped_column(Integer, default=1)  # 1, 2, 3... progresivo
    
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

class Lesson(Base):
    __tablename__ = "lessons"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    title: Mapped[str] = mapped_column(String(255), index=True)
    description: Mapped[str] = mapped_column(Text)
    content: Mapped[str] = mapped_column(Text)
    order: Mapped[int] = mapped_column(Integer)
    difficulty: Mapped[DifficultyLevel] = mapped_column(Enum(DifficultyLevel))
    
    # Multimedia
    video_url: Mapped[str | None] = mapped_column(String(500))
    image_url: Mapped[str | None] = mapped_column(String(500))
    
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
