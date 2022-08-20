from .accounts import AccountQueries
from .currencies import CurrencyQueries
from .transfers import TransferQueries

account_queries = AccountQueries()
currency_queries = CurrencyQueries()
transfer_queries = TransferQueries()

__all__ = ["account_queries", "currency_queries", "transfer_queries"]
