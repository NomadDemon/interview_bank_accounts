from dataclasses import dataclass
from decimal import Decimal

from django.db import transaction

from ..models import Account
from ..queries import currency_queries


@dataclass(frozen=True, slots=True)
class AddAccountCommand:
    name: str
    description: str
    currency: int
    funds: Decimal


class AddAccountUsecase:
    def execute(self, command: AddAccountCommand):
        currency = currency_queries.get_by_id(command.currency)

        with transaction.atomic():
            Account.objects.create(
                name=command.name,
                description=command.description,
                currency=currency,
                funds=command.funds or 0,
            )
