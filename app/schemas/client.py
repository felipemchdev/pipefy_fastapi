from datetime import datetime

from pydantic import BaseModel, EmailStr, Field


class ClientCreateRequest(BaseModel):
    cliente_nome: str = Field(..., min_length=2, max_length=255)
    cliente_email: EmailStr
    tipo_solicitacao: str = Field(..., min_length=2, max_length=100)
    valor_patrimonio: float = Field(..., ge=0.0)


class ClientResponse(BaseModel):
    id: str
    nome: str
    email: str
    tipo_solicitacao: str
    valor_patrimonio: float
    status: str
    prioridade: str | None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class ClientCreateResponse(BaseModel):
    message: str
    client_id: str
    pipefy_card_payload: dict
