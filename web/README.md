# Simple Loan Management Frontend

A React + TypeScript frontend for managing loans with GraphQL integration, built with Vite.

## Tech Stack

| Technology | Purpose |
|------------|---------|
| **React 18** | UI framework |
| **TypeScript** | Type-safe JavaScript |
| **Vite** | Build tool with HMR |
| **Apollo Client** | GraphQL client for data fetching and caching |
| **GraphQL Codegen** | Generates TypeScript types from GraphQL schema |
| **ESLint** | Code linting |

## Folder Structure

```text
web/
├── src/
│   ├── __generated__/        # Auto-generated GraphQL types (do not edit)
│   │   ├── fragment-masking.ts
│   │   ├── gql.ts
│   │   ├── graphql.ts
│   │   └── index.ts
│   ├── assets/               # Static assets (images, fonts, etc.)
│   ├── components/           # React components
│   │   ├── AddNewPayment.tsx # Form to add loan payments
│   │   ├── ExistingLoans.tsx # Loans table with filters & pagination
│   │   ├── LoanCalculator.tsx# Loan calculation utility
│   │   ├── PaymentList.tsx   # Display loan payment history
│   │   ├── spinner.tsx       # Loading spinner component
│   │   └── table.tsx         # Generic reusable table component
│   ├── graphql/              # GraphQL operations (queries, mutations)
│   │   └── loan.ts           # Loan-related queries
│   ├── hooks/                # Custom React hooks
│   │   └── pagination.ts     # usePagination hook for cursor-based pagination
│   ├── App.css               # Main application styles
│   ├── App.tsx               # Root application component
│   ├── config.ts             # API configuration (URLs from env vars)
│   ├── index.css             # Global styles
│   ├── main.tsx              # Application entry point
│   ├── types.ts              # Shared TypeScript types
│   └── vite-env.d.ts         # Vite environment type declarations
├── codegen.ts                # GraphQL Codegen configuration
├── package.json
├── tsconfig.json
├── tsconfig.app.json
├── tsconfig.node.json
├── vite.config.ts
└── eslint.config.js
```

## Prerequisites

- **Node.js** v20+ (recommended: v22+)
- **npm** or **yarn**
- **Backend server running** at configured URL (default: `http://localhost:2024`)

## Environment Variables

Create a `.env` file in the `web/` directory:

```env
VITE_API_BASE_URL=http://localhost:2024
```

The frontend uses this to configure:

- **GraphQL endpoint**: `${VITE_API_BASE_URL}/graphql`
- **REST endpoints**: `${VITE_API_BASE_URL}/payment`

> **Note**: Vite requires the `VITE_` prefix for environment variables to be exposed to the client.

## Installation

```bash
cd web
npm install
```

## Running Locally

```bash
# Start development server with HMR
npm run dev
```

The app will be available at `http://localhost:5173` (Vite default).

> **Important**: Ensure the backend server is running before starting the frontend.

## GraphQL Codegen

We use [GraphQL Code Generator](https://the-guild.dev/graphql/codegen) to generate TypeScript types from the GraphQL schema.

### How It Works

1. **Schema introspection**: Codegen connects to the running backend at the GraphQL endpoint
2. **Type generation**: Creates TypeScript types for all queries, mutations, and fragments
3. **Output**: Generated files are placed in `src/__generated__/`

### Regenerating Types

```bash
# Ensure backend is running first
npm run compile
```

### Configuration

The codegen configuration is in `codegen.ts`:

### Adding a New Query/Mutation

1. **Create the operation** in `src/graphql/loan.ts` (or create a new file):

   ```typescript
   import { graphql } from '../__generated__/gql';

   export const GET_LOAN_BY_ID = graphql(`
     query GetLoanById($id: ID!) {
       loan(id: $id) {
         id
         name
         interestRate
       }
     }
   `);
   ```

2. **Regenerate types**:

   ```bash
   npm run compile
   ```

3. **Use in a component** with full type safety:

   ```typescript
   import { useQuery } from '@apollo/client';
   import { GET_LOAN_BY_ID } from '../graphql/loan';

   const { data, loading, error } = useQuery(GET_LOAN_BY_ID, {
     variables: { id: '123' },
   });
   // data is fully typed!
   ```

## Architecture & Patterns

### Component Structure

| Component | Description |
|-----------|-------------|
| `ExistingLoans` | Main loans display with filter panel, data fetching, and cursor-based pagination |
| `AddNewPayment` | Form component for submitting loan payments via REST API |
| `LoanCalculator` | Utility component for loan calculations |
| `PaymentList` | Displays payment history for a loan |
| `Table` | Generic, reusable table with TypeScript generics |
| `Spinner` | Simple loading indicator |

### Custom Hooks

#### `usePagination`

Manages cursor-based pagination state with history for back navigation:

```typescript
import { usePagination } from '../hooks/pagination';

const {
  currentCursor,   // Current page cursor (null for first page)
  goToNext,        // Navigate to next page
  goToPrevious,    // Navigate to previous page
  canGoBack,       // Whether back navigation is possible
  resetPagination, // Reset to first page
} = usePagination();
```

### Generic Reusable Components

#### `Table<T>`

A fully typed generic table component:

```typescript
import { Table, Column } from '../components/table';

interface Loan {
  id: string;
  name: string;
  interestRate: number;
}

const columns: Column<Loan>[] = [
  'Loan Id',
  'Name',
  'Interest Rate',
];

<Table data={loans} columns={columns} />
```

## Styling

### CSS Approach

The project uses **plain CSS** with file-based organization:

- `index.css` — Global styles, CSS resets, root variables
- `App.css` — Application-level component styles

### Responsive Considerations

Currently basic responsive design. Filter panel and table layouts adapt to available width.

## Available Scripts

| Script | Command | Description |
|--------|---------|-------------|
| `dev` | `npm run dev` | Start development server with HMR |
| `build` | `npm run build` | Build for production |
| `preview` | `npm run preview` | Preview production build locally |
| `lint` | `npm run lint` | Run ESLint |
| `compile` | `npm run compile` | Regenerate GraphQL types |

## Linting

ESLint is configured with TypeScript support. Configuration is in `eslint.config.js`.

```bash
# Run linter
npm run lint
```

## Testing

> **TODO**: Testing is not yet implemented.

### Recommended Testing Stack

- **Vitest** — Fast unit testing (Vite-native)
- **React Testing Library** — Component testing
- **MSW (Mock Service Worker)** — API mocking for tests

### Example Test Setup (Future)

```typescript
import { render, screen } from '@testing-library/react';
import { MockedProvider } from '@apollo/client/testing';
import { ExistingLoans } from './ExistingLoans';

const mocks = [/* GraphQL mocks */];

test('renders loans table', async () => {
  render(
    <MockedProvider mocks={mocks}>
      <ExistingLoans />
    </MockedProvider>
  );
  expect(await screen.findByText('Loans')).toBeInTheDocument();
});
```

## Future Improvements / TODOs

### Testing the app

- [ ] Unit tests with Vitest + React Testing Library
- [ ] E2E tests with Cypress
- [ ] Apollo MockedProvider for GraphQL testing

### UX Improvements

- [ ] Add react-router for multi-page navigation
- [ ] Error boundary components for graceful error handling
- [ ] Loading skeletons (Shimmers) instead of spinners
- [ ] Toast notifications for success/error feedback
- [ ] Form validation with better error messages using Zod + React Hook Form

### Architecture

- [ ] Environment-based API URLs (dev/staging/prod)
- [ ] State management evaluation (Zustand, Redux, etc.) for complex state

### Advanced Features

- [ ] Real-time updates with GraphQL subscriptions
