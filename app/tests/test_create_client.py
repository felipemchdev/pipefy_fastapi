def test_create_client_success(client):
    payload = {
        "cliente_nome": "Joao Silva",
        "cliente_email": "joao.silva@example.com",
        "tipo_solicitacao": "Atualizacao cadastral",
        "valor_patrimonio": 250000,
    }

    response = client.post("/clientes", json=payload)

    assert response.status_code == 201
    data = response.json()
    assert data["message"] == "Client successfully created"
    assert data["client_id"] is not None
    assert "pipefy_card_payload" in data
    assert data["pipefy_card_payload"]["variables"]["input"]["pipe_id"] is not None


def test_create_client_initial_status(client):
    from app.tests.conftest import TestingSessionLocal
    from app.models.client import Client

    payload = {
        "cliente_nome": "Maria Souza",
        "cliente_email": "maria.souza@example.com",
        "tipo_solicitacao": "Abertura de conta",
        "valor_patrimonio": 50000,
    }

    response = client.post("/clientes", json=payload)
    assert response.status_code == 201

    db = TestingSessionLocal()
    db_client = db.query(Client).first()
    assert db_client.status == "Aguardando Analise"
    db.close()


def test_create_client_invalid_email(client):
    payload = {
        "cliente_nome": "Teste",
        "cliente_email": "invalid-email",
        "tipo_solicitacao": "Teste",
        "valor_patrimonio": 100,
    }
    response = client.post("/clientes", json=payload)
    assert response.status_code == 422


def test_create_client_negative_patrimonio(client):
    payload = {
        "cliente_nome": "Teste",
        "cliente_email": "teste@example.com",
        "tipo_solicitacao": "Teste",
        "valor_patrimonio": -100,
    }
    response = client.post("/clientes", json=payload)
    assert response.status_code == 422
