from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from uuid import UUID
from enum import Enum

class DifficultyLevel(str, Enum):
    BEGINNER = "BEGINNER"
    INTERMEDIATE = "INTERMEDIATE"
    ADVANCED = "ADVANCED"

class VulnerabilityType(str, Enum):
    SQL_INJECTION = "SQL_INJECTION"
    XSS = "XSS"
    CSRF = "CSRF"
    BROKEN_AUTH = "BROKEN_AUTH"
    IDOR = "IDOR"
    SECURITY_MISCONFIGURATION = "SECURITY_MISCONFIGURATION"
    SENSITIVE_DATA_EXPOSURE = "SENSITIVE_DATA_EXPOSURE"
    XXE = "XXE"
    BROKEN_ACCESS_CONTROL = "BROKEN_ACCESS_CONTROL"
    COMPONENTS_WITH_KNOWN_VULN = "COMPONENTS_WITH_KNOWN_VULN"
    INSUFFICIENT_LOGGING_MONITORING = "INSUFFICIENT_LOGGING_MONITORING"
    COMMAND_INJECTION = "COMMAND_INJECTION"
    PATH_TRAVERSAL = "PATH_TRAVERSAL"
    DESERIALIZATION = "DESERIALIZATION"
    WEAK_CRYPTOGRAPHY = "WEAK_CRYPTOGRAPHY"

class AttackType(str, Enum):
    INJECTION = "INJECTION"
    CROSS_SITE = "CROSS_SITE"
    AUTHENTICATION = "AUTHENTICATION"
    AUTHORIZATION = "AUTHORIZATION"
    CONFIGURATION = "CONFIGURATION"
    CRYPTOGRAPHY = "CRYPTOGRAPHY"
    LOGIC = "LOGIC"
    SERIALIZATION = "SERIALIZATION"

class HintSchema(BaseModel):
    id: UUID
    title: str
    content: str
    level: int

    class Config:
        from_attributes = True

class HintCreateSchema(BaseModel):
    title: str
    content: str
    level: int = 1

class ChallengeBase(BaseModel):
    title: str
    description: str
    difficulty: DifficultyLevel
    vulnerability_type: VulnerabilityType
    attack_type: AttackType
    vulnerability_explanation: str
    attack_explanation: str
    countermeasures: str
    vulnerable_code: str
    vulnerable_code_language: str
    secure_code: str
    secure_code_language: str
    cvss_score: Optional[float] = None
    owasp_top_10: str
    cwe_id: Optional[str] = None
    test_endpoint: Optional[str] = None
    test_payload: Optional[str] = None
    expected_result: Optional[str] = None
    references: Optional[str] = None
    difficulty_order: int = 0
    is_active: bool = True

class ChallengeCreate(ChallengeBase):
    pass

class ChallengeUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    difficulty: Optional[DifficultyLevel] = None
    is_active: Optional[bool] = None
    vulnerability_explanation: Optional[str] = None
    attack_explanation: Optional[str] = None
    countermeasures: Optional[str] = None

class ChallengeResponse(ChallengeBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class ChallengeDetailResponse(ChallengeResponse):
    hints: list[HintSchema] = []

class UserProgressCreate(BaseModel):
    user_id: str
    challenge_id: UUID
    user_answer: Optional[str] = None

class UserProgressResponse(BaseModel):
    id: UUID
    user_id: str
    challenge_id: UUID
    is_completed: bool
    attempts: int
    hints_requested: int
    is_correct: bool
    started_at: datetime
    completed_at: Optional[datetime] = None
    time_spent_seconds: Optional[int] = None

    class Config:
        from_attributes = True

class UserProgressUpdate(BaseModel):
    user_answer: Optional[str] = None
    attempts: Optional[int] = None
    hints_requested: Optional[int] = None
    is_correct: Optional[bool] = None

class LessonBase(BaseModel):
    title: str
    description: str
    content: str
    order: int
    difficulty: DifficultyLevel
    video_url: Optional[str] = None
    image_url: Optional[str] = None

class LessonCreate(LessonBase):
    pass

class LessonResponse(LessonBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class DashboardStatsResponse(BaseModel):
    total_challenges: int
    challenges_by_difficulty: dict
    total_users: int
    total_completions: int
    average_success_rate: float
    challenges_by_vulnerability_type: dict
