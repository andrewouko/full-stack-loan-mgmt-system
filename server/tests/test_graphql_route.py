from typing import Any, cast
from flask.testing import FlaskClient

from models import Loan
from datastore import InMemoryDataStore


class TestGraphQLRoute:
    def test_get_existing_loans(self, client: FlaskClient, loan_datastore: InMemoryDataStore[Loan]):
        query = """
        query {
            loans {
                items {
                    id
                    name
                    interestRate
                    principal
                    dueDate
                }
                paginationParams {
                    totalItems
                    nextCursor
                }
            }
        }
        """
        response = client.post("/graphql", json={"query": query})
        assert response.status_code == 200
        data = response.get_json()
        assert data is not None
        loans = data["data"]["loans"]["items"]
        assert isinstance(loans, list)
        all_loans, _ = loan_datastore.get_all(limit=None, cursor=None)
        assert len(cast(list[Loan], loans)) == len(all_loans)

    def test_get_existing_loans_with_pagination(self, client: FlaskClient, loan_datastore: InMemoryDataStore[Loan]):
        query = """
        query {
            loans(cursor: 3, limit: 1) {
                items {
                    id
                    name
                    interestRate
                    principal
                    dueDate
                }
                paginationParams {
                    totalItems
                    nextCursor
                }
            }
        }
        """
        response = client.post("/graphql", json={"query": query})
        assert response.status_code == 200
        data = response.get_json()
        assert data is not None
        loans = data["data"]["loans"]["items"]
        pagination = data["data"]["loans"]["paginationParams"]
        # Should return 1 loan (limit=1)
        assert len(loans) == 1
        # totalItems should still reflect all loans
        all_loans, _ = loan_datastore.get_all(limit=None, cursor=None)
        assert pagination["totalItems"] == len(all_loans)

    def test_get_loan_by_id(self, client: FlaskClient, loan_datastore: InMemoryDataStore[Loan]):
        # Pick a loan from the repo
        all_loans, _ = loan_datastore.get_all(limit=1, cursor=None)
        existing_loan = all_loans[0]
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

    def test_get_loan_payments(self, client: FlaskClient, loan_datastore: InMemoryDataStore[Loan]):
        # Pick a loan from the repo with payments
        loans, _ = loan_datastore.get_all(limit=None, cursor=None)
        existing_loan = loans[1]

        query = f"""
        query {{
            loanPayments(loanId: {existing_loan.id}) {{
                items {{
                    id
                    name
                    interestRate
                    principal
                    dueDate
                    paymentDate
                    status
                }}
                paginationParams {{
                    totalItems
                    nextCursor
                }}
            }}
        }}
        """
        response = client.post("/graphql", json={"query": query})
        assert response.status_code == 200
        data = response.get_json()
        assert data is not None
        assert "data" in data
        assert "loanPayments" in data["data"]
        assert "items" in data["data"]["loanPayments"]
        assert "paginationParams" in data["data"]["loanPayments"]
        payments = cast(list[dict[str, Any]], data["data"]
                        ["loanPayments"]["items"])
        assert isinstance(payments, list)
        assert len(payments) >= 1
        assert all(payment["name"] ==
                   existing_loan.name for payment in payments)
