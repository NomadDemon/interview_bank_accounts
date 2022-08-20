from dataclasses import dataclass
from decimal import Decimal

from django.db import transaction

from ..exceptions import (
    InvalidTransferCurrencyException,
    InvalidWithdrawAmountException,
)
from ..models import Transfer
from ..queries import account_queries, currency_queries


@dataclass(frozen=True, slots=True)
class WithdrawCommand:
    name: str
    from_account: int
    currency: int
    value: Decimal


class WithdrawUsecase:
    def execute(self, command: WithdrawCommand):
        account = account_queries.get_by_id(command.from_account)
        currency = currency_queries.get_by_id(command.currency)

        if account.currency != currency:
            raise InvalidTransferCurrencyException(
                "Account currency does not match withdrawal currency"
            )

        if command.value <= 0:
            raise InvalidWithdrawAmountException(
                "Withdraw amount must be higher than 0"
            )

        if command.value > account.funds:
            raise InvalidWithdrawAmountException(
                "Withdraw amount cannot be higher than available funds"
            )

        with transaction.atomic():
            Transfer.objects.create(
                name=command.name,
                from_account=account,
                currency=currency,
                value=command.value,
            )

            account.funds -= command.value
            account.save()
