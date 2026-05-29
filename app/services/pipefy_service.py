from app.core.logging import get_logger
from app.integrations.pipefy.graphql_client import PipefyGraphQLClient
from app.integrations.pipefy.mutations import (
    PIPEFY_DEFAULT_PIPE_ID,
    build_create_card_input,
    build_update_card_field_input,
)

logger = get_logger(__name__)


class PipefyService:
    def __init__(self):
        self.client = PipefyGraphQLClient()

    def build_create_card_payload(
        self,
        pipe_id: str | None,
        nome: str,
        email: str,
        tipo_solicitacao: str,
        valor_patrimonio: float,
    ) -> dict:
        pid = pipe_id or PIPEFY_DEFAULT_PIPE_ID
        input_data = build_create_card_input(
            pipe_id=pid,
            nome=nome,
            email=email,
            tipo_solicitacao=tipo_solicitacao,
            valor_patrimonio=valor_patrimonio,
        )
        payload = {
            "query": (
                "mutation CreateCard($input: CreateCardInput!) {"
                " createCard(input: $input) { card { id title created_at } }"
                " }"
            ),
            "variables": {"input": input_data},
        }
        self.client.simulate_request(payload)
        return payload

    def build_update_card_field_payload(
        self,
        card_id: str,
        field_id: str,
        new_value: str,
    ) -> dict:
        input_data = build_update_card_field_input(
            card_id=card_id,
            field_id=field_id,
            new_value=new_value,
        )
        payload = {
            "query": (
                "mutation UpdateCardField($input: UpdateCardFieldInput!) {"
                " updateCardField(input: $input) { card { id } success }"
                " }"
            ),
            "variables": {"input": input_data},
        }
        self.client.simulate_request(payload)
        return payload
