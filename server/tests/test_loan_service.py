from typing import cast
from models import LoanFilter, LoanPayment, PaymentStatus
from models import Loan
from datastore import InMemoryDataStore
from tests.factories import LoanPaymentFactory
from services import LoanService


class TestLoanServiceGetLoans:

    def test_get_loans_no_filter(self, loan_service: LoanService, loan_datastore: InMemoryDataStore[Loan]):
        all_loans, _ = loan_datastore.get_all(cursor=None, limit=None)
        result, _ = loan_service.get_loans(
            cursor=None, limit=None, filter=None)
        assert result == all_loans
        assert len(result) == 5

    def test_get_loans_filter_by_name(self, loan_service: LoanService, loan_datastore: InMemoryDataStore[Loan]):
        loans, _ = loan_datastore.get_all(cursor=None, limit=None)
        target_loan = loans[0]
        filter_obj = LoanFilter(name=target_loan.name)
        result, _ = loan_service.get_loans(
            cursor=None, limit=None, filter=filter_obj)
        assert len(result) == 1
        assert target_loan in result
        assert all(loan.name == target_loan.name for loan in result)

    def test_get_loans_limit(self, loan_service: LoanService):
        result, _ = loan_service.get_loans(cursor=None, limit=2, filter=None)
        assert len(result) == 2

    def test_get_loans_with_cursor(self, loan_service: LoanService, loan_datastore: InMemoryDataStore[Loan]):
        # Pick the first loan as cursor
        loans_list, _ = loan_datastore.get_all(cursor=None, limit=None)
        first_loan = loans_list[0]

        # Cursor should skip the first loan
        result, _ = loan_service.get_loans(
            cursor=first_loan.id, limit=None, filter=None)
        assert first_loan not in result
        assert result == loans_list[1:]

    def test_get_loans_with_cursor_and_limit(self, loan_service: LoanService, loan_datastore: InMemoryDataStore[Loan]):
        loans_list, _ = loan_datastore.get_all(cursor=None, limit=None)
        first_loan = loans_list[0]

        # Limit the result to 2 items after cursor
        result, _ = loan_service.get_loans(
            cursor=first_loan.id, limit=2, filter=None)
        assert len(result) == 2
        assert first_loan not in result
        assert result == loans_list[1:3]

    def test_get_loan_by_id_found(self, loan_service: LoanService, loan_datastore: InMemoryDataStore[Loan]):
        loans, _ = loan_datastore.get_all(cursor=None, limit=None)
        target_loan = loans[0]
        result = loan_service.get_loan_by_id(target_loan.id)
        assert result == target_loan

    def test_get_loan_by_id_not_found(self, loan_service: LoanService):
        result = loan_service.get_loan_by_id(9999)
        assert result is None


class TestLoanServiceGetLoanPayments:
    def test_get_loan_payments_found(self, loan_service: LoanService, loan_datastore: InMemoryDataStore[Loan]):
        # Get a loan that has payments
        all_loans, _ = loan_datastore.get_all(cursor=None, limit=None)
        target_loan = all_loans[1]

        result, _ = loan_service.get_loan_payments(
            loan_id=target_loan.id, cursor=None, limit=None)
        assert len(result) > 0
        assert all(payment.name == target_loan.name for payment in result)

    def test_get_loan_payments_not_found(self, loan_service: LoanService, loan_with_no_payments: Loan):
        result, _ = loan_service.get_loan_payments(
            loan_id=loan_with_no_payments.id, cursor=None, limit=None)
        assert len(result) == 1
        assert result[0].status == PaymentStatus.UNPAID
        assert result[0].payment_date is None
        assert result[0].id == -1

    def test_on_time_payment_status(self, loan_service: LoanService, loan_with_no_payments: Loan, payment_datastore: InMemoryDataStore[LoanPayment]):
        # Create on-time payment and add to payment repo
        payment = cast(LoanPayment, LoanPaymentFactory(
            loan=loan_with_no_payments))
        payment_datastore.add(payment)

        payments, _ = loan_service.get_loan_payments(
            loan_id=loan_with_no_payments.id, cursor=None, limit=None)
        assert len(payments) == 1
        assert payments[0].status == PaymentStatus.ON_TIME

    def test_unpaid_payment_status(self, loan_service: LoanService, loan_with_no_payments: Loan, payment_datastore: InMemoryDataStore[LoanPayment]):
        # Create payment with no payment date and add to payment repo
        payment = cast(LoanPayment, LoanPaymentFactory(
            loan=loan_with_no_payments, unpaid=True))
        payment_datastore.add(payment)

        payments, _ = loan_service.get_loan_payments(
            loan_id=loan_with_no_payments.id, cursor=None, limit=None)
        assert len(payments) == 1
        assert payments[0].status == PaymentStatus.UNPAID

    def test_late_payment_status(self, loan_service: LoanService, loan_with_no_payments: Loan, payment_datastore: InMemoryDataStore[LoanPayment]):
        # Create payment with no payment date and add to payment repo
        payment = cast(LoanPayment, LoanPaymentFactory(
            loan=loan_with_no_payments, late=True))
        payment_datastore.add(payment)

        payments, _ = loan_service.get_loan_payments(
            loan_id=loan_with_no_payments.id, cursor=None, limit=None)
        assert len(payments) == 1
        assert payments[0].status == PaymentStatus.LATE

    def test_defaulted_payment_status(self, loan_service: LoanService, loan_with_no_payments: Loan, payment_datastore: InMemoryDataStore[LoanPayment]):
        # Create payment with no payment date and add to payment repo
        payment = cast(LoanPayment, LoanPaymentFactory(
            loan=loan_with_no_payments, defaulted=True))
        payment_datastore.add(payment)

        payments, _ = loan_service.get_loan_payments(
            loan_id=loan_with_no_payments.id, cursor=None, limit=None)
        assert len(payments) == 1
        assert payments[0].status == PaymentStatus.DEFAULTED
