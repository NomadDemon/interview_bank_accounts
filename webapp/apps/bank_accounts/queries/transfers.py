from django.db.models import Q

from ..models import Transfer
from .base import BaseQuery


class TransferQueries(BaseQuery):
    model = Transfer

    def get_filtered_by_account(self, account):
        return self.model.objects.filter(
            Q(from_account_id=account) | Q(to_account=account)
        )
