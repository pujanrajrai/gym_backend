from base.models import BaseModel
from django.db import models
from rental.models import Customer, Ledger, ledger_last_balance
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.core.exceptions import ValidationError


class Payment(BaseModel):
    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE
    )
    amount = models.FloatField()
    is_cancelled = models.BooleanField(
        default=False
    )

    def __str__(self):
        return self.customer.name


@receiver(post_save, sender=Payment)
def add_payment_to_ledger(sender, instance, created, **kwargs):
    if created:
        customer = instance.customer
        amount = instance.amount
        last_balance = ledger_last_balance(customer)
        new_balance = last_balance + amount
        try:
            company_balance = Ledger.objects.latest(
                'created_date').company_balance+float(amount)
        except:
            company_balance = float(amount)
        Ledger.objects.create(
            customer=customer,
            _type='Credit',
            particular=f'Payment received from {customer.name}',
            amount=amount,
            balance=new_balance,
            company_balance=company_balance,
            remarks='Payment received',
            entry_type='Other',
            leaserid=str(instance.id),
        )
