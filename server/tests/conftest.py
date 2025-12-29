from pathlib import Path
import sys
from typing import Generator, cast

from flask import Flask
import pytest
from flask.testing import FlaskClient

sys.path.append(str(Path(__file__).resolve().parent.parent))

from app import create_app
from models import Loan, LoanPayment
from repositories import InMemoryRepository
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
def loan_repo() -> InMemoryRepository[Loan]:
    # 5 dummy loans created using our LoanFactory
    loans = [cast(Loan, LoanFactory()) for _ in range(5)]
    return InMemoryRepository[Loan](loans)


@pytest.fixture
def payment_repo(loan_repo: InMemoryRepository[Loan]) -> InMemoryRepository[LoanPayment]:
    payments: list[LoanPayment] = []
    all_loans = loan_repo.get_all(limit=None, cursor=None)
    for i, loan in enumerate(all_loans):
        # Skip creating payments for the first loan to test no-payment scenario
        if i == 0:
            continue
        
        payments.extend([
            # Create one or two payments per loan
            cast(LoanPayment, LoanPaymentFactory(loan=loan))
            for _ in range(1, 3)
        ])
    return InMemoryRepository[LoanPayment](payments)


@pytest.fixture(autouse=True)
def setup_container(
    loan_repo: InMemoryRepository[Loan],
    payment_repo: InMemoryRepository[LoanPayment],
) -> Generator[None, None, None]:
    Container.override(
        loan_repo=loan_repo,
        payment_repo=payment_repo,
    )
    yield
    Container.reset()


@pytest.fixture
@pytest.mark.usefixtures("setup_container")
def loan_service() -> LoanService:
    return Container.loan_service()