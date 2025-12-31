/* eslint-disable */
import { TypedDocumentNode as DocumentNode } from '@graphql-typed-document-node/core';
export type Maybe<T> = T | null;
export type InputMaybe<T> = Maybe<T>;
export type Exact<T extends { [key: string]: unknown }> = { [K in keyof T]: T[K] };
export type MakeOptional<T, K extends keyof T> = Omit<T, K> & { [SubKey in K]?: Maybe<T[SubKey]> };
export type MakeMaybe<T, K extends keyof T> = Omit<T, K> & { [SubKey in K]: Maybe<T[SubKey]> };
export type MakeEmpty<T extends { [key: string]: unknown }, K extends keyof T> = { [_ in K]?: never };
export type Incremental<T> = T | { [P in keyof T]?: P extends ' $fragmentName' | '__typename' ? T[P] : never };
/** All built-in and custom scalars, mapped to their actual values */
export type Scalars = {
  ID: { input: string; output: string; }
  String: { input: string; output: string; }
  Boolean: { input: boolean; output: boolean; }
  Int: { input: number; output: number; }
  Float: { input: number; output: number; }
  /** Date (isoformat) */
  Date: { input: any; output: any; }
};

export type Loan = {
  __typename?: 'Loan';
  dueDate: Scalars['Date']['output'];
  id: Scalars['Int']['output'];
  interestRate: Scalars['Float']['output'];
  name: Scalars['String']['output'];
  principal: Scalars['Float']['output'];
};

export type LoanFilter = {
  dueDate?: InputMaybe<Scalars['Date']['input']>;
  interestRate?: InputMaybe<Scalars['Float']['input']>;
  name?: InputMaybe<Scalars['String']['input']>;
  principal?: InputMaybe<Scalars['Float']['input']>;
};

export type LoanPaginatedResult = {
  __typename?: 'LoanPaginatedResult';
  items: Array<Loan>;
  paginationParams: PaginationResult;
};

export type LoanPaymentResponse = {
  __typename?: 'LoanPaymentResponse';
  amount: Scalars['Float']['output'];
  dueDate: Scalars['Date']['output'];
  id: Scalars['Int']['output'];
  interestRate: Scalars['Float']['output'];
  name: Scalars['String']['output'];
  paymentDate?: Maybe<Scalars['Date']['output']>;
  principal: Scalars['Float']['output'];
  status: PaymentStatus;
};

export type LoanPaymentResponsePaginatedResult = {
  __typename?: 'LoanPaymentResponsePaginatedResult';
  items: Array<LoanPaymentResponse>;
  paginationParams: PaginationResult;
};

export type PaginationResult = {
  __typename?: 'PaginationResult';
  nextCursor?: Maybe<Scalars['Int']['output']>;
  totalItems: Scalars['Int']['output'];
};

export enum PaymentStatus {
  Defaulted = 'DEFAULTED',
  Late = 'LATE',
  OnTime = 'ON_TIME',
  Unpaid = 'UNPAID'
}

export type Query = {
  __typename?: 'Query';
  loan?: Maybe<Loan>;
  loanPayments: LoanPaymentResponsePaginatedResult;
  loans: LoanPaginatedResult;
};


export type QueryLoanArgs = {
  loanId: Scalars['Int']['input'];
};


export type QueryLoanPaymentsArgs = {
  cursor?: InputMaybe<Scalars['Int']['input']>;
  limit?: InputMaybe<Scalars['Int']['input']>;
  loanId: Scalars['Int']['input'];
};


export type QueryLoansArgs = {
  cursor?: InputMaybe<Scalars['Int']['input']>;
  filter?: InputMaybe<LoanFilter>;
  limit?: InputMaybe<Scalars['Int']['input']>;
};

export type LoansQueryVariables = Exact<{
  cursor?: InputMaybe<Scalars['Int']['input']>;
  limit?: InputMaybe<Scalars['Int']['input']>;
  filter?: InputMaybe<LoanFilter>;
}>;


export type LoansQuery = { __typename?: 'Query', loans: { __typename?: 'LoanPaginatedResult', paginationParams: { __typename?: 'PaginationResult', totalItems: number, nextCursor?: number | null }, items: Array<{ __typename?: 'Loan', id: number, name: string, interestRate: number, principal: number, dueDate: any }> } };

export type LoanQueryVariables = Exact<{
  loanId: Scalars['Int']['input'];
}>;


export type LoanQuery = { __typename?: 'Query', loan?: { __typename?: 'Loan', id: number, name: string, interestRate: number, principal: number, dueDate: any } | null };

export type LoanPaymentsQueryVariables = Exact<{
  loanId: Scalars['Int']['input'];
  cursor?: InputMaybe<Scalars['Int']['input']>;
  limit?: InputMaybe<Scalars['Int']['input']>;
}>;


export type LoanPaymentsQuery = { __typename?: 'Query', loanPayments: { __typename?: 'LoanPaymentResponsePaginatedResult', items: Array<{ __typename?: 'LoanPaymentResponse', id: number, name: string, interestRate: number, principal: number, dueDate: any, status: PaymentStatus, amount: number, paymentDate?: any | null }>, paginationParams: { __typename?: 'PaginationResult', totalItems: number, nextCursor?: number | null } } };


export const LoansDocument = {"kind":"Document","definitions":[{"kind":"OperationDefinition","operation":"query","name":{"kind":"Name","value":"Loans"},"variableDefinitions":[{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"cursor"}},"type":{"kind":"NamedType","name":{"kind":"Name","value":"Int"}}},{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"limit"}},"type":{"kind":"NamedType","name":{"kind":"Name","value":"Int"}}},{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"filter"}},"type":{"kind":"NamedType","name":{"kind":"Name","value":"LoanFilter"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"loans"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"cursor"},"value":{"kind":"Variable","name":{"kind":"Name","value":"cursor"}}},{"kind":"Argument","name":{"kind":"Name","value":"limit"},"value":{"kind":"Variable","name":{"kind":"Name","value":"limit"}}},{"kind":"Argument","name":{"kind":"Name","value":"filter"},"value":{"kind":"Variable","name":{"kind":"Name","value":"filter"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"paginationParams"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"totalItems"}},{"kind":"Field","name":{"kind":"Name","value":"nextCursor"}}]}},{"kind":"Field","name":{"kind":"Name","value":"items"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"id"}},{"kind":"Field","name":{"kind":"Name","value":"name"}},{"kind":"Field","name":{"kind":"Name","value":"interestRate"}},{"kind":"Field","name":{"kind":"Name","value":"principal"}},{"kind":"Field","name":{"kind":"Name","value":"dueDate"}}]}}]}}]}}]} as unknown as DocumentNode<LoansQuery, LoansQueryVariables>;
export const LoanDocument = {"kind":"Document","definitions":[{"kind":"OperationDefinition","operation":"query","name":{"kind":"Name","value":"Loan"},"variableDefinitions":[{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"loanId"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"Int"}}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"loan"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"loanId"},"value":{"kind":"Variable","name":{"kind":"Name","value":"loanId"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"id"}},{"kind":"Field","name":{"kind":"Name","value":"name"}},{"kind":"Field","name":{"kind":"Name","value":"interestRate"}},{"kind":"Field","name":{"kind":"Name","value":"principal"}},{"kind":"Field","name":{"kind":"Name","value":"dueDate"}}]}}]}}]} as unknown as DocumentNode<LoanQuery, LoanQueryVariables>;
export const LoanPaymentsDocument = {"kind":"Document","definitions":[{"kind":"OperationDefinition","operation":"query","name":{"kind":"Name","value":"LoanPayments"},"variableDefinitions":[{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"loanId"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"Int"}}}},{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"cursor"}},"type":{"kind":"NamedType","name":{"kind":"Name","value":"Int"}}},{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"limit"}},"type":{"kind":"NamedType","name":{"kind":"Name","value":"Int"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"loanPayments"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"loanId"},"value":{"kind":"Variable","name":{"kind":"Name","value":"loanId"}}},{"kind":"Argument","name":{"kind":"Name","value":"cursor"},"value":{"kind":"Variable","name":{"kind":"Name","value":"cursor"}}},{"kind":"Argument","name":{"kind":"Name","value":"limit"},"value":{"kind":"Variable","name":{"kind":"Name","value":"limit"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"items"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"id"}},{"kind":"Field","name":{"kind":"Name","value":"name"}},{"kind":"Field","name":{"kind":"Name","value":"interestRate"}},{"kind":"Field","name":{"kind":"Name","value":"principal"}},{"kind":"Field","name":{"kind":"Name","value":"dueDate"}},{"kind":"Field","name":{"kind":"Name","value":"status"}},{"kind":"Field","name":{"kind":"Name","value":"amount"}},{"kind":"Field","name":{"kind":"Name","value":"paymentDate"}}]}},{"kind":"Field","name":{"kind":"Name","value":"paginationParams"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"totalItems"}},{"kind":"Field","name":{"kind":"Name","value":"nextCursor"}}]}}]}}]}}]} as unknown as DocumentNode<LoanPaymentsQuery, LoanPaymentsQueryVariables>;