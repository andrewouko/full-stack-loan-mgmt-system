from typing import Union, cast
from flask.testing import FlaskClient

from models import Loan
from datastore import InMemoryDataStore
from tests.factories import LoanFactory


class TestRestRoutes:
    def test_home_route(self, client: FlaskClient):
        response = client.get("/")
        assert response.status_code == 200
        assert response.data.decode() == "Welcome to the Loan Application API"

    def test_add_loan_payment_route_success(self, client: FlaskClient, loan_datastore: InMemoryDataStore[Loan]):
        # loan for testing
        loan = cast(Loan, LoanFactory())
        loan_datastore.add(loan)

        payload: dict[str, Union[float, int]] = {
            "loan_id": loan.id,
            "amount": 100.0
        }

        response = client.post("/payment", json=payload)

        assert response.status_code == 201
        data = response.get_json()
        assert data is not None
        assert "id" in data
        assert "loan_id" in data
        assert "amount" in data
        assert "status" in data
        assert data["status"] is None
    
    def test_add_loan_paymment_invalid_payload(self, client: FlaskClient):
        payload = {
            "amount": 100.0
        }
        response = client.post("/payment", json=payload)
        assert response.status_code == 400
        data = response.get_json()
        assert data is not None
        assert "error" in data
        assert data["error"] == "loan_id must be a positive integer."
    
    def test_add_loan_payment_nonexistent_loan(self, client: FlaskClient):
        # Non-existent loan ID
        payload: dict[str, Union[int, float]] = {
            "loan_id": 9999,
            "amount": 100.0
        }
        response = client.post("/payment", json=payload)
        assert response.status_code == 400
        data = response.get_json()
        assert data is not None
        assert "error" in data
        assert data["error"] == "Loan with id 9999 does not exist."
    
    def test_add_loan_payment_excess_amount(self, client: FlaskClient, loan_datastore: InMemoryDataStore[Loan]):
        # loan for testing
        loan = cast(Loan, LoanFactory(principal=500.0, interest_rate=10))
        loan_datastore.add(loan)

        payload: dict[str, Union[int, float]] = {
            "loan_id": loan.id,
            "amount": 1000.0 # Excess amount
        }

        response = client.post("/payment", json=payload)
        assert response.status_code == 400
        data = response.get_json()
        assert data is not None
        assert "error" in data
        assert data["error"] == f"Payment exceeds total amount due for loan id {loan.id}. Total due: 550.0, already paid: 0, attempted payment: 1000.0."