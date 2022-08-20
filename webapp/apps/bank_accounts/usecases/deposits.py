from dataclasses import dataclass
from decimal import Decimal

from django.db import transaction

from ..exceptions import (
    InvalidDepositAmountException,
    InvalidTransferCurrencyException,
)
from ..models import Transfer
from ..queries import account_queries, currency_queries


@dataclass(frozen=True, slots=True)
class DepositCommand:
    name: str
    to_account: int
    currency: int
    value: Decimal


class DepositUsecase:
    def execute(self, command: DepositCommand):
        account = account_queries.get_by_id(command.to_account)
        currency = currency_queries.get_by_id(command.currency)

        if account.currency != currency:
            raise InvalidTransferCurrencyException(
                "Account currency does not match deposit currency"
            )

        if command.value <= 0:
            raise InvalidDepositAmountException(
                "Deposit amount must be higher than 0"
            )

        with transaction.atomic():
            Transfer.objects.create(
                name=command.name,
                to_account=account,
                currency=currency,
                value=command.value,
            )
            account.funds += command.value
            account.save()
