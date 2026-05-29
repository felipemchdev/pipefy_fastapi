from datetime import datetime

from pydantic import BaseModel, EmailStr, Field


class CardUpdatedWebhook(BaseModel):
    event_id: str = Field(..., min_length=1)
    card_id: str = Field(..., min_length=1)
    cliente_email: EmailStr
    timestamp: datetime


class WebhookProcessResponse(BaseModel):
    message: str
    event_id: str
    client_id: str
    prioridade: str
    pipefy_update_payload: dict
