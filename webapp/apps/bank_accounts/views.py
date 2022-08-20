from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from django.views.generic import TemplateView

from .exceptions import (
    CannotTransferToSameAccountException,
    InvalidCurrencyException,
    InvalidDepositAmountException,
    InvalidTransferCurrencyException,
    InvalidWithdrawAmountException,
)
from .forms import (
    AddAccountForm,
    AddCurrencyForm,
    DepositForm,
    HistoryFilterForm,
    TransferForm,
    WithdrawForm,
)
from .queries import account_queries, currency_queries, transfer_queries
from .usecases import (
    AddAccountCommand,
    AddAccountUsecase,
    AddCurrencyCommand,
    AddCurrencyUsecase,
    DepositCommand,
    DepositUsecase,
    TransferCommand,
    TransferUsecase,
    WithdrawCommand,
    WithdrawUsecase,
)


class HomeView(TemplateView):
    template_name = "subpages/home.html"

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        context["available_currencies"] = currency_queries.get_all()
        context["available_accounts"] = account_queries.get_all()
        return self.render_to_response(context)


class AddAccountView(TemplateView):
    template_name = "subpages/add_account.html"

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        form = AddAccountForm()
        context["add_account_form"] = form

        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        form = AddAccountForm(data=request.POST)
        context["add_account_form"] = form

        if form.is_valid():
            entity = AddAccountCommand(**form.cleaned_data)
            usecase = AddAccountUsecase()
            new_account = form.cleaned_data["name"]

            try:
                usecase.execute(entity)

            except IntegrityError:
                message = (
                    f"Cannot add account, '{new_account}' already in database"
                )
                form.errors["internal"] = form.error_class([message])
                return self.render_to_response(context, status=400)

            else:
                context["success"] = True
                context["account_name"] = new_account

            return self.render_to_response(context)

        else:
            return self.render_to_response(context, status=400)


class AddCurrencyView(TemplateView):
    template_name = "subpages/add_currency.html"

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        form = AddCurrencyForm()
        context["add_currency_form"] = form

        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        form = AddCurrencyForm(data=request.POST)
        context["add_currency_form"] = form

        if form.is_valid():
            entity = AddCurrencyCommand(**form.cleaned_data)
            usecase = AddCurrencyUsecase()
            new_currency = form.cleaned_data["symbol"]

            try:
                usecase.execute(entity)

            except IntegrityError:
                message = f"Cannot add currency, '{new_currency}' already in database"
                form.errors["internal"] = form.error_class([message])
                return self.render_to_response(context, status=400)

            except InvalidCurrencyException as ex:
                form.errors["internal"] = form.error_class([ex])
                return self.render_to_response(context, status=400)

            else:
                context["success"] = True
                context["symbol"] = new_currency

            return self.render_to_response(context)

        else:
            return self.render_to_response(context, status=400)


class HistoryView(TemplateView):
    template_name = "subpages/history.html"

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        form = HistoryFilterForm(request.GET)
        context["history_filters"] = form

        by_account = request.GET.get("by_account")

        if by_account:
            context["transfers"] = transfer_queries.get_filtered_by_account(
                by_account
            )

        else:
            context["transfers"] = transfer_queries.get_all()

        return self.render_to_response(context)


class DepositView(TemplateView):
    template_name = "subpages/deposit.html"

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        form = DepositForm()
        context["deposit_form"] = form

        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        form = DepositForm(data=request.POST)
        context["deposit_form"] = form

        if form.is_valid():
            entity = DepositCommand(**form.cleaned_data)
            usecase = DepositUsecase()

            try:
                usecase.execute(entity)

            except (
                InvalidTransferCurrencyException,
                InvalidDepositAmountException,
                ObjectDoesNotExist,
            ) as ex:
                form.errors["internal"] = form.error_class([ex])
                return self.render_to_response(context, status=400)

            else:
                context["success"] = True
                context["value"] = form.cleaned_data["value"]
                context["account"] = form.cleaned_data["to_account"]

            return self.render_to_response(context)

        else:
            return self.render_to_response(context, status=400)


class WithdrawView(TemplateView):
    template_name = "subpages/withdraw.html"

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        form = WithdrawForm()
        context["withdraw_form"] = form

        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        form = WithdrawForm(data=request.POST)
        context["withdraw_form"] = form

        if form.is_valid():
            entity = WithdrawCommand(**form.cleaned_data)
            usecase = WithdrawUsecase()

            try:
                usecase.execute(entity)

            except (
                InvalidTransferCurrencyException,
                InvalidWithdrawAmountException,
                ObjectDoesNotExist,
            ) as ex:
                form.errors["internal"] = form.error_class([ex])
                return self.render_to_response(context, status=400)

            else:
                context["success"] = True
                context["value"] = form.cleaned_data["value"]
                context["account"] = form.cleaned_data["from_account"]

            return self.render_to_response(context)

        else:
            return self.render_to_response(context, status=400)


class TransferView(TemplateView):
    template_name = "subpages/transfer.html"

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        form = TransferForm()
        context["transfer_form"] = form

        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        form = TransferForm(data=request.POST)
        context["transfer_form"] = form

        if form.is_valid():
            entity = TransferCommand(**form.cleaned_data)
            usecase = TransferUsecase()

            try:
                usecase.execute(entity)

            except (
                InvalidTransferCurrencyException,
                InvalidWithdrawAmountException,
                CannotTransferToSameAccountException,
                ObjectDoesNotExist,
            ) as ex:
                form.errors["internal"] = form.error_class([ex])
                return self.render_to_response(context, status=400)

            else:
                context["success"] = True
                context["value"] = form.cleaned_data["value"]
                context["from_account"] = form.cleaned_data["from_account"]
                context["to_account"] = form.cleaned_data["to_account"]

            return self.render_to_response(context)

        else:
            return self.render_to_response(context, status=400)
