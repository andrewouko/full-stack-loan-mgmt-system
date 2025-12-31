import { gql } from "@apollo/client";

export const GET_LOANS = gql`
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
`;

export const GET_LOAN = gql`
  query Loan($loanId: Int!) {
    loan(loanId: $loanId) {
      id
      name
      interestRate
      principal
      dueDate
    }
  }
`;

export const GET_LOAN_PAYMENTS = gql`
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
`;
