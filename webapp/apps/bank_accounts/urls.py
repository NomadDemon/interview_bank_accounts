from django.urls import path

from .views import (
    AddAccountView,
    AddCurrencyView,
    DepositView,
    HistoryView,
    HomeView,
    TransferView,
    WithdrawView,
)

app_name = "bank_accounts"

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path(
        "add_account/",
        AddAccountView.as_view(),
        kwargs={},
        name="add-account",
    ),
    path(
        "add_currency/",
        AddCurrencyView.as_view(),
        kwargs={},
        name="add-currency",
    ),
    path(
        "history/",
        HistoryView.as_view(),
        kwargs={},
        name="history",
    ),
    path(
        "deposit/",
        DepositView.as_view(),
        kwargs={},
        name="deposit",
    ),
    path(
        "withdraw/",
        WithdrawView.as_view(),
        kwargs={},
        name="withdraw",
    ),
    path(
        "transfer/",
        TransferView.as_view(),
        kwargs={},
        name="transfer",
    ),
]
