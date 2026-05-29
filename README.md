# Client Management & Pipefy Integration

Backend corporativo desenvolvido com FastAPI para gerenciamento de clientes, processamento de webhooks e integração simulada com Pipefy via GraphQL.

O projeto foi estruturado utilizando arquitetura em camadas, separação clara de responsabilidades, idempotência para eventos distribuídos e testes automatizados, simulando um cenário próximo de uma aplicação backend real utilizada em ambientes corporativos.

---

# Visão Geral

A aplicação possui dois fluxos principais:

## 1. Criação de Clientes

Responsável por:
- validar dados de entrada
- persistir clientes no banco
- definir status inicial
- estruturar mutation GraphQL de criação de card no Pipefy

## 2. Processamento de Webhooks

Responsável por:
- receber eventos simulados do Pipefy
- garantir idempotência
- aplicar regra de priorização
- atualizar status do cliente
- estruturar mutations GraphQL de atualização de campos

---

# Objetivos Técnicos

O projeto foi desenvolvido com foco em:

- arquitetura backend desacoplada
- separação entre HTTP, regras de negócio e persistência
- integração externa simulada
- organização enterprise-ready
- facilidade de manutenção
- testabilidade
- escalabilidade futura

---

# Stack Utilizada

| Tecnologia     | Objetivo                       |
| -------------- | ------------------------------ |
| Python 3.12+   | Linguagem principal            |
| FastAPI        | Framework HTTP                 |
| SQLAlchemy 2.0 | ORM                            |
| SQLite         | Banco local                    |
| Alembic        | Controle de migrations         |
| Pydantic v2    | Validação de dados             |
| Pytest         | Testes automatizados           |
| Docker         | Containerização                |
| Uvicorn        | ASGI Server                    |
| GraphQL        | Simulação da integração Pipefy |

---

# Arquitetura da Aplicação

O projeto segue arquitetura em camadas para reduzir acoplamento e melhorar organização do domínio.

```text
HTTP Layer (Routes)
        ↓
Service Layer (Business Rules)
        ↓
Repository Layer (Database Access)
        ↓
Database
````

## Separação de responsabilidades

### Routes

Responsáveis apenas por:

* receber requests
* validar payloads
* chamar services
* retornar responses HTTP

Nenhuma regra de negócio fica nos endpoints.

---

### Services

Responsáveis por:

* regras de negócio
* fluxo transacional
* priorização
* idempotência
* integração com Pipefy
* orquestração da aplicação

---

### Repositories

Responsáveis exclusivamente por:

* persistência
* queries
* isolamento do ORM

Isso evita espalhar acesso ao banco pela aplicação.

---

### Integrations

Camada isolada para integrações externas.

Atualmente:

* Pipefy GraphQL mutations
* simulação de requests externos

Essa separação facilita:

* mocking
* testes
* manutenção
* troca futura de providers

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
├── models/
│   ├── client.py
│   └── webhook_event.py
│
├── repositories/
│   ├── client_repository.py
│   └── webhook_repository.py
│
├── services/
│   ├── client_service.py
│   ├── webhook_service.py
│   └── pipefy_service.py
│
├── schemas/
│   ├── client.py
│   └── webhook.py
│
├── integrations/
│   └── pipefy/
│       ├── graphql_client.py
│       └── mutations.py
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

# Fluxo Completo da Aplicação

## Fluxo 1 - POST /clientes

### Entrada

Recebe:

* nome
* email
* tipo de solicitação
* valor do patrimônio

### Processamento

O sistema:

1. valida os dados com Pydantic
2. persiste o cliente no banco
3. define status inicial
4. monta mutation GraphQL createCard
5. simula envio ao Pipefy
6. retorna payload estruturado

### Status inicial

```text
Aguardando Analise
```

---

## Fluxo 2 - POST /webhooks/pipefy/card-updated

### Entrada

Recebe:

* event_id
* card_id
* cliente_email
* timestamp

### Processamento

O sistema:

1. verifica idempotência
2. valida duplicidade do evento
3. busca cliente
4. calcula prioridade
5. atualiza status
6. registra evento processado
7. monta mutations GraphQL de update

### Status final

```text
Processado
```

---

# Regra de Priorização

| Patrimonio | Prioridade        |
| ---------- | ----------------- |
| >= 200.000 | prioridade_alta   |
| < 200.000  | prioridade_normal |

---

# Estratégia de Idempotência

Webhooks podem ser reenviados múltiplas vezes em arquiteturas distribuídas.

Para evitar processamento duplicado:

* cada evento possui `event_id`
* o banco mantém controle dos eventos já processados
* `event_id` possui restrição UNIQUE

Caso um evento duplicado seja recebido:

* o processamento é interrompido
* a API retorna HTTP 409

---

# GraphQL - Integração Pipefy

O projeto utiliza estrutura realista baseada na documentação oficial do Pipefy GraphQL API.

A integração foi mantida desacoplada da aplicação principal para facilitar evolução futura.

---

# Mutation - Create Card

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

# Mutation - Update Card Field

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

# Exemplo de Payload GraphQL

```json
{
  "query": "mutation CreateCard($input: CreateCardInput!) { createCard(input: $input) { card { id title created_at } } }",
  "variables": {
    "input": {
      "pipe_id": "304497",
      "title": "Joao Silva - Atualizacao cadastral",
      "fields_attributes": [
        {
          "field_id": "cliente_email",
          "field_value": "joao@example.com"
        },
        {
          "field_id": "valor_patrimonio",
          "field_value": "250000"
        }
      ]
    }
  }
}
```

---

# Banco de Dados

## Tabela: clients

Armazena:

* dados do cliente
* patrimonio
* status
* prioridade

---

## Tabela: processed_webhook_events

Responsável por:

* controle de idempotência
* rastreamento de eventos processados

Possui:

* índice
* constraint UNIQUE para `event_id`

---

# Como Executar o Projeto

## Execução Local

### Instalar dependências

```bash
pip install -r requirements.txt
```

### Executar migrations

```bash
alembic upgrade head
```

### Iniciar aplicação

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

---

# Execução via Docker

## Build e start

```bash
docker-compose up --build
```

---

# Executando os Testes

```bash
pytest app/tests/ -v
```

---

# Cobertura de Testes

Os testes automatizados cobrem:

* criação de cliente
* persistência no banco
* validação de email
* patrimônio inválido
* regra de prioridade
* prioridade no threshold exato
* idempotência
* cliente inexistente
* duplicidade de eventos

---

# Swagger

Disponível em:

```text
http://localhost:8000/docs
```

---

# Exemplos de Requisição

## Criar Cliente

```bash
curl -X POST http://localhost:8000/clientes \
  -H "Content-Type: application/json" \
  -d '{
    "cliente_nome":"Joao Silva",
    "cliente_email":"joao@example.com",
    "tipo_solicitacao":"Atualizacao cadastral",
    "valor_patrimonio":250000
  }'
```

---

## Processar Webhook

```bash
curl -X POST http://localhost:8000/webhooks/pipefy/card-updated \
  -H "Content-Type: application/json" \
  -d '{
    "event_id":"evt_123",
    "card_id":"card_456",
    "cliente_email":"joao@example.com",
    "timestamp":"2026-05-18T12:00:00Z"
  }'
```

---

# Logging Estruturado

A aplicação possui logging estruturado para:

* criação de clientes
* processamento de webhook
* detecção de duplicidade
* simulação de integração Pipefy
* tratamento de erros

---

# Tratamento de Erros

Exceções customizadas:

* ClientNotFoundException
* DuplicateWebhookEventException
* ValidationException

Handlers globais garantem responses padronizadas.

---

# Possíveis Evoluções

* PostgreSQL em produção
* integração real com Pipefy
* autenticação JWT
* filas assíncronas
* retry policy
* observabilidade distribuída
* tracing
* rate limiting
* CI/CD pipeline

---

# Escalabilidade AWS

A arquitetura foi desenhada para permitir evolução para ambientes cloud distribuídos.

## Arquitetura sugerida

```text
API Gateway
    ↓
ECS Fargate / Lambda
    ↓
RDS PostgreSQL
    ↓
SQS
    ↓
Workers Assincronos
```

---

## Componentes AWS

| Serviço         | Responsabilidade         |
| --------------- | ------------------------ |
| API Gateway     | Entrada HTTP             |
| ECS Fargate     | Containers da aplicação  |
| Lambda          | Processamento assíncrono |
| RDS PostgreSQL  | Persistência relacional  |
| DynamoDB        | Idempotência distribuída |
| SQS             | Fila de eventos          |
| EventBridge     | Orquestração de eventos  |
| CloudWatch      | Logs e monitoramento     |
| Secrets Manager | Gestão de segredos       |

---

## Idempotência Distribuída

Em ambiente distribuído, o controle de idempotência pode ser realizado via DynamoDB utilizando:

```python
attribute_not_exists(event_id)
```

Isso garante processamento único mesmo com múltiplas réplicas da aplicação.

---

# Considerações Finais

O objetivo deste projeto foi simular uma aplicação backend corporativa moderna, aplicando:

* arquitetura desacoplada
* separação de responsabilidades
* integração externa simulada
* regras de negócio isoladas
* testes automatizados
* idempotência
* observabilidade
* preparação para cloud

A proposta foi construir algo além de um CRUD simples, aproximando a solução de um cenário real de engenharia backend.

