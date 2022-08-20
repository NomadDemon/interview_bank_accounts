from django.db import models


class Currency(models.Model):
    symbol = models.CharField(max_length=3, unique=True, verbose_name="Symbol")

    class Meta:
        verbose_name = "Currency"
        verbose_name_plural = "Currencies"

    def __str__(self):
        return self.symbol


class Account(models.Model):
    name = models.CharField(max_length=63, unique=True, verbose_name="Name")
    description = models.CharField(
        max_length=127, default="", verbose_name="Description"
    )
    currency = models.ForeignKey(
        Currency,
        on_delete=models.CASCADE,
        related_name="account_currency",
        verbose_name="Currency",
    )
    funds = models.DecimalField(
        max_digits=6, decimal_places=2, default=0, verbose_name="Funds"
    )
    created_date = models.DateTimeField(
        auto_now_add=True, verbose_name="Created date"
    )

    class Meta:
        verbose_name = "Account"
        verbose_name_plural = "Accounts"

    def __str__(self):
        return f"{self.name}"


class Transfer(models.Model):
    from_account = models.ForeignKey(
        Account,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="transfer_from",
    )
    to_account = models.ForeignKey(
        Account,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="transfer_to",
    )
    name = models.CharField(max_length=50, default="", verbose_name="name")
    currency = models.ForeignKey(
        Currency, on_delete=models.CASCADE, related_name="currency"
    )
    value = models.DecimalField(
        max_digits=6, decimal_places=2, verbose_name="value"
    )
    transfer_date = models.DateTimeField(
        auto_now_add=True, verbose_name="transfer date"
    )

    class Meta:
        verbose_name = "Transfer"
        verbose_name_plural = "Transfers"

    def __str__(self):
        return (
            f"Moved: {self.value}{self.currency}\n"
            f"{self.from_account} -> {self.to_account}"
        )
