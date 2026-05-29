from fastapi import Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.services.client_service import ClientService
from app.services.webhook_service import WebhookService


def get_client_service(db: Session = Depends(get_db)) -> ClientService:
    return ClientService(db)


def get_webhook_service(db: Session = Depends(get_db)) -> WebhookService:
    return WebhookService(db)
