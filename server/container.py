from typing import Optional

from models import Config, Loan, LoanPayment
from datastore import InMemoryDataStore, DataStore
from seed import loans, loan_payments
from services import LoanService


class Container:
    """
    Simple DI container.
    - Production: use init() to set up singletons.
    - Testing: call override() to inject test doubles.
    """

    _loan_datastore: Optional[DataStore[Loan]] = None
    _payment_datastore: Optional[DataStore[LoanPayment]] = None
    _loan_service: Optional[LoanService] = None

    @classmethod
    def reset(cls) -> None:
        cls._loan_datastore = None
        cls._payment_datastore = None
        cls._loan_service = None

    @classmethod
    def init(cls, config: Config) -> None:
        cls.reset()
        if config.datastore_type == "in_memory":
            cls._loan_datastore = InMemoryDataStore[Loan](
                initial_items=list(loans))
            cls._payment_datastore = InMemoryDataStore[LoanPayment](
                initial_items=list(loan_payments)
            )

    @classmethod
    def loan_service(cls) -> LoanService:
        if cls._loan_service is None:
            if cls._loan_datastore is None or cls._payment_datastore is None:
                raise ValueError(
                    "Container not initialized. Call init() first.")

            cls._loan_service = LoanService(
                loan_data=cls._loan_datastore,
                loan_payment_data=cls._payment_datastore,
            )

        return cls._loan_service

    @classmethod
    def override(
        cls,
        loan_datastore: Optional[DataStore[Loan]] = None,
        payment_datastore: Optional[DataStore[LoanPayment]] = None,
    ) -> None:
        cls.reset()
        if loan_datastore is not None:
            cls._loan_datastore = loan_datastore
        if payment_datastore is not None:
            cls._payment_datastore = payment_datastore
        cls._loan_service = None
