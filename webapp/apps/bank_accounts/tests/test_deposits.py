from decimal import Decimal

from django.urls import reverse

import pytest

from ..models import Account, Currency, Transfer
from .utils import funds_to_decimal, generate_fake_money_value


@pytest.mark.django_db()
class TestDepositsUsecases:
    @pytest.fixture(autouse=True, scope="function")
    def _prepare(self, client):
        self.client = client
        self.url = reverse("bank-accounts:deposit")
        self.currency = Currency.objects.create(symbol="USD")
        self.account = Account.objects.create(
            name="test1",
            description="desc1",
            currency=self.currency,
            funds=0,
        )

    def _assert_error(self, resp, expected_errors, expected_funds):
        assert resp.status_code == 400
        form = resp.context_data["deposit_form"]
        assert form.errors == expected_errors
        all_transfers = Transfer.objects.all()
        assert len(all_transfers) == 0
        self.account.refresh_from_db()
        assert self.account.funds == expected_funds

    def test_new_deposit(self):
        data = {
            "name": "deposit1",
            "to_account": self.account.id,
            "currency": self.currency.id,
            "value": generate_fake_money_value(),
        }
        expected_funds = self.account.funds + funds_to_decimal(data["value"])

        resp = self.client.post(self.url, data=data)

        assert resp.status_code == 200
        all_transfers = Transfer.objects.all()
        assert len(all_transfers) == 1
        assert all_transfers[0].name == data["name"]
        assert all_transfers[0].from_account is None
        assert all_transfers[0].to_account == self.account
        assert all_transfers[0].currency == self.currency
        assert all_transfers[0].value == Decimal(str(data["value"]))
        self.account.refresh_from_db()
        assert self.account.funds == expected_funds

    def test_new_deposit_and_another_one(self):
        data_1 = {
            "name": "deposit1",
            "to_account": self.account.id,
            "currency": self.currency.id,
            "value": generate_fake_money_value(),
        }
        data_2 = {
            "name": "deposit1",
            "to_account": self.account.id,
            "currency": self.currency.id,
            "value": generate_fake_money_value(),
        }
        expected_funds = self.account.funds + (
            Decimal(str(data_1["value"])) + funds_to_decimal(data_2["value"])
        )

        self.client.post(self.url, data=data_1)
        resp = self.client.post(self.url, data=data_2)

        assert resp.status_code == 200
        all_transfers = Transfer.objects.all()
        assert len(all_transfers) == 2
        assert all_transfers[0].name == data_1["name"]
        assert all_transfers[0].from_account is None
        assert all_transfers[0].to_account == self.account
        assert all_transfers[0].currency == self.currency
        assert all_transfers[0].value == funds_to_decimal(data_1["value"])
        assert all_transfers[1].name == data_2["name"]
        assert all_transfers[1].from_account is None
        assert all_transfers[1].to_account == self.account
        assert all_transfers[1].currency == self.currency
        assert all_transfers[1].value == funds_to_decimal(data_2["value"])
        self.account.refresh_from_db()
        assert self.account.funds == expected_funds

    def test_new_deposit_but_invalid_currency(self):
        data = {
            "name": "deposit1",
            "to_account": self.account.id,
            "currency": 0,
            "value": generate_fake_money_value(),
        }
        expected_errors = {
            "currency": [
                "Select a valid choice. 0 is not one of the available choices."
            ]
        }
        expected_funds = self.account.funds

        resp = self.client.post(self.url, data=data)

        self._assert_error(resp, expected_errors, expected_funds)

    def test_new_deposit_but_invalid_account(self):
        data = {
            "name": "deposit1",
            "to_account": 0,
            "currency": self.currency.id,
            "value": generate_fake_money_value(),
        }
        expected_errors = {
            "to_account": [
                "Select a valid choice. 0 is not one of the available choices."
            ]
        }
        expected_funds = self.account.funds

        resp = self.client.post(self.url, data=data)

        self._assert_error(resp, expected_errors, expected_funds)

    def test_new_deposit_but_currency_doesn_not_match_account(self):
        another_currency = Currency.objects.create(symbol="XXX")
        data = {
            "name": "deposit1",
            "to_account": 0,
            "currency": another_currency.id,
            "value": generate_fake_money_value(),
        }
        expected_errors = {
            "to_account": [
                "Select a valid choice. 0 is not one of the available choices."
            ]
        }
        expected_funds = self.account.funds

        resp = self.client.post(self.url, data=data)

        self._assert_error(resp, expected_errors, expected_funds)

    @pytest.mark.parametrize(
        "value, error",
        [(-1, "Value cannot be less than 0"), ("abc", "Enter a number.")],
    )
    def test_new_deposit_but_invalid_value(self, value, error):
        data = {
            "name": "deposit1",
            "to_account": self.account.id,
            "currency": self.currency.id,
            "value": value,
        }
        expected_errors = {"value": [error]}
        expected_funds = self.account.funds

        resp = self.client.post(self.url, data=data)

        assert resp.status_code == 400
        form = resp.context_data["deposit_form"]
        assert form.errors == expected_errors
        all_transfers = Transfer.objects.all()
        assert len(all_transfers) == 0
        self.account.refresh_from_db()
        assert self.account.funds == expected_funds

    def test_new_deposit_but_missing_data(self):
        data = {}
        expected_errors = {
            "currency": ["This field is required."],
            "name": ["This field is required."],
            "to_account": ["This field is required."],
            "value": ["This field is required."],
        }
        expected_funds = self.account.funds

        resp = self.client.post(self.url, data=data)

        self._assert_error(resp, expected_errors, expected_funds)
