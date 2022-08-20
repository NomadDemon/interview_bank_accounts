from dataclasses import dataclass
from decimal import Decimal

from django.db import transaction

from ..exceptions import (
    CannotTransferToSameAccountException,
    InvalidTransferCurrencyException,
    InvalidWithdrawAmountException,
)
from ..models import Transfer
from ..queries import account_queries, currency_queries


@dataclass(frozen=True, slots=True)
class TransferCommand:
    name: str
    from_account: int
    to_account: int
    currency: int
    value: Decimal


class TransferUsecase:
    def execute(self, command: TransferCommand):
        from_account = account_queries.get_by_id(command.from_account)
        to_account = account_queries.get_by_id(command.to_account)
        currency = currency_queries.get_by_id(command.currency)

        if command.from_account == command.to_account:
            raise CannotTransferToSameAccountException(
                "Source account is same as target account, its not allowed."
            )

        if from_account.currency != currency:
            raise InvalidTransferCurrencyException(
                "Source account currency does not match transfer currency"
            )

        if to_account.currency != currency:
            raise InvalidTransferCurrencyException(
                "Target account currency does not match transfer currency"
            )
        if command.value <= 0:
            raise InvalidWithdrawAmountException(
                "Transfer amount must be higher than 0"
            )

        if command.value > from_account.funds:
            raise InvalidWithdrawAmountException(
                "Transfer amount cannot be higher than available funds on source account"
            )

        with transaction.atomic():
            Transfer.objects.create(
                name=command.name,
                from_account=from_account,
                to_account=to_account,
                currency=currency,
                value=command.value,
            )

            from_account.funds -= command.value
            from_account.save()

            to_account.funds += command.value
            to_account.save()
