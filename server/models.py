from dataclasses import dataclass
import enum
from typing import Generic, Literal, Optional, TypeVar, List
import strawberry
import datetime

DataStoreType = Literal["in_memory", "database"]


@dataclass
class Config:
    datastore_type: DataStoreType = "in_memory"  # or "database"
    database_url: Optional[str] = None


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


@dataclass
class LoanPayment:
    id: int
    loan_id: int
    payment_date: datetime.date
    amount: float

    def to_dict(self) -> dict[str, object]:
        return {
            "id": self.id,
            "loan_id": self.loan_id,
            "payment_date": self.payment_date.isoformat(),
            "amount": self.amount,
        }


@strawberry.enum
class PaymentStatus(enum.Enum):
    UNPAID = "Unpaid"
    ON_TIME = "On Time"
    LATE = "Late"
    DEFAULTED = "Defaulted"


@strawberry.type
@dataclass
class LoanPaymentResponse:
    id: int
    name: str
    interest_rate: float
    principal: float
    due_date: datetime.date
    status: PaymentStatus
    amount: float
    payment_date: Optional[datetime.date] = None

@strawberry.type
@dataclass
class PaginationResult:
    total_items: int
    next_cursor: Optional[int] = None

# Generic type variable for paginated results
T = TypeVar("T")
@strawberry.type
@dataclass
class PaginatedResult(Generic[T]):
    """Generic paginated result wrapper for any list type."""
    items: List[T]
    pagination_params: PaginationResult