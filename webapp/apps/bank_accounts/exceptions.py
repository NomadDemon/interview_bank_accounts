class InvalidTransferCurrencyException(Exception):
    """
    When there is something wrong with currencies between
    accounts and transfer currency.
    """


class InvalidDepositAmountException(Exception):
    """
    When deposit amount is not positive number.
    """


class InvalidWithdrawAmountException(Exception):
    """
    When withdraw amount is not positive number or is higher than available funds.
    """


class CannotTransferToSameAccountException(Exception):
    """
    When try to transfer from same account to same account.
    """


class InvalidCurrencyException(Exception):
    """
    When currency symbol is not valid.
    """
