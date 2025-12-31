import React, { useState } from "react";
import { useQuery } from "@apollo/client";
import { usePagination } from "../hooks/pagination";
import { Table } from "./table";
import { Spinner } from "./spinner";
import {
  LoansDocument,
  LoansQuery,
  LoansQueryVariables,
} from "../__generated__/graphql";
import { Loan } from "../types";
import { PaymentList } from "./PaymentList";

const PAGE_SIZE_OPTIONS = [1, 5, 10];

export const ExistingLoans: React.FC = () => {
  const [limit, setLimit] = useState<number>(PAGE_SIZE_OPTIONS[1]);
  const { goToNextPage, goToPreviousPage, cursor, resetPagination } = usePagination();
  const [selectedLoan, setSelectedLoan] = useState<Loan | null>(null);

  // filter UI state
  const [showFilters, setShowFilters] = useState<boolean>(false);
  const [nameFilter, setNameFilter] = useState<string | null>(null);
  const [interestRateFilter, setInterestRateFilter] = useState<string | null>(
    null
  );
  const [dueDateFilter, setDueDateFilter] = useState<string | null>(null); // yyyy-mm-dd
  const [principalFilter, setPrincipalFilter] = useState<string | null>(null);
  const [appliedFilter, setAppliedFilter] = useState<
    LoansQueryVariables["filter"] | undefined
  >(undefined);

  const applyFilters = () => {
    const filter: LoansQueryVariables["filter"] = {};
    // Filter for the name
    if (nameFilter?.trim().length) filter.name = nameFilter.trim();

    // Filter for the interest rate
    if (
      interestRateFilter?.trim().length &&
      !Number.isNaN(Number(interestRateFilter))
    ) {
      // backend expects Float (use <= semantics); convert percent input to number
      filter.interestRate = Number(interestRateFilter);
    }

    // Filter for the due date
    if (dueDateFilter?.length) {
      // backend expects Date input (use <= semantics)
      filter.dueDate = dueDateFilter;
    }

    // Filter for the principal
    if (
      principalFilter?.trim().length &&
      !Number.isNaN(Number(principalFilter))
    ) {
      // backend expects Float (use <= semantics)
      filter.principal = Number(principalFilter);
    }
    setAppliedFilter(filter);
    resetPagination();
  };

  const clearFilters = () => {
    setNameFilter(null);
    setInterestRateFilter(null);
    setDueDateFilter(null);
    setAppliedFilter(undefined);
    resetPagination();
  };

  const { data, loading, error } = useQuery<LoansQuery, LoansQueryVariables>(
    LoansDocument,
    {
      variables: { cursor, limit, filter: appliedFilter },
      // Prefer fresh data when filters change
      fetchPolicy: "cache-and-network",
    }
  );

  if (loading) return <Spinner />;
  if (error) return <div>Error: {error.message}</div>;

  const loans = data?.loans.items ?? [];

  return (
    <>
      <button onClick={() => setShowFilters(!showFilters)}>{`${
        showFilters ? "Hide Filters" : "Show Filters"
      }`}</button>
      {showFilters && (
        <div className="filters">
          <label>
            {`Name:`}
            <input
              type="text"
              value={nameFilter ?? ""}
              onChange={(e) => setNameFilter(e.target.value)}
              placeholder="Search by name"
            />
            <small>Loan name includes search value</small>
          </label>

          <label>
            {`Interest rate:`}
            <input
              type="number"
              value={interestRateFilter ?? ""}
              onChange={(e) => setInterestRateFilter(e.target.value)}
              placeholder="e.g. 10 (means <= 10%)"
              min={0}
            />
          </label>

          <label>
            {`Due date:`}
            <input
              type="date"
              value={dueDateFilter ?? ""}
              onChange={(e) => setDueDateFilter(e.target.value)}
            />
            <small>Loans before date selected</small>
          </label>

          <label>
            {`Principal:`}
            <input
              type="number"
              value={principalFilter ?? ""}
              onChange={(e) => setPrincipalFilter(e.target.value)}
              placeholder="e.g. 10,000 (means <= 10,000)"
              min={0}
            />
          </label>

          <div className="filter-actions">
            <button onClick={applyFilters}>Apply</button>
            <button onClick={clearFilters}>Clear</button>
          </div>
        </div>
      )}
      <Table
        title="Loans"
        columnNames={["ID", "Name", "Principal", "Interest %", "Due Date"]}
        data={loans.map((loan) => ({
          id: loan.id,
          name: loan.name,
          principal: loan.principal.toLocaleString("en-KE", {
            style: "currency",
            currency: "KES",
            minimumFractionDigits: 2,
            maximumFractionDigits: 2,
          }),
          interestRate: (loan.interestRate / 100).toLocaleString("en-KE", {
            minimumFractionDigits: 2,
            maximumFractionDigits: 2,
            style: "percent",
          }),
          dueDate: loan.dueDate,
        }))}
        loading={loading}
        hasError={!!error}
        pagination={{
          limit,
          setLimit,
          cursor,
          goToNextPage,
          goToPreviousPage,
          pageSizeOptions: PAGE_SIZE_OPTIONS,
          totalItems: data?.loans.paginationParams.totalItems ?? 0,
          nextCursor: data?.loans.paginationParams.nextCursor ?? null,
        }}
        onRowClick={(loan) =>
          setSelectedLoan({
            id: loan.id,
            name: loan.name,
            interestRate: Number(loan.interestRate),
            principal: Number(loan.principal),
            dueDate: loan.dueDate,
          })
        }
      />
      {selectedLoan && (
        <div
          className="modal-overlay"
          onClick={(e) => {
            // Prevent bubbling to avoid closing when clicking inside the modal
            if (e.target === e.currentTarget) {
              setSelectedLoan(null);
            }
          }}
        >
          <div className="modal scrollable-modal">
            <PaymentList loan={selectedLoan} />
            <button
              className="modal-close"
              onClick={() => setSelectedLoan(null)}
            >
              Close
            </button>
          </div>
        </div>
      )}
    </>
  );
};
