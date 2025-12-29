from typing import List, Optional
import strawberry

from models import Loan, LoanFilter, LoanPayment
from container import Container


@strawberry.type
class Query:

    @strawberry.field
    def loans(self, cursor: Optional[int] = None, limit: Optional[int] = None, filter: Optional[LoanFilter] = None) -> List[Loan]:
        loan_service = Container.loan_service()
        return loan_service.get_loans(cursor, limit, filter)

    @strawberry.field
    def loan(self, loan_id: int) -> Optional[Loan]:
        loan_service = Container.loan_service()
        return loan_service.get_loan_by_id(loan_id)

    @strawberry.field
    def loan_payments(self, loan_id: int, cursor: Optional[int] = None, limit: Optional[int] = None) -> List[LoanPayment]:
        loan_service = Container.loan_service()
        return loan_service.get_loan_payments(loan_id, cursor, limit)


schema = strawberry.Schema(query=Query)
