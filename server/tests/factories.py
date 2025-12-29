from datetime import timedelta
import factory
from faker import Faker

from models import Loan, LoanPayment

faker = Faker()


class LoanFactory(factory.Factory):
    class Meta:
        model = Loan

    id = factory.Sequence(lambda n: n + 1)
    name = factory.Faker('company')
    interest_rate = factory.Faker(
        'pyfloat', min_value=1.0, max_value=15.0, right_digits=2)
    principal = factory.Faker(
        'pyfloat', min_value=1000.0, max_value=100_000.0, right_digits=2)
    due_date = factory.Faker(
        'date_between', start_date='+30d', end_date='+365d')


class LoanPaymentFactory(factory.Factory):
    class Meta:
        model = LoanPayment
        exclude = ('loan',)

    id = factory.Sequence(lambda n: n + 1)

    loan = factory.SubFactory(LoanFactory)
    
    loan_id = factory.LazyAttribute(lambda obj: obj.loan.id)
    amount = factory.LazyAttribute(
        lambda o: min(
            faker.pyfloat(min_value=100.0, max_value=10_000.0, right_digits=2),
            o.loan.principal + (o.loan.interest_rate / 100) * o.loan.principal
        )
    )
    payment_date = factory.LazyAttribute(lambda o: o.loan.due_date)
    status = None
    
    class Params:
        unpaid = factory.Trait(payment_date=None)
        late = factory.Trait(
            payment_date=factory.LazyAttribute(lambda o: o.loan.due_date + timedelta(days=10))
        )
        defaulted = factory.Trait(
            payment_date=factory.LazyAttribute(lambda o: o.loan.due_date + timedelta(days=60))
        )
