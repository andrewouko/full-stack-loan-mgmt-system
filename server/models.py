from dataclasses import dataclass
from typing import Optional
import strawberry
import datetime


@strawberry.type
@dataclass
class Loan:
    id: int
    name: str
    interest_rate: float
    principal: float
    due_date: datetime.date


@strawberry.input
@dataclass
class LoanFilter:
    name: Optional[str] = None
    interest_rate: Optional[float] = None
    principal: Optional[float] = None
    due_date: Optional[datetime.date] = None


@dataclass
class LoanPaymentInput:
    loan_id: int
    amount: float


@strawberry.type
@dataclass
class LoanPayment:
    id: int
    loan_id: int
    payment_date: datetime.date
    amount: float
    status: Optional[str] = None
    
    def to_dict(self) -> dict[str, object]:
        return {
            "id": self.id,
            "loan_id": self.loan_id,
            "payment_date": self.payment_date,
            "amount": self.amount,
            "status": self.status,
        }
