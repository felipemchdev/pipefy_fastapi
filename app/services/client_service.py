from sqlalchemy.orm import Session

from app.core.logging import get_logger
from app.integrations.pipefy.graphql_client import PipefyGraphQLClient
from app.integrations.pipefy.mutations import PIPEFY_DEFAULT_PIPE_ID
from app.models.client import Client
from app.repositories.client_repository import ClientRepository
from app.schemas.client import ClientCreateRequest

logger = get_logger(__name__)


class ClientService:
    def __init__(self, db: Session):
        self.repository = ClientRepository(db)
        self.pipefy_client = PipefyGraphQLClient()

    def create_client(self, request: ClientCreateRequest) -> dict:
        client = Client(
            nome=request.cliente_nome,
            email=request.cliente_email,
            tipo_solicitacao=request.tipo_solicitacao,
            valor_patrimonio=request.valor_patrimonio,
            status="Aguardando Analise",
        )

        created = self.repository.create(client)
        logger.info(f"Client created: {created.id} - {created.nome}")

        pipefy_payload = self.pipefy_client.build_card_payload(
            pipe_id=PIPEFY_DEFAULT_PIPE_ID,
            nome=created.nome,
            email=created.email,
            tipo_solicitacao=created.tipo_solicitacao,
            valor_patrimonio=created.valor_patrimonio,
        )

        self.pipefy_client.simulate_request(pipefy_payload)

        return {
            "message": "Client successfully created",
            "client_id": created.id,
            "pipefy_card_payload": pipefy_payload,
        }

    def get_client_by_email(self, email: str) -> Client | None:
        return self.repository.get_by_email(email)

    def update_client(self, client: Client) -> Client:
        return self.repository.update(client)
