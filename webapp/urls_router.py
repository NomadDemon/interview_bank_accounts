from django.urls import include, path

urlpatterns = [
    path("", include("apps.bank_accounts.urls", namespace="bank-accounts")),
]
