# Simple Loan Management System

A full-stack loan management application with a Python/Flask backend and React/TypeScript frontend.

## Overview

This application allows users to:

- View loans with filtering and pagination
- Track loan payment statuses (On Time, Late, Defaulted, Unpaid)
- Add new payments to existing loans
- Calculate loan details

## Tech Stack

| Layer | Technologies |
|-------|--------------|
| **Backend** | Python 3.9+, Flask, Strawberry GraphQL |
| **Frontend** | React 18, TypeScript, Vite, Apollo Client |
| **Data** | In-memory store (repository pattern for future DB support) |
| **Testing** | pytest (backend), GraphQL Codegen (type safety) |

## Project Structure Overview

```text
full-stack/
├── server/          # Python Flask backend
│   ├── app.py       # Entry point
│   ├── schema.py    # GraphQL schema
│   ├── services.py  # Business logic
│   ├── datastore.py # Data access layer
│   └── tests/       # pytest tests
├── web/             # React frontend
│   ├── src/
│   │   ├── components/   # React components
│   │   ├── graphql/      # GraphQL operations
│   │   ├── hooks/        # Custom hooks
│   │   └── __generated__/ # Generated types
│   └── codegen.ts   # GraphQL Codegen config
└── README.md        # This file
```

## Quick Start

### 1. Start the Backend

```bash
cd server
docker compose up --build
```

Server available at: http://localhost:2024

> Or run locally with Python — see [Server README](server/README.md)

### 2. Start the Frontend

```bash
cd web
npm install
npm run dev
```

App available at: http://localhost:5173

## API Endpoints

### GraphQL (`/graphql`)

| Query | Description |
|-------|-------------|
| `loans` | Get paginated loans with optional filters |
| `loan(loanId)` | Get a single loan by ID |
| `loanPayments(loanId)` | Get payment history with status |

### REST

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | Health check |
| `POST` | `/payment` | Add a new payment |

## Payment Status Logic

| Status | Condition | Color |
|--------|-----------|-------|
| **On Time** | Paid within 5 days of due date | 🟢 Green |
| **Late** | Paid 6-30 days after due date | 🟠 Orange |
| **Defaulted** | Paid 30+ days after due date | 🔴 Red |
| **Unpaid** | No payment date | ⚪ Gray |

## Documentation

- **[Server README](server/README.md)** — Backend setup, architecture, API docs, testing
- **[Web README](web/README.md)** — Frontend setup, components, GraphQL Codegen, patterns

## Development

### Running Tests (Backend)

```bash
cd server
pytest
```

### Regenerating GraphQL Types (Frontend)

```bash
cd web
npm run compile
```

## Architecture Highlights

- **Repository Pattern** — Abstracted data access for easy DB swap
- **Dependency Injection** — Container pattern for testability
- **Type Safety** — Strawberry GraphQL (backend) + GraphQL Codegen (frontend)
- **Cursor Pagination** — Scalable pagination with `cursor` + `limit`

## Future Improvements

- [ ] PostgreSQL database integration
- [ ] JWT authentication
- [ ] Unit tests for frontend (Vitest + RTL)
- [ ] E2E tests (Cypress)

---
