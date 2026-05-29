from sqlalchemy.orm import Session

from app.core.exceptions import ClientNotFoundException, DuplicateWebhookEventException
from app.core.logging import get_logger
from app.integrations.pipefy.graphql_client import PipefyGraphQLClient
from app.models.webhook_event import ProcessedWebhookEvent
from app.repositories.webhook_repository import WebhookRepository
from app.schemas.webhook import CardUpdatedWebhook
from app.services.client_service import ClientService

logger = get_logger(__name__)

PRIORITY_THRESHOLD = 200_000.0


class WebhookService:
    def __init__(self, db: Session):
        self.webhook_repository = WebhookRepository(db)
        self.client_service = ClientService(db)
        self.pipefy_client = PipefyGraphQLClient()

    def process_card_updated(self, webhook: CardUpdatedWebhook) -> dict:
        if self.webhook_repository.event_exists(webhook.event_id):
            logger.warning(f"Duplicate webhook event detected: {webhook.event_id}")
            raise DuplicateWebhookEventException(webhook.event_id)

        client = self.client_service.get_client_by_email(webhook.cliente_email)
        if not client:
            raise ClientNotFoundException(email=webhook.cliente_email)

        client.prioridade = (
            "alta" if client.valor_patrimonio >= PRIORITY_THRESHOLD else "normal"
        )

        client.status = "Processado"
        self.client_service.update_client(client)
        logger.info(
            f"Client {client.id} updated: priority={client.prioridade}, status={client.status}"
        )

        event = ProcessedWebhookEvent(
            event_id=webhook.event_id,
            card_id=webhook.card_id,
        )
        self.webhook_repository.register_event(event)
        logger.info(f"Webhook event registered: {webhook.event_id}")

        pipefy_update_payload = self.pipefy_client.build_update_card_field_payload(
            card_id=webhook.card_id,
            field_id="prioridade",
            new_value=client.prioridade or "",
        )
        self.pipefy_client.simulate_request(pipefy_update_payload)

        status_payload = self.pipefy_client.build_update_card_field_payload(
            card_id=webhook.card_id,
            field_id="status",
            new_value=client.status,
        )
        self.pipefy_client.simulate_request(status_payload)

        return {
            "message": "Webhook processed successfully",
            "event_id": webhook.event_id,
            "client_id": client.id,
            "prioridade": client.prioridade or "",
            "pipefy_update_payload": {
                "prioridade_update": pipefy_update_payload,
                "status_update": status_payload,
            },
        }
