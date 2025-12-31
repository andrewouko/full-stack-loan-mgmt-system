import { useQuery } from "@apollo/client";
import { LoanPaymentsDocument, LoanPaymentsQuery, LoanPaymentsQueryVariables, PaymentStatus } from "../__generated__/graphql";
import { Loan } from "../types";
import { Table } from "./table";

const paymentStatusClass: Record<PaymentStatus, string> = {
  ON_TIME: "on-time-status",
  LATE: "late-status",
  DEFAULTED: "defaulted-status",
  UNPAID: "unpaid-status",
};

const paymentStatusText: Record<PaymentStatus, string> = {
  ON_TIME: "On Time",
  LATE: "Late",
  DEFAULTED: "Defaulted",
  UNPAID: "Unpaid",
};

export const PaymentList: React.FC<{ loan: Loan }> = ({ loan }) => {
  const { data, loading, error } = useQuery<
    LoanPaymentsQuery,
    LoanPaymentsQueryVariables
  >(LoanPaymentsDocument, {
    variables: { loanId: loan.id },
    fetchPolicy: "no-cache",
  });

  if (loading) return <div>Loading...</div>;
  if (error) return <div>Error: {error.message}</div>;

  const loanPayments = data?.loanPayments.items ?? [];
  return (
    <>
      <h2>
        Payments for Loan: <em>{loan.name}</em>
      </h2>
      <Table
        title="Payments"
        columnNames={[
          "Payment ID",
          "Payment Amount",
          "Interest Rate",
          "Principal",
          "Due Date",
          "Payment Date",
          "Status",
        ]}
        data={loanPayments.map((payment) => ({
          id: payment.id,
          amount: payment.amount.toLocaleString("en-KE", {
            style: "currency",
            currency: "KES",
            minimumFractionDigits: 2,
            maximumFractionDigits: 2,
          }),
          interestRate: (payment.interestRate / 100).toLocaleString("en-KE", {
            minimumFractionDigits: 2,
            maximumFractionDigits: 2,
            style: "percent",
          }),
          principal: payment.principal.toLocaleString("en-KE", {
            style: "currency",
            currency: "KES",
            minimumFractionDigits: 2,
            maximumFractionDigits: 2,
          }),
          dueDate: payment.dueDate,
          paymentDate: payment.paymentDate ? payment.paymentDate : "N/A",
          status: paymentStatusText[payment.status],
          className: paymentStatusClass[payment.status],
        }))}
        loading={false}
        hasError={false}
      />
    </>
  );
};
