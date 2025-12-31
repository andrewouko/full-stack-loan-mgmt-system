from typing import Optional
import strawberry

from models import Loan, LoanFilter, LoanPaymentResponse, PaginatedResult
from container import Container


@strawberry.type
class Query:

    @strawberry.field
    def loans(self, cursor: Optional[int] = None, limit: Optional[int] = None, filter: Optional[LoanFilter] = None) -> PaginatedResult[Loan]:
        loan_service = Container.loan_service()
        items, pagination_params = loan_service.get_loans(
            cursor, limit, filter)
        return PaginatedResult[Loan](items=items, pagination_params=pagination_params)

    @strawberry.field
    def loan(self, loan_id: int) -> Optional[Loan]:
        loan_service = Container.loan_service()
        return loan_service.get_loan_by_id(loan_id)

    @strawberry.field
    def loan_payments(self, loan_id: int, cursor: Optional[int] = None, limit: Optional[int] = None) -> PaginatedResult[LoanPaymentResponse]:
        loan_service = Container.loan_service()
        items, pagination_params = loan_service.get_loan_payments(
            loan_id, cursor, limit)
        return PaginatedResult[LoanPaymentResponse](items=items, pagination_params=pagination_params)


schema = strawberry.Schema(query=Query)
