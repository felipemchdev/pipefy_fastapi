import uuid
from datetime import datetime

from sqlalchemy import Column, DateTime, String, func

from app.core.database import Base


class ProcessedWebhookEvent(Base):
    __tablename__ = "processed_webhook_events"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    event_id = Column(String(255), unique=True, nullable=False, index=True)
    card_id = Column(String(255), nullable=False)
    processed_at = Column(DateTime, server_default=func.now())

    def __repr__(self) -> str:
        return f"<ProcessedWebhookEvent(event_id={self.event_id})>"
