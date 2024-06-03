from django.dispatch import receiver
from django.db.models.signals import post_save
from rental.models import Customer, Property, Ledger, Invoice, ledger_last_balance
from django.core.exceptions import ValidationError
from django.utils import timezone


@receiver(post_save, sender=Invoice)
def create_ledger_entry(sender, instance, created, **kwargs):
    if created:
        customer = instance.customer
        amount = instance.total_price
        last_balance = ledger_last_balance(customer)
        new_balance = last_balance - amount
        try:
            company_balance = Ledger.objects.latest(
                'created_date').company_balance-float(amount)
        except:
            company_balance = -float(amount)
        Ledger.objects.create(
            customer=customer,
            _type='Debit',
            particular=f'Invoice for {instance.month_name}',
            amount=amount,
            balance=new_balance,
            company_balance=company_balance,
            remarks=instance.remarks,
            entry_type='Invoice',
            leaserid=str(instance.id),
            expenses_date=instance.created_date
        )

    else:
        # Handle the cancellation of an invoice
        if instance.is_cancelled:
            if not instance.can_be_cancelled():
                raise ValidationError(
                    "Invoice can only be cancelled within 24 hours of creation.")

            customer = instance.customer
            amount = instance.total_price
            last_balance = ledger_last_balance(customer)
            new_balance = last_balance + amount

            Ledger.objects.create(
                customer=customer,
                _type='Credit',
                particular=f'Cancellation of Invoice for {instance.month_name}',
                amount=amount,
                balance=new_balance,
                company_balance=new_balance,
                remarks=f'Cancelled: {instance.remarks}',
                entry_type='Cancel Invoice',
                leaserid=str(instance.id),
                expenses_date=timezone.now()
            )
