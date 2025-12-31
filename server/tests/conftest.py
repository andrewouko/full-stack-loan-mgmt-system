from pathlib import Path
import sys
from typing import Generator, cast

from flask import Flask
import pytest
from flask.testing import FlaskClient

sys.path.append(str(Path(__file__).resolve().parent.parent))

from app import create_app
from models import Loan, LoanPayment
from datastore import InMemoryDataStore
from tests.factories import LoanFactory, LoanPaymentFactory
from container import Container
from services import LoanService


@pytest.fixture
def app() -> Generator[Flask, None, None]:
    app = create_app()
    app.config["TESTING"] = True
    yield app


@pytest.fixture
def client(app: Flask) -> Generator[FlaskClient, None, None]:
    with app.test_client() as client:
        yield client

@pytest.fixture
def loan_datastore() -> InMemoryDataStore[Loan]:
    # 5 dummy loans created using our LoanFactory
    loans = [cast(Loan, LoanFactory()) for _ in range(5)]
    return InMemoryDataStore[Loan](loans)


@pytest.fixture
def payment_datastore(loan_datastore: InMemoryDataStore[Loan]) -> InMemoryDataStore[LoanPayment]:
    payments: list[LoanPayment] = []
    all_loans = loan_datastore.get_all(limit=None, cursor=None)
    for i, loan in enumerate(all_loans):
        # Skip creating payments for the first loan to test no-payment scenario
        if i == 0:
            continue
        
        payments.extend([
            # Create one or two payments per loan
            cast(LoanPayment, LoanPaymentFactory(loan=loan))
            for _ in range(1, 3)
        ])
    return InMemoryDataStore[LoanPayment](payments)


@pytest.fixture(autouse=True)
def setup_container(
    loan_datastore: InMemoryDataStore[Loan],
    payment_datastore: InMemoryDataStore[LoanPayment],
) -> Generator[None, None, None]:
    Container.override(
        loan_datastore=loan_datastore,
        payment_datastore=payment_datastore,
    )
    yield
    Container.reset()


@pytest.fixture
@pytest.mark.usefixtures("setup_container")
def loan_service() -> LoanService:
    return Container.loan_service()