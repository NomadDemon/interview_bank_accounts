from django.urls import reverse

import pytest

from ..models import Account, Currency, Transfer
from .utils import generate_fake_money_value


@pytest.mark.django_db()
class TestCurrenciesUsecases:
    @pytest.fixture(autouse=True, scope="function")
    def _prepare(self, client):
        self.client = client
        self.url = reverse("bank-accounts:history")
        self.currency = Currency.objects.create(symbol="USD")
        self.account_1 = Account.objects.create(
            name="test1",
            description="desc1",
            currency=self.currency,
            funds=1000,
        )
        self.account_2 = Account.objects.create(
            name="test2",
            description="desc2",
            currency=self.currency,
            funds=1000,
        )

    def _generate_fake_transactions(self):
        transfer_1 = Transfer.objects.create(
            name="transfer_1",
            from_account=self.account_1,
            to_account=self.account_2,
            currency=self.currency,
            value=generate_fake_money_value(),
        )
        transfer_2 = Transfer.objects.create(
            name="transfer_2",
            from_account=self.account_1,
            to_account=self.account_2,
            currency=self.currency,
            value=generate_fake_money_value(),
        )
        deposit_1 = Transfer.objects.create(
            name="deposit_1",
            to_account=self.account_1,
            currency=self.currency,
            value=generate_fake_money_value(),
        )
        deposit_2 = Transfer.objects.create(
            name="deposit_2",
            to_account=self.account_2,
            currency=self.currency,
            value=generate_fake_money_value(),
        )
        withdrawal_1 = Transfer.objects.create(
            name="withdrawal_1",
            to_account=self.account_1,
            currency=self.currency,
            value=generate_fake_money_value(),
        )
        withdrawal_2 = Transfer.objects.create(
            name="withdrawal_2",
            to_account=self.account_2,
            currency=self.currency,
            value=generate_fake_money_value(),
        )

        return [
            transfer_1,
            transfer_2,
            deposit_1,
            deposit_2,
            withdrawal_1,
            withdrawal_2,
        ]

    def test_history_show_all(self):
        prepared_objects = self._generate_fake_transactions()

        resp = self.client.get(self.url)

        assert resp.status_code == 200
        result_transfers = list(resp.context_data["transfers"])
        assert len(result_transfers) == 6
        assert result_transfers == prepared_objects

    def test_history_show_filtered(self):
        prepared_objects = self._generate_fake_transactions()
        filters = {"by_account": self.account_1.id}
        expected_result = [
            prepared_objects[0],
            prepared_objects[1],
            prepared_objects[2],
            prepared_objects[4],
        ]

        resp = self.client.get(self.url, filters)

        assert resp.status_code == 200
        result_transfers = list(resp.context_data["transfers"])
        assert len(result_transfers) == 4
        assert result_transfers == expected_result

    def test_history_show_all_but_no_entries(self):
        resp = self.client.get(self.url)

        assert resp.status_code == 200
        result_transfers = resp.context_data["transfers"]
        assert len(result_transfers) == 0
