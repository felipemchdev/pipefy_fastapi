from app.core.config import settings
from app.core.logging import get_logger

logger = get_logger(__name__)


class PipefyGraphQLClient:

    def __init__(self, api_url: str | None = None, api_token: str | None = None):
        self.api_url = api_url or settings.PIPEFY_API_URL
        self.api_token = api_token or settings.PIPEFY_API_TOKEN

    def build_card_payload(
        self,
        pipe_id: str,
        nome: str,
        email: str,
        tipo_solicitacao: str,
        valor_patrimonio: float,
    ) -> dict:
        return {
            "query": """mutation CreateCard($input: CreateCardInput!) {
  createCard(input: $input) {
    card {
      id
      title
      created_at
    }
  }
}""",
            "variables": {
                "input": {
                    "pipe_id": pipe_id,
                    "title": f"{nome} - {tipo_solicitacao}",
                    "fields_attributes": [
                        {"field_id": "cliente_email", "field_value": email},
                        {"field_id": "valor_patrimonio", "field_value": str(valor_patrimonio)},
                        {"field_id": "tipo_solicitacao", "field_value": tipo_solicitacao},
                    ],
                }
            },
        }

    def build_update_card_field_payload(
        self,
        card_id: str,
        field_id: str,
        new_value: str,
    ) -> dict:
        return {
            "query": """mutation UpdateCardField($input: UpdateCardFieldInput!) {
  updateCardField(input: $input) {
    card {
      id
    }
    success
  }
}""",
            "variables": {
                "input": {
                    "card_id": card_id,
                    "field_id": field_id,
                    "new_value": new_value,
                }
            },
        }

    def simulate_request(self, payload: dict) -> None:
        logger.info(
            "Simulating Pipefy GraphQL request",
            extra={"api_url": self.api_url, "payload": payload},
        )
