from decimal import Decimal
from accounts.models.users import User
from base.models import BaseModel
from django.db import models

from django.db.models.signals import post_save
from django.dispatch import receiver

leasertype = [
    ('Debit', 'Debit'),
    ('Credit', 'Credit')
]

entry_type = [
    ('Ledger Entry', 'Ledger Entry'),
    ('Invoice', 'Invoice'),
    ('Cancel Invoice', 'Cancel Invoice'),
    ('Salary', 'Salary'),
    ('Other', 'Other'),
]


class Ledger(BaseModel):
    user = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name="user_ledger"
    )

    _type = models.CharField(
        choices=leasertype,
        max_length=100,
        editable=False
    )
    particular = models.CharField(
        max_length=500,
        editable=False
    )
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        editable=False
    )

    balance = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        editable=False
    )
    company_balance = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        editable=False
    )
    remarks = models.CharField(
        max_length=1000
    )
    entry_type = models.CharField(
        choices=entry_type,
        editable=False,
        max_length=50
    )
    leaserid = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    def __str__(self):
        return f"{self.user}-{self._type}-{self.particular}-{self.amount}-{self.balance}"


def ledger_last_balance(user):
    try:
        user_last_balance = Ledger.objects.filter(
            user=user).latest('created_date').balance
    except Exception as e:
        print(f"Error getting user last balance: {e}")
        user_last_balance = 0
    return user_last_balance
