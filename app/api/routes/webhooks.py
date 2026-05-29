from fastapi import APIRouter, Depends

from app.schemas.webhook import CardUpdatedWebhook, WebhookProcessResponse
from app.services.webhook_service import WebhookService
from app.api.dependencies import get_webhook_service

router = APIRouter(prefix="/webhooks/pipefy", tags=["Webhooks"])


@router.post(
    "/card-updated",
    response_model=WebhookProcessResponse,
    responses={
        409: {"description": "Duplicate webhook event"},
        404: {"description": "Client not found"},
    },
)
def card_updated_webhook(
    payload: CardUpdatedWebhook,
    service: WebhookService = Depends(get_webhook_service),
) -> dict:
    return service.process_card_updated(payload)
