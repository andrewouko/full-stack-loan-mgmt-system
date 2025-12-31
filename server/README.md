# Simple Loan API Server

A Python Flask server with GraphQL (Strawberry) API for managing loans and payments.

## Tech Stack

- **Framework:** Flask 3.x
- **GraphQL:** Strawberry GraphQL
- **Data Store:** In-memory (with repository pattern for future DB support)
- **Testing:** pytest, pytest-cov, factory-boy
- **Containerization:** Docker

## Folder Structure

```markdown
server/
├── app.py # Entry point - Flask app factory
├── conf.py # Configuration (environment variables)
├── container.py # Dependency injection container
├── models.py # Data models (Loan, LoanPayment, PaymentStatus)
├── datastore.py # DataStore interface + InMemoryDataStore
├── services.py # Business logic (LoanService)
├── schema.py # GraphQL schema + resolvers
├── routes.py # REST endpoints
├── seed.py # Initial seed data
├── requirements.txt
├── Dockerfile
├── compose.yaml
├── pytest.ini # Pytest configuration
└── tests/
├── conftest.py # Shared pytest fixtures (app, client, datastores, services)
├── factories.py # Factory Boy factories for generating test data
├── test_loan_service.py # Unit tests for LoanService
├── test_rest_routes.py # Integration Tests for REST / and /payment routes
└── test_graphql_route.py # Integration Tests for /graphql queries
```

## Architecture

### Dependency Injection (Container Pattern)

The `Container` class provides centralized dependency management:

- Datastores are injected into services
- Easy to swap implementations (InMemory → PostgreSQL)
- Test-friendly: override datastores for isolated testing

### Repository Pattern

Data access is abstracted via `DataStore` interface:

- `InMemoryDataStore` — development/testing
- Future: `SQLLiteDataStore` — lightweight file-based DB for development/testing
- Future: `PostgresDataStore` — full scale production ready app

### Payment Status Calculation

Status is computed based on payment timing relative to due date:

| Status      | Condition                      |
| ----------- | ------------------------------ |
| `UNPAID`    | No payment date                |
| `ON_TIME`   | Paid within 5 days of due date |
| `LATE`      | Paid 6-30 days after due date  |
| `DEFAULTED` | Paid more than 30 days late    |

## Configuration

### Environment Variables

| Variable         | Default     | Description                                 |
| ---------------- | ----------- | ------------------------------------------- |
| `DATASTORE_TYPE` | `in_memory` | Data store type (`in_memory` or `database`) |
| `DATABASE_URL`   | `None`      | PostgreSQL connection string (future)       |

### Example `.env`

```bash
DATASTORE_TYPE=in_memory
```

## Running Locally

### Prerequisites

- Python 3.9+
- pip

### Setup

```bash
cd server

# Create virtual environment
python3 -m venv .venv

# Activate (bash/zsh)
source .venv/bin/activate

# Activate (fish)
source .venv/bin/activate.fish

# Install dependencies
pip install -r requirements.txt

# Run the server
python app.py
```

Server available at: http://localhost:5000

## Running with Docker

### Prerequisites for Docker

- Docker
- Docker Compose

### Commands

```bash
cd server

# Build and run
docker compose up --build

# Run in background
docker compose up -d --build

# Stop
docker compose down
```

Server available at: http://localhost:2024

## Running Tests

```bash
cd server

# Run all tests with coverage
pytest

# Run specific test file
pytest tests/test_loan_service.py

# Run with verbose output
pytest -s
```

### Test Structure

- **Unit tests:** `test_loan_service.py` — business logic
- **Integration tests:** `test_rest_routes.py`, `test_graphql_route.py` — API endpoints
- **Factories:** `factories` - Uses factory boy for test data generation
- **Fixtures:** Configured in `conftest.py` to provide reusable test components

## API Documentation

### GraphQL Endpoint

**URL:** `POST /graphql`

**Playground:** Visit `/graphql` in browser when server is running

#### Queries

##### Get Loans (with pagination)

```graphql
query Loans($cursor: Int, $limit: Int, $filter: LoanFilter) {
  loans(cursor: $cursor, limit: $limit, filter: $filter) {
    paginationParams {
      totalItems
      nextCursor
    }
    items {
      id
      name
      interestRate
      principal
      dueDate
    }
  }
}
```

##### Get Loan Payments (with pagination)

```graphql
query LoanPayments($loanId: Int!, $cursor: Int, $limit: Int) {
  loanPayments(loanId: $loanId, cursor: $cursor, limit: $limit) {
    items {
      id
      name
      interestRate
      principal
      dueDate
      status
      amount
      paymentDate
    }
    paginationParams {
      totalItems
      nextCursor
    }
  }
}
```

##### Get Loan By ID

```graphql
query Loan($loanId: Int!) {
  loan(loanId: $loanId) {
    id
    name
    interestRate
    principal
    dueDate
  }
}
```

#### Types

```graphql
type Loan {
  id: Int!
  name: String!
  interestRate: Float!
  principal: Float!
  dueDate: Date!
}

type LoanPaymentResponse {
  id: Int!
  name: String!
  interestRate: Float!
  principal: Float!
  dueDate: Date!
  paymentDate: Date
  status: PaymentStatus!
  statusDisplay: String!
}

enum PaymentStatus {
  UNPAID
  ON_TIME
  LATE
  DEFAULTED
}
```

### REST Endpoints

#### Home

**URL:** `GET /`

**Response:**

```text
Welcome to the Loan Application API
```

#### Add Payment

**URL:** `POST /payment`

**Request Body:**

```json
{
  "loan_id": 1,
  "amount": 1000.0
}
```

**Success Response (201):**

```json
{
  "id": 5,
  "loan_id": 1,
  "payment_date": "2025-12-31",
  "amount": 1000.0
}
```

**Error Response (400):**

```json
{
  "error": "Loan with id 999 does not exist."
}
```

## Future Improvements / TODOs

### Code Structure

- [ ] **Modularization** — Split code into modules/packages for better organization
  - `app/` package with submodules: `models`, `services`, `datastore`, `graphql`, `routes`
  - Easier to navigate and maintain as codebase grows

### Database & Persistence

- [ ] **PostgreSQL DataStore** — Implement `PostgresDataStore` using SQLAlchemy Core for production persistence

  - Add `InMemoryDataStore` with SQLAlchemy-backed repositories
  - Introduce `DATASTORE_TYPE=database` and `DATABASE_URL` environment variables
  - Keep repository interface unchanged for seamless swap

- [ ] **SQLAlchemy Integration** — Add SQLAlchemy as the ORM/query layer

  - Use SQLAlchemy Core (lightweight) or ORM (full-featured)
  - Define table models in `db.py` (engine, metadata, table definitions)
  - Session management via `sessionmaker`

- [ ] **Database Migrations (Alembic)** — Version-controlled schema changes
  - Initialize: `alembic init migrations`
  - Configure `alembic.ini` to read `DATABASE_URL` from environment
  - Auto-generate migrations: `alembic revision --autogenerate -m "description"`
  - Apply migrations: `alembic upgrade head`
  - Rollback: `alembic downgrade -1`
  - Run migrations in Docker entrypoint before starting the app

### Security & Auth

- [ ] **Authentication** — Add JWT-based auth for protected endpoints
- [ ] **Input validation** — Enhanced validation with Pydantic or Marshmallow

### Observability

- [ ] **Logging** — Structured logging with correlation IDs
- [ ] **Health checks** — Expand `/healthz` to verify DB connectivity

### DevOps & CI/CD

- [ ] **CI/CD Pipeline** — GitHub Actions for:

  - Automated testing on PR
  - Linting (flake8/black)
  - Docker image build and push
  - Deployment to cloud (e.g., AWS ECS, GCP Cloud Run)

- [ ] **Docker Entrypoint** — Run migrations automatically on container start:

  ```bash
  #!/bin/bash
  alembic upgrade head
  exec python app.py
  ```

### API Improvements

- [ ] **API versioning** — Version REST endpoints (e.g., `/api/v1/payment`)
- [ ] **Rate limiting** — Protect endpoints from abuse
- [ ] **OpenAPI docs** — Generate Swagger/OpenAPI spec for REST endpoints
- [ ] **GraphQL Mutations** — Add mutations for creating/updating loans
