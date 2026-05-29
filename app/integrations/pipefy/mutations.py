PIPEFY_CREATE_CARD_MUTATION = """mutation CreateCard($input: CreateCardInput!) {
  createCard(input: $input) {
    card {
      id
      title
      created_at
    }
  }
}"""

PIPEFY_UPDATE_CARD_FIELD_MUTATION = """mutation UpdateCardField($input: UpdateCardFieldInput!) {
  updateCardField(input: $input) {
    card {
      id
    }
    success
  }
}"""

PIPEFY_DEFAULT_PIPE_ID = "304497"


def build_create_card_input(
    pipe_id: str,
    nome: str,
    email: str,
    tipo_solicitacao: str,
    valor_patrimonio: float,
) -> dict:
    return {
        "pipe_id": pipe_id,
        "title": f"{nome} - {tipo_solicitacao}",
        "fields_attributes": [
            {"field_id": "cliente_email", "field_value": email},
            {"field_id": "valor_patrimonio", "field_value": str(valor_patrimonio)},
            {"field_id": "tipo_solicitacao", "field_value": tipo_solicitacao},
        ],
    }


def build_update_card_field_input(
    card_id: str,
    field_id: str,
    new_value: str,
) -> dict:
    return {
        "card_id": card_id,
        "field_id": field_id,
        "new_value": new_value,
    }
