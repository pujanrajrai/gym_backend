# In your app's models.py file

from django.dispatch import receiver
from django.db import transaction
from django.db.models.signals import post_save
from django.db import models
from accounts.models import UserProfile
from plan.models import Plan
from base.models import BaseModel
from datetime import datetime, timedelta
from ledger.models import Ledger, ledger_last_balance


def get_tomorrow():
    return datetime.now().date() + timedelta(days=1)


class UnConfirmUserPlan(BaseModel):
    userprofile = models.ForeignKey(
        UserProfile,
        on_delete=models.CASCADE,
        related_name="unconfirmuserplan"
    )
    starting_date = models.DateField(
        blank=True,
        null=True,
        default=get_tomorrow
    )

    def total_price(self):
        allplan = self.unconfirmuserplandetails.all()
        total = 0
        for plan in allplan:
            total += plan.plan.price
        return total


class UnConfirmUserPlanDetail(BaseModel):
    userplan = models.ForeignKey(
        UnConfirmUserPlan,
        on_delete=models.CASCADE,
        related_name='unconfirmuserplandetails'
    )
    plan = models.ForeignKey(
        Plan,
        on_delete=models.CASCADE
    )

    class Meta:
        unique_together = ['userplan', 'plan']


class UserPlan(BaseModel):
    userprofile = models.ForeignKey(
        UserProfile,
        on_delete=models.PROTECT,
        related_name="userplan"
    )
    starting_date = models.DateField()
    ending_date = models.DateField(
        null=True, blank=True
    )
    plan_price = models.PositiveIntegerField()
    discount = models.PositiveIntegerField()
    total = models.PositiveIntegerField()
    is_cancelled = models.BooleanField(default=False)


class UserPlanDetail(BaseModel):
    userplan = models.ForeignKey(
        UserPlan,
        on_delete=models.PROTECT,
        related_name="userplandetails"
    )
    plan = models.ForeignKey(
        Plan,
        on_delete=models.PROTECT
    )


@receiver(post_save, sender=UserPlan)
def create_ledger(sender, instance, created, **kwargs):
    if created:
        try:
            with transaction.atomic():
                user = instance.userprofile.user
                last_balance = ledger_last_balance(user)
                credit_ledger = Ledger.objects.create(
                    user=user,
                    _type="Credit",
                    particular="Invoice Total Amount",
                    amount=instance.total,
                    remarks="Invoice Total Amount",
                    entry_type="Invoice",
                    leaserid=instance.pk,
                    balance=last_balance + instance.total
                )
                print("success")
                print(credit_ledger)
        except Exception as e:
            print(f"Error creating ledger entriess: {e}")
            transaction.set_rollback(True)
    elif instance.is_cancelled:
        try:
            with transaction.atomic():
                user = instance.userprofile.user
                last_balance = ledger_last_balance(user)
                # Debit ledger entry
                debit_ledger = Ledger.objects.create(
                    user=user,
                    _type="Debit",
                    particular="Invoice Cancelled Amount",
                    amount=instance.total,
                    remarks="Invoice Cancelled Amount",
                    entry_type="Cancel Invoice",
                    leaserid=instance.pk,
                    balance=last_balance - instance.total
                )
        except Exception as e:
            print(f"Error creating ledger entries: {e}")
            transaction.set_rollback(True)
