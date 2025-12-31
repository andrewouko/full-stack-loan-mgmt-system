from datetime import date
from itertools import count
from typing import Any, List, Optional
from models import Loan, LoanFilter, LoanPayment, LoanPaymentInput, LoanPaymentResponse, PaginationResult, PaymentStatus
from datastore import DataStore


class LoanService:
    _id_counter = count(4)

    def __init__(self, loan_data: DataStore[Loan], loan_payment_data: DataStore[LoanPayment]) -> None:
        self._loan_data = loan_data
        self._loan_payment_data = loan_payment_data

    def get_loans(
        self,
        cursor: Optional[int],
        limit: Optional[int],
        filter: Optional[LoanFilter],
    ) -> tuple[List[Loan], PaginationResult]:
        def filter_fn(loan: Loan) -> bool:
            if filter is None:
                return True
            if filter.name is not None and filter.name.lower() not in loan.name.lower():
                return False
            if filter.interest_rate is not None and loan.interest_rate > filter.interest_rate:
                return False
            if filter.principal is not None and loan.principal > filter.principal:
                return False
            if filter.due_date is not None and loan.due_date > filter.due_date:
                return False
            return True

        return self._loan_data.get_all(cursor=cursor, limit=limit, filter_fn=filter_fn)

    def get_loan_by_id(self, loan_id: int) -> Optional[Loan]:
        return self._loan_data.get_by_id(loan_id)

    def get_loan_payments(self, loan_id: int, cursor: Optional[int] = None, limit: Optional[int] = None) -> tuple[List[LoanPaymentResponse], PaginationResult]:
        loan = self.get_loan_by_id(loan_id)
        if loan is None:
            return [], PaginationResult(total_items=0)

        def filter_fn(payment: LoanPayment) -> bool:
            return payment.loan_id == loan_id

        payments, pagination_result = self._loan_payment_data.get_all(
            cursor=cursor, limit=limit, filter_fn=filter_fn)

        if len(payments) == 0:
            return [
                LoanPaymentResponse(
                    id=-1,
                    name=loan.name,
                    interest_rate=loan.interest_rate,
                    principal=loan.principal,
                    due_date=loan.due_date,
                    payment_date=None,
                    status=PaymentStatus.UNPAID,
                    amount=0.0
                )
            ], pagination_result

        return [
            LoanPaymentResponse(
                id=payment.id,
                name=loan.name,
                interest_rate=loan.interest_rate,
                principal=loan.principal,
                due_date=loan.due_date,
                payment_date=payment.payment_date,
                status=self._get_loan_payment_status(
                    loan.due_date, payment.payment_date),
                amount=payment.amount
            )
            for payment in payments
        ], pagination_result

    def _get_loan_payment_status(self, loan_due_date: date, payment_date: Optional[date]) -> PaymentStatus:
        if payment_date is None:
            return PaymentStatus.UNPAID

        days_late = (payment_date - loan_due_date).days
        if days_late <= 5:
            return PaymentStatus.ON_TIME
        elif 6 <= days_late <= 30:
            return PaymentStatus.LATE
        else:
            return PaymentStatus.DEFAULTED

    def validate_and_format_loan_payment_request(self, input: dict[str, Any]) -> LoanPaymentInput:
        loan_id = input.get("loan_id")
        amount = input.get("amount")

        if not isinstance(loan_id, int) or loan_id <= 0:
            raise ValueError("loan_id must be a positive integer.")

        if not isinstance(amount, (int, float)) or amount <= 0:
            raise ValueError("amount must be a positive number.")

        return LoanPaymentInput(loan_id=loan_id, amount=float(amount))

    def add_loan_payment(self, input: LoanPaymentInput) -> LoanPayment:
        loan = self.get_loan_by_id(input.loan_id)
        if loan is None:
            raise ValueError(f"Loan with id {input.loan_id} does not exist.")

        loan_payment = LoanPayment(
            id=next(self._id_counter),
            loan_id=input.loan_id,
            payment_date=date.today(),
            amount=input.amount
        )

        return self._loan_payment_data.add(loan_payment)
