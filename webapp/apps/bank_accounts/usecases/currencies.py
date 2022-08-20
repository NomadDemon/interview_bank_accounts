from dataclasses import dataclass

from django.db import transaction

from ..exceptions import InvalidCurrencyException
from ..models import Currency


@dataclass(frozen=True, slots=True)
class AddCurrencyCommand:
    symbol: str


class AddCurrencyUsecase:
    def execute(self, command: AddCurrencyCommand):
        if len(command.symbol) != 3:
            raise InvalidCurrencyException(
                "Account currency does not match deposit currency"
            )

        with transaction.atomic():
            Currency.objects.create(symbol=command.symbol)
