def test_webhook_idempotency_blocks_duplicate(client):
    create_payload = {
        "cliente_nome": "Duplo Silva",
        "cliente_email": "duplo.silva@example.com",
        "tipo_solicitacao": "Atualizacao cadastral",
        "valor_patrimonio": 250000,
    }
    client.post("/clientes", json=create_payload)

    webhook_payload = {
        "event_id": "evt_duplicate_001",
        "card_id": "card_dup",
        "cliente_email": "duplo.silva@example.com",
        "timestamp": "2026-05-18T12:00:00Z",
    }

    first = client.post("/webhooks/pipefy/card-updated", json=webhook_payload)
    assert first.status_code == 200

    second = client.post("/webhooks/pipefy/card-updated", json=webhook_payload)
    assert second.status_code == 409
    assert "already been processed" in second.json()["detail"]


def test_different_event_ids_same_client_ok(client):
    create_payload = {
        "cliente_nome": "Multi Eventos",
        "cliente_email": "multi.eventos@example.com",
        "tipo_solicitacao": "Atualizacao",
        "valor_patrimonio": 150000,
    }
    client.post("/clientes", json=create_payload)

    payload_a = {
        "event_id": "evt_a",
        "card_id": "card_a",
        "cliente_email": "multi.eventos@example.com",
        "timestamp": "2026-05-18T10:00:00Z",
    }

    payload_b = {
        "event_id": "evt_b",
        "card_id": "card_b",
        "cliente_email": "multi.eventos@example.com",
        "timestamp": "2026-05-18T11:00:00Z",
    }

    r1 = client.post("/webhooks/pipefy/card-updated", json=payload_a)
    assert r1.status_code == 200

    r2 = client.post("/webhooks/pipefy/card-updated", json=payload_b)
    assert r2.status_code == 200
