from typing import Optional

from models import Loan, LoanPayment
from repositories import InMemoryRepository, Repository
from seed import loans, loan_payments
from services import LoanService


class Container:
    """
    Simple DI container.
    - Production: uses seed data with InMemoryRepository (we can swap for DB later).
    - Testing: call override() to inject test doubles.
    """

    _loan_repo: Optional[Repository[Loan]] = None
    _payment_repo: Optional[Repository[LoanPayment]] = None
    _loan_service: Optional[LoanService] = None

    @classmethod
    def loan_repo(cls) -> Repository[Loan]:
        if cls._loan_repo is None:
            cls._loan_repo = InMemoryRepository[Loan](
                initial_items=list(loans))
        return cls._loan_repo

    @classmethod
    def payment_repo(cls) -> Repository[LoanPayment]:
        if cls._payment_repo is None:
            cls._payment_repo = InMemoryRepository[LoanPayment](
                initial_items=list(loan_payments)
            )
        return cls._payment_repo

    @classmethod
    def loan_service(cls) -> LoanService:
        if cls._loan_service is None:
            cls._loan_service = LoanService(
                loan_data=cls.loan_repo(),
                loan_payment_data=cls.payment_repo(),
            )
        return cls._loan_service

    @classmethod
    def reset(cls) -> None:
        cls._loan_repo = None
        cls._payment_repo = None
        cls._loan_service = None

    @classmethod
    def override(
        cls,
        loan_repo: Optional[Repository[Loan]] = None,
        payment_repo: Optional[Repository[LoanPayment]] = None,
    ) -> None:
        if loan_repo is not None:
            cls._loan_repo = loan_repo
        if payment_repo is not None:
            cls._payment_repo = payment_repo
        cls._loan_service = None
