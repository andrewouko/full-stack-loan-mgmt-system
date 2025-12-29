from typing import Any, cast
from flask.testing import FlaskClient

from models import Loan
from repositories import InMemoryRepository


class TestGraphQLRoute:
    def test_get_existing_loans(self, client: FlaskClient, loan_repo: InMemoryRepository[Loan]):
        query = """
        query {
            loans {
                id
                name
                principal
                interestRate
                dueDate
            }
        }
        """
        response = client.post("/graphql", json={"query": query})
        assert response.status_code == 200
        data = response.get_json()
        assert data is not None
        assert "data" in data
        assert "loans" in data["data"]
        loans = data["data"]["loans"]
        assert isinstance(loans, list)
        assert len(cast(list[Loan], loans)) == len(
            loan_repo.get_all(limit=None, cursor=None))

    def test_get_loan_by_id(self, client: FlaskClient, loan_repo: InMemoryRepository[Loan]):
        # Pick a loan from the repo
        existing_loan = loan_repo.get_all(limit=1, cursor=None)[0]
        query = f"""
        query {{
            loan(loanId: {existing_loan.id}) {{
                id
                name
                principal
                interestRate
                dueDate
            }}
        }}
        """
        response = client.post("/graphql", json={"query": query})
        assert response.status_code == 200
        data = response.get_json()
        assert data is not None
        assert "data" in data
        assert "loan" in data["data"]
        loan = data["data"]["loan"]
        assert loan is not None
        assert loan["id"] == existing_loan.id
        assert loan["name"] == existing_loan.name
        assert loan["principal"] == existing_loan.principal
        assert loan["interestRate"] == existing_loan.interest_rate
        assert loan["dueDate"] == existing_loan.due_date.isoformat()

    def test_get_loan_payments(self, client: FlaskClient, loan_repo: InMemoryRepository[Loan]):
        # Pick a loan from the repo with payments
        existing_loan = loan_repo.get_all(limit=None, cursor=None)[1]
        query = f"""
        query {{
            loanPayments(loanId: {existing_loan.id}) {{
                id
                loanId
                paymentDate
                amount
                status
            }}
        }}
        """
        response = client.post("/graphql", json={"query": query})
        assert response.status_code == 200
        data = response.get_json()
        assert data is not None
        assert "data" in data
        assert "loanPayments" in data["data"]
        payments = cast(list[dict[str, Any]], data["data"]["loanPayments"])
        assert isinstance(payments, list)
        assert len(payments) >= 1
        print(f"Payments retrieved: {payments}")
        assert all(payment["loanId"] == existing_loan.id for payment in payments)