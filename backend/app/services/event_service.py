from app.models.event import Event
from sqlalchemy.ext.asyncio import AsyncSession

class EventService:
    @staticmethod
    async def publish(db: AsyncSession, event_type: str, payload: dict):
        event = Event(type=event_type, payload=payload)
        db.add(event)
        await db.flush()
