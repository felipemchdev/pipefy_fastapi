from fastapi import APIRouter, Depends

from app.schemas.client import ClientCreateRequest, ClientCreateResponse
from app.services.client_service import ClientService
from app.api.dependencies import get_client_service

router = APIRouter(prefix="/clientes", tags=["Clients"])


@router.post("", response_model=ClientCreateResponse, status_code=201)
def create_client(
    payload: ClientCreateRequest,
    service: ClientService = Depends(get_client_service),
) -> dict:
    return service.create_client(payload)
