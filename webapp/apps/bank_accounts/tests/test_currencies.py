from django.urls import reverse

import pytest

from ..models import Currency


@pytest.mark.django_db()
class TestCurrenciesUsecases:
    @pytest.fixture(autouse=True, scope="function")
    def _prepare(self, client):
        self.client = client
        self.url = reverse("bank-accounts:add-currency")

    def test_add_new_currency(self):
        symbol = "USD"
        data = {"symbol": symbol}

        resp = self.client.post(self.url, data=data)

        assert resp.status_code == 200
        all_currencies = Currency.objects.all()
        assert len(all_currencies) == 1
        assert all_currencies[0].symbol == symbol

    def test_add_new_currency_and_another_one(self):
        symbol_1 = "USD"
        symbol_2 = "EUR"
        data_1 = {"symbol": symbol_1}
        data_2 = {"symbol": symbol_2}

        self.client.post(self.url, data=data_1)
        resp = self.client.post(self.url, data=data_2)

        assert resp.status_code == 200
        all_currencies = Currency.objects.all()
        assert len(all_currencies) == 2
        assert all_currencies[0].symbol == symbol_1
        assert all_currencies[1].symbol == symbol_2

    def test_add_new_currency_but_already_exist(self):
        symbol = "USD"
        data = {"symbol": symbol}
        Currency.objects.create(symbol=symbol)
        expected_errors = {
            "internal": ["Cannot add currency, 'USD' already in database"]
        }

        resp = self.client.post(self.url, data=data)

        assert resp.status_code == 400
        form = resp.context_data["add_currency_form"]
        assert form.errors == expected_errors
        all_currencies = Currency.objects.all()
        assert len(all_currencies) == 1
        assert all_currencies[0].symbol == symbol

    def test_add_new_currency_but_missing_data(self):
        data = {}
        expected_errors = {"symbol": ["This field is required."]}

        resp = self.client.post(self.url, data=data)

        assert resp.status_code == 400
        form = resp.context_data["add_currency_form"]
        assert form.errors == expected_errors
        all_currencies = Currency.objects.all()
        assert len(all_currencies) == 0

    def test_add_new_currency_but_invalid_data(self):
        symbol = "USDX"
        data = {"symbol": symbol}
        expected_errors = {
            "symbol": [
                "Ensure this value has at most 3 characters (it has 4)."
            ]
        }

        resp = self.client.post(self.url, data=data)

        assert resp.status_code == 400
        form = resp.context_data["add_currency_form"]
        assert form.errors == expected_errors
        all_currencies = Currency.objects.all()
        assert len(all_currencies) == 0
