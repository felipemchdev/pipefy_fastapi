# Client Management & Pipefy Integration

Backend desenvolvido com FastAPI para gerenciamento de clientes, processamento de webhooks e integração simulada com Pipefy via GraphQL.

O projeto foi construído com foco em arquitetura backend desacoplada, separação de responsabilidades, idempotência e organização próxima de aplicações corporativas reais.

---

# Visão Geral

A aplicação possui dois fluxos principais:

## 1. Criação de Clientes

Fluxo responsável por:

- validar os dados recebidos
- persistir clientes no banco
- definir status inicial
- gerar payload GraphQL para criação de card no Pipefy

## 2. Processamento de Webhooks

Fluxo responsável por:

- receber eventos simulados do Pipefy
- garantir idempotência
- calcular prioridade do cliente
- atualizar status
- gerar mutations GraphQL de atualização

---

# Objetivos do Projeto

O projeto foi desenvolvido para praticar e demonstrar:

- arquitetura backend em camadas
- separação entre HTTP, negócio e persistência
- integração externa desacoplada
- idempotência em eventos distribuídos
- organização enterprise-ready
- testabilidade
- preparação para escalabilidade futura

---

# Stack Utilizada

| Tecnologia     | Objetivo             |
| -------------- | -------------------- |
| Python 3.12+   | Linguagem principal  |
| FastAPI        | API HTTP             |
| SQLAlchemy 2.0 | ORM                  |
| SQLite         | Banco local          |
| Alembic        | Migrations           |
| Pydantic v2    | Validação            |
| Pytest         | Testes automatizados |
| Docker         | Containerização      |
| Uvicorn        | ASGI Server          |
| GraphQL        | Integração Pipefy    |

---

# Arquitetura da Aplicação

A aplicação segue arquitetura em camadas para reduzir acoplamento e melhorar manutenção.

```text
HTTP Layer (Routes)
        ↓
Service Layer
        ↓
Repository Layer
        ↓
Database
````

## Separação de Responsabilidades

### Routes

Responsáveis apenas por:

* receber requests
* validar payloads
* chamar services
* retornar responses HTTP

As rotas não possuem regras de negócio.

---

### Services

Responsáveis por:

* regras de negócio
* orquestração dos fluxos
* priorização
* idempotência
* integração com Pipefy

---

### Repositories

Responsáveis exclusivamente pelo acesso ao banco.

Centralizam:

* queries
* inserts
* updates
* persistência

---

### Integrations

Camada isolada para integrações externas.

Atualmente contém:

* mutations GraphQL
* cliente Pipefy
* simulação de requests

Essa separação facilita manutenção e testes.

---

# Estrutura de Pastas

```text
app/
├── api/
│   ├── routes/
│   │   ├── clients.py
│   │   └── webhooks.py
│   └── dependencies.py
│
├── core/
│   ├── config.py
│   ├── database.py
│   ├── logging.py
│   └── exceptions.py
│
├── integrations/
│   └── pipefy/
│       ├── graphql_client.py
│       └── mutations.py
│
├── models/
│   ├── client.py
│   └── webhook_event.py
│
├── repositories/
│   ├── client_repository.py
│   └── webhook_repository.py
│
├── schemas/
│   ├── client.py
│   └── webhook.py
│
├── services/
│   ├── client_service.py
│   └── webhook_service.py
│
├── tests/
│   ├── conftest.py
│   ├── test_create_client.py
│   ├── test_webhook_priority.py
│   └── test_webhook_idempotency.py
│
└── main.py
```

---

# Fluxos da Aplicação

# POST /clientes

Endpoint responsável pela criação de clientes.

## Fluxo

1. valida payload com Pydantic
2. cria cliente no banco
3. define status inicial
4. monta mutation GraphQL
5. simula envio ao Pipefy
6. retorna resposta estruturada

## Status Inicial

```text
Aguardando Analise
```

---

# POST /webhooks/pipefy/card-updated

Endpoint responsável pelo processamento de webhooks.

## Fluxo

1. verifica idempotência
2. valida duplicidade do evento
3. busca cliente
4. calcula prioridade
5. atualiza status
6. registra evento processado
7. gera mutations GraphQL de update

## Status Final

```text
Processado
```

---

# Regra de Priorização

| Patrimônio | Prioridade |
| ---------- | ---------- |
| >= 200000  | alta       |
| < 200000   | normal     |

---

# Estratégia de Idempotência

Como webhooks podem ser reenviados múltiplas vezes, o sistema implementa controle de idempotência utilizando:

* `event_id`
* tabela de eventos processados
* constraint UNIQUE

Caso um evento duplicado seja recebido:

* o processamento é interrompido
* a API retorna HTTP 409

---

# Integração GraphQL

O projeto utiliza estrutura baseada na API GraphQL do Pipefy.

## Mutation - Create Card

```graphql
mutation CreateCard($input: CreateCardInput!) {
  createCard(input: $input) {
    card {
      id
      title
      created_at
    }
  }
}
```

---

## Mutation - Update Card Field

```graphql
mutation UpdateCardField($input: UpdateCardFieldInput!) {
  updateCardField(input: $input) {
    card {
      id
    }
    success
  }
}
```

---

# Banco de Dados

## Tabela: clients

Armazena:

* dados do cliente
* patrimônio
* status
* prioridade

---

## Tabela: processed_webhook_events

Responsável pelo controle de idempotência.

Possui:

* índice
* constraint UNIQUE para `event_id`

---

# Executando o Projeto

## Instalar dependências

```bash
pip install -r requirements.txt
```

## Executar migrations

```bash
alembic upgrade head
```

## Subir aplicação

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

---

# Executando com Docker

```bash
docker-compose up --build
```

---

# Executando os Testes

```bash
pytest app/tests/ -v
```

---

# Swagger

Disponível em:

```text
http://localhost:8000/docs
```

---

# Exemplos de Requisição

## Criar Cliente (PowerShell)

```powershell
Invoke-RestMethod `
  -Method POST `
  -Uri "http://localhost:8000/clientes" `
  -ContentType "application/json" `
  -Body '{
    "cliente_nome":"Joao Silva",
    "cliente_email":"joao@example.com",
    "tipo_solicitacao":"Atualizacao cadastral",
    "valor_patrimonio":250000
  }'
```

---

## Processar Webhook (PowerShell)

```powershell
Invoke-RestMethod `
  -Method POST `
  -Uri "http://localhost:8000/webhooks/pipefy/card-updated" `
  -ContentType "application/json" `
  -Body '{
    "event_id":"evt_123",
    "card_id":"card_456",
    "cliente_email":"joao@example.com",
    "timestamp":"2026-05-18T12:00:00Z"
  }'
```

---

# Logging

A aplicação possui logging estruturado para:

* criação de clientes
* processamento de webhooks
* eventos duplicados
* integração Pipefy
* tratamento de erros

---

# Tratamento de Erros

Exceções customizadas utilizadas:

* `ClientNotFoundException`
* `DuplicateWebhookEventException`

Handlers globais padronizam as respostas HTTP.

---

# Testes Automatizados

Os testes cobrem:

* criação de cliente
* validação de email
* patrimônio inválido
* regra de prioridade
* idempotência
* cliente inexistente
* duplicidade de eventos

---

# Possíveis Evoluções

* PostgreSQL
* autenticação JWT
* integração real com Pipefy
* filas assíncronas
* retry policy
* observabilidade distribuída
* CI/CD
* rate limiting
* tracing

---

# Escalabilidade AWS

Arquitetura futura planejada:

```text
API Gateway
    ↓
ECS Fargate / Lambda
    ↓
RDS PostgreSQL
    ↓
SQS
    ↓
Workers Assíncronos
```

## Serviços AWS

| Serviço         | Responsabilidade         |
| --------------- | ------------------------ |
| API Gateway     | Entrada HTTP             |
| ECS Fargate     | Containers               |
| Lambda          | Processamento assíncrono |
| RDS PostgreSQL  | Persistência             |
| DynamoDB        | Idempotência distribuída |
| SQS             | Fila de eventos          |
| CloudWatch      | Logs                     |
| Secrets Manager | Gestão de segredos       |

---

# Considerações Finais

O objetivo do projeto foi simular uma aplicação backend moderna aplicando:

* arquitetura desacoplada
* separação de responsabilidades
* integração externa
* regras de negócio isoladas
* testes automatizados
* idempotência
* observabilidade
* preparação para cloud

A proposta foi construir algo além de um CRUD simples, aproximando o projeto de um cenário real de engenharia backend.

