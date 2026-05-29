def test_webhook_priority_high(client):
    create_payload = {
        "cliente_nome": "Carlos Alta",
        "cliente_email": "carlos.alta@example.com",
        "tipo_solicitacao": "Atualizacao cadastral",
        "valor_patrimonio": 300000,
    }
    create_resp = client.post("/clientes", json=create_payload)
    assert create_resp.status_code == 201

    webhook_payload = {
        "event_id": "evt_high_001",
        "card_id": "card_high_001",
        "cliente_email": "carlos.alta@example.com",
        "timestamp": "2026-05-18T12:00:00Z",
    }
    response = client.post("/webhooks/pipefy/card-updated", json=webhook_payload)
    assert response.status_code == 200
    data = response.json()
    assert data["prioridade"] == "alta"
    assert data["message"] == "Webhook processed successfully"


def test_webhook_priority_normal(client):
    create_payload = {
        "cliente_nome": "Ana Normal",
        "cliente_email": "ana.normal@example.com",
        "tipo_solicitacao": "Consulta",
        "valor_patrimonio": 50000,
    }
    create_resp = client.post("/clientes", json=create_payload)
    assert create_resp.status_code == 201

    webhook_payload = {
        "event_id": "evt_normal_001",
        "card_id": "card_normal_001",
        "cliente_email": "ana.normal@example.com",
        "timestamp": "2026-05-18T14:00:00Z",
    }
    response = client.post("/webhooks/pipefy/card-updated", json=webhook_payload)
    assert response.status_code == 200
    data = response.json()
    assert data["prioridade"] == "normal"


def test_webhook_priority_exactly_threshold(client):
    create_payload = {
        "cliente_nome": "Exato Limiar",
        "cliente_email": "exato.limiar@example.com",
        "tipo_solicitacao": "Atualizacao",
        "valor_patrimonio": 200000,
    }
    create_resp = client.post("/clientes", json=create_payload)
    assert create_resp.status_code == 201

    webhook_payload = {
        "event_id": "evt_exact_001",
        "card_id": "card_exact_001",
        "cliente_email": "exato.limiar@example.com",
        "timestamp": "2026-05-18T15:00:00Z",
    }
    response = client.post("/webhooks/pipefy/card-updated", json=webhook_payload)
    assert response.status_code == 200
    data = response.json()
    assert data["prioridade"] == "alta"


def test_webhook_client_not_found(client):
    payload = {
        "event_id": "evt_notfound_001",
        "card_id": "card_nf",
        "cliente_email": "notfound@example.com",
        "timestamp": "2026-05-18T12:00:00Z",
    }
    response = client.post("/webhooks/pipefy/card-updated", json=payload)
    assert response.status_code == 404
