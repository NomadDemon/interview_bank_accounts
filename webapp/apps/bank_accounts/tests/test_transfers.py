from decimal import Decimal

from django.urls import reverse

import pytest

from ..models import Account, Currency, Transfer
from .utils import funds_to_decimal, generate_fake_money_value


@pytest.mark.django_db()
class TestTransfersUsecases:
    @pytest.fixture(autouse=True, scope="function")
    def _prepare(self, client):
        self.client = client
        self.url = reverse("bank-accounts:transfer")
        self.currency = Currency.objects.create(symbol="USD")
        self.from_account = Account.objects.create(
            name="test1",
            description="desc1",
            currency=self.currency,
            funds=1000,
        )
        self.to_account = Account.objects.create(
            name="test2",
            description="desc2",
            currency=self.currency,
            funds=1000,
        )

    def _assert_error(
        self, resp, expected_errors, expected_from_funds, expected_to_funds
    ):
        assert resp.status_code == 400
        form = resp.context_data["transfer_form"]

        for k, v in expected_errors.items():
            assert str(form.errors[k][0]) == str(v[0])

        all_transfers = Transfer.objects.all()
        assert len(all_transfers) == 0
        self.from_account.refresh_from_db()
        self.to_account.refresh_from_db()
        assert self.from_account.funds == expected_from_funds
        assert self.to_account.funds == expected_to_funds

    def test_new_transfer(self):
        data = {
            "name": "withdraw1",
            "from_account": self.from_account.id,
            "to_account": self.to_account.id,
            "currency": self.currency.id,
            "value": generate_fake_money_value(),
        }
        expected_from_funds = self.from_account.funds - funds_to_decimal(
            data["value"]
        )
        expected_to_funds = self.to_account.funds + funds_to_decimal(
            data["value"]
        )

        resp = self.client.post(self.url, data=data)

        assert resp.status_code == 200
        all_transfers = Transfer.objects.all()
        assert len(all_transfers) == 1
        assert all_transfers[0].name == data["name"]
        assert all_transfers[0].from_account == self.from_account
        assert all_transfers[0].to_account == self.to_account
        assert all_transfers[0].currency == self.currency
        assert all_transfers[0].value == Decimal(str(data["value"]))
        self.from_account.refresh_from_db()
        self.to_account.refresh_from_db()
        assert self.from_account.funds == expected_from_funds
        assert self.to_account.funds == expected_to_funds

    def test_new_transfer_and_another_one(self):
        data_1 = {
            "name": "withdraw1",
            "from_account": self.from_account.id,
            "to_account": self.to_account.id,
            "currency": self.currency.id,
            "value": generate_fake_money_value(),
        }
        data_2 = {
            "name": "withdraw1",
            "from_account": self.from_account.id,
            "to_account": self.to_account.id,
            "currency": self.currency.id,
            "value": generate_fake_money_value(),
        }
        sum_values = funds_to_decimal(data_1["value"]) + funds_to_decimal(
            data_2["value"]
        )
        expected_from_funds = self.from_account.funds - sum_values
        expected_to_funds = self.to_account.funds + sum_values

        self.client.post(self.url, data=data_1)
        resp = self.client.post(self.url, data=data_2)

        assert resp.status_code == 200
        all_transfers = Transfer.objects.all()
        assert len(all_transfers) == 2
        assert all_transfers[0].name == data_1["name"]
        assert all_transfers[0].from_account == self.from_account
        assert all_transfers[0].to_account == self.to_account
        assert all_transfers[0].currency == self.currency
        assert all_transfers[0].value == funds_to_decimal(data_1["value"])
        assert all_transfers[1].name == data_2["name"]
        assert all_transfers[1].from_account == self.from_account
        assert all_transfers[0].to_account == self.to_account
        assert all_transfers[1].currency == self.currency
        assert all_transfers[1].value == funds_to_decimal(data_2["value"])
        self.from_account.refresh_from_db()
        self.to_account.refresh_from_db()
        assert self.from_account.funds == expected_from_funds
        assert self.to_account.funds == expected_to_funds

    def test_new_transfer_but_not_enough_funds(self):
        data = {
            "name": "withdraw1",
            "from_account": self.from_account.id,
            "to_account": self.to_account.id,
            "currency": self.currency.id,
            "value": self.from_account.funds + 0.01,
        }
        expected_errors = {
            "internal": [
                "Transfer amount cannot be higher than available funds on source account"
            ]
        }
        expected_from_funds = self.from_account.funds
        expected_to_funds = self.to_account.funds

        resp = self.client.post(self.url, data=data)

        self._assert_error(
            resp, expected_errors, expected_from_funds, expected_to_funds
        )

    def test_new_transfer_but_invalid_currency(self):
        data = {
            "name": "withdraw1",
            "from_account": self.from_account.id,
            "to_account": self.to_account.id,
            "currency": 0,
            "value": generate_fake_money_value(),
        }
        expected_errors = {
            "currency": [
                "Select a valid choice. 0 is not one of the available choices."
            ]
        }
        expected_from_funds = self.from_account.funds
        expected_to_funds = self.to_account.funds

        resp = self.client.post(self.url, data=data)

        self._assert_error(
            resp, expected_errors, expected_from_funds, expected_to_funds
        )

    def test_new_transfer_but_invalid_from_account(self):
        data = {
            "name": "withdraw1",
            "from_account": 0,
            "to_account": self.to_account.id,
            "currency": self.currency.id,
            "value": generate_fake_money_value(),
        }
        expected_errors = {
            "from_account": [
                "Select a valid choice. 0 is not one of the available choices."
            ]
        }
        expected_from_funds = self.from_account.funds
        expected_to_funds = self.to_account.funds

        resp = self.client.post(self.url, data=data)

        self._assert_error(
            resp, expected_errors, expected_from_funds, expected_to_funds
        )

    def test_new_transfer_but_invalid_to_account(self):
        data = {
            "name": "withdraw1",
            "from_account": self.from_account.id,
            "to_account": 0,
            "currency": self.currency.id,
            "value": generate_fake_money_value(),
        }
        expected_errors = {
            "to_account": [
                "Select a valid choice. 0 is not one of the available choices."
            ]
        }
        expected_from_funds = self.from_account.funds
        expected_to_funds = self.to_account.funds

        resp = self.client.post(self.url, data=data)

        self._assert_error(
            resp, expected_errors, expected_from_funds, expected_to_funds
        )

    def test_new_transfer_but_currency_doesn_not_match_from_account(self):
        another_currency = Currency.objects.create(symbol="XXX")
        another_account = Account.objects.create(
            name="test3",
            description="desc3",
            currency=another_currency,
            funds=1000,
        )
        data = {
            "name": "withdraw1",
            "from_account": self.from_account.id,
            "to_account": another_account.id,
            "currency": another_currency.id,
            "value": generate_fake_money_value(),
        }
        expected_errors = {
            "internal": [
                "Source account currency does not match transfer currency"
            ]
        }
        expected_from_funds = self.from_account.funds
        expected_to_funds = self.to_account.funds

        resp = self.client.post(self.url, data=data)

        self._assert_error(
            resp, expected_errors, expected_from_funds, expected_to_funds
        )

    def test_new_transfer_but_currency_doesn_not_match_to_account(self):
        another_currency = Currency.objects.create(symbol="XXX")
        another_account = Account.objects.create(
            name="test3",
            description="desc3",
            currency=another_currency,
            funds=1000,
        )
        data = {
            "name": "withdraw1",
            "from_account": another_account.id,
            "to_account": self.to_account.id,
            "currency": another_currency.id,
            "value": generate_fake_money_value(),
        }
        expected_errors = {
            "internal": [
                "Target account currency does not match transfer currency"
            ]
        }
        expected_from_funds = self.from_account.funds
        expected_to_funds = self.to_account.funds

        resp = self.client.post(self.url, data=data)

        self._assert_error(
            resp, expected_errors, expected_from_funds, expected_to_funds
        )

    @pytest.mark.parametrize(
        "value, error",
        [(-1, "Value cannot be less than 0"), ("abc", "Enter a number.")],
    )
    def test_new_transfer_but_invalid_value(self, value, error):
        data = {
            "name": "withdraw1",
            "from_account": self.from_account.id,
            "to_account": self.to_account.id,
            "currency": self.currency.id,
            "value": value,
        }
        expected_errors = {"value": [error]}
        expected_from_funds = self.from_account.funds
        expected_to_funds = self.to_account.funds

        resp = self.client.post(self.url, data=data)

        self._assert_error(
            resp, expected_errors, expected_from_funds, expected_to_funds
        )

    def test_new_transfer_but_missing_data(self):
        data = {}
        expected_errors = {
            "currency": ["This field is required."],
            "name": ["This field is required."],
            "from_account": ["This field is required."],
            "to_account": ["This field is required."],
            "value": ["This field is required."],
        }
        expected_from_funds = self.from_account.funds
        expected_to_funds = self.to_account.funds

        resp = self.client.post(self.url, data=data)

        self._assert_error(
            resp, expected_errors, expected_from_funds, expected_to_funds
        )
