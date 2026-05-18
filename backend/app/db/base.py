from sqlalchemy.orm import DeclarativeBase
from app.models.finding import Finding
from app.models.challenge import Challenge, UserProgress, Hint, Lesson

class Base(DeclarativeBase):
    pass

