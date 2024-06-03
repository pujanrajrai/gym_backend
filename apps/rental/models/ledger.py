from decimal import Decimal
from rental.models import Customer
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
    customer = models.ForeignKey(
        Customer,
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
    amount = models.FloatField(
        editable=False
    )

    balance = models.FloatField(

        editable=False
    )
    company_balance = models.FloatField(
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
    expenses_date = models.DateField(
        null=True,
        blank=True
    )

    def __str__(self):
        return f"{self.user}-{self._type}-{self.particular}-{self.amount}-{self.balance}"


def ledger_last_balance(customer):
    try:
        user_last_balance = Ledger.objects.filter(
            customer=customer).latest('created_date').balance
    except Exception as e:
        print(f"Error getting user last balance: {e}")
        user_last_balance = 0
    return user_last_balance
