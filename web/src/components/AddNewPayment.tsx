import { useState } from "react";
import { LoanPayment } from "../types";
import { Spinner } from "./spinner";
import { PAYMENT_URL } from "../config";

type ResponseData =
  | {
      error?: string;
    }
  | LoanPayment;

export const AddNewPayment = () => {
  const [loanId, setLoanId] = useState<string | null>(null);
  const [amount, setAmount] = useState<number | null>(null);
  const [errorText, setErrorText] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [showSuccessModal, setShowSuccessModal] = useState<boolean>(false);

  const validateInput = () => {
    if (loanId === null || amount === null) {
      setErrorText("Please provide both Loan ID and Amount.");
      return false;
    }
    if (loanId.trim().length === 0) {
      setErrorText("Loan ID cannot be empty.");
      return false;
    }
    if (amount <= 0) {
      setErrorText("Amount must be greater than zero.");
      return false;
    }
    if (Number.isNaN(amount)) {
      setErrorText("Amount must be a valid number.");
      return false;
    }
    setErrorText(null);
    return true;
  };

  const handleSubmit = async () => {
    setIsLoading(true);
    const res = await fetch(PAYMENT_URL, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        loan_id: Number(loanId),
        amount,
      }),
    });
    const responseData = (await res.json()) as ResponseData;
    console.log("Response Data:", responseData);
    if (res.ok) {
      setErrorText(null);
      // Clear form fields upon successful submission
      setLoanId(null);
      setAmount(null);
      setShowSuccessModal(true);
    } else {
      const errorMessage =
        "error" in responseData && responseData.error
          ? responseData.error
          : "Failed to add payment.";
      setErrorText(errorMessage);
    }
    setIsLoading(false);
  };

  return (
    <div>
      {isLoading ? (
        <Spinner />
      ) : (
        <form
          onSubmit={(e) => {
            e.preventDefault();
            const isValid = validateInput();
            if (isValid) {
              handleSubmit();
            }
          }}
        >
          <p>
            <label htmlFor="loan-id">Payment Loan Id: </label>
            <input
              id="loan-id"
              name="loan-id"
              value={loanId ?? ""}
              onChange={(e) => {
                setLoanId(e.target.value);
              }}
            />
          </p>

          <p>
            <label htmlFor="payment-amount">Payment Amount: </label>
            <input
              id="payment-amount"
              name="payment-amount"
              type="number"
              value={amount ?? ""}
              onChange={(e) => {
                setAmount(Number(e.target.value));
              }}
            />
          </p>
          {errorText && <p className="error-message">{errorText}</p>}
          <p>
            <button type="submit">Add Payment</button>
          </p>
        </form>
      )}
      {showSuccessModal && (
        <div className="modal-overlay">
          <div className="modal alert-success">
            <p>Payment added successfully!</p>
            <button
              className="modal-close"
              onClick={() => setShowSuccessModal(false)}
            >
              Close
            </button>
          </div>
        </div>
      )}
    </div>
  );
};
