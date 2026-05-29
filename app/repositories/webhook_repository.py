from sqlalchemy.orm import Session

from app.models.webhook_event import ProcessedWebhookEvent


class WebhookRepository:
    def __init__(self, db: Session):
        self.db = db

    def event_exists(self, event_id: str) -> bool:
        return (
            self.db.query(ProcessedWebhookEvent)
            .filter(ProcessedWebhookEvent.event_id == event_id)
            .first()
            is not None
        )

    def register_event(self, event: ProcessedWebhookEvent) -> ProcessedWebhookEvent:
        self.db.add(event)
        self.db.commit()
        self.db.refresh(event)
        return event
