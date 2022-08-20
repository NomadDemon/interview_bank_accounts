from django import forms
from django.core.validators import ValidationError

from .const import (
    CURRENCY_SYMBOL_PLACEHOLDER,
    CURRENCY_SYMBOL_VALIDATOR,
    MONEY_AMOUNT_PATTERN,
    MONEY_AMOUNT_PLACEHOLDER,
    NEGATIVE_VALUE_ERROR_MESSAGE,
)
from .queries import account_queries, currency_queries


class AddAccountForm(forms.Form):
    name = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "Name"})
    )
    description = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "Description"})
    )
    currency = forms.ChoiceField(choices=())
    funds = forms.DecimalField(
        widget=forms.TextInput(
            attrs={
                "placeholder": MONEY_AMOUNT_PLACEHOLDER,
                "pattern": MONEY_AMOUNT_PATTERN,
            }
        )
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        currency_choices = [
            (curr.pk, curr.symbol) for curr in currency_queries.get_all()
        ]
        self.fields["currency"].choices = currency_choices

    def clean_funds(self):
        funds = self.cleaned_data["funds"]

        if funds < 0:
            raise ValidationError(NEGATIVE_VALUE_ERROR_MESSAGE)

        return funds


class AddCurrencyForm(forms.Form):
    symbol = forms.CharField(
        max_length=3,
        min_length=3,
        widget=forms.TextInput(
            attrs={"placeholder": CURRENCY_SYMBOL_PLACEHOLDER}
        ),
    )

    def clean_symbol(self):
        symbol = self.cleaned_data["symbol"]

        if len(symbol) != 3:
            raise ValidationError(CURRENCY_SYMBOL_VALIDATOR)

        return symbol.upper()


class HistoryFilterForm(forms.Form):
    by_account = forms.ChoiceField(choices=())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        choices = [(acc.pk, acc.name) for acc in account_queries.get_all()]
        self.fields["by_account"].choices = choices


class DepositForm(forms.Form):
    name = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "Title"})
    )
    to_account = forms.ChoiceField(choices=())
    currency = forms.ChoiceField(choices=())
    value = forms.DecimalField(
        widget=forms.TextInput(
            attrs={
                "placeholder": MONEY_AMOUNT_PLACEHOLDER,
                "pattern": MONEY_AMOUNT_PATTERN,
            }
        )
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        currency_choices = [
            (curr.pk, curr.symbol) for curr in currency_queries.get_all()
        ]
        account_choices = [
            (acc.pk, acc.name) for acc in account_queries.get_all()
        ]
        self.fields["currency"].choices = currency_choices
        self.fields["to_account"].choices = account_choices

    def clean_value(self):
        value = self.cleaned_data["value"]

        if value < 0:
            raise ValidationError(NEGATIVE_VALUE_ERROR_MESSAGE)

        return value


class WithdrawForm(forms.Form):
    name = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "Title"})
    )
    from_account = forms.ChoiceField(choices=())
    currency = forms.ChoiceField(choices=())
    value = forms.DecimalField(
        widget=forms.TextInput(
            attrs={
                "placeholder": MONEY_AMOUNT_PLACEHOLDER,
                "pattern": MONEY_AMOUNT_PATTERN,
            }
        )
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        currency_choices = [
            (curr.pk, curr.symbol) for curr in currency_queries.get_all()
        ]
        account_choices = [
            (acc.pk, acc.name) for acc in account_queries.get_all()
        ]
        self.fields["currency"].choices = currency_choices
        self.fields["from_account"].choices = account_choices

    def clean_value(self):
        value = self.cleaned_data["value"]

        if value < 0:
            raise ValidationError(NEGATIVE_VALUE_ERROR_MESSAGE)

        return value


class TransferForm(forms.Form):
    name = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "Title"})
    )
    from_account = forms.ChoiceField(choices=())
    to_account = forms.ChoiceField(choices=())
    currency = forms.ChoiceField(choices=())
    value = forms.DecimalField(
        widget=forms.TextInput(
            attrs={
                "placeholder": MONEY_AMOUNT_PLACEHOLDER,
                "pattern": MONEY_AMOUNT_PATTERN,
            }
        )
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        currency_choices = [
            (curr.pk, curr.symbol) for curr in currency_queries.get_all()
        ]
        account_choices = [
            (acc.pk, acc.name) for acc in account_queries.get_all()
        ]
        self.fields["currency"].choices = currency_choices
        self.fields["from_account"].choices = account_choices
        self.fields["to_account"].choices = account_choices

    def clean_value(self):
        value = self.cleaned_data["value"]

        if value < 0:
            raise ValidationError(NEGATIVE_VALUE_ERROR_MESSAGE)

        return value
