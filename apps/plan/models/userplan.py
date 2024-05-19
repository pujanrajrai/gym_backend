# In your app's models.py file

import calendar
from datetime import date
from django.dispatch import receiver
from django.db import transaction
from django.db.models.signals import post_save
from django.db import models
from accounts.models import UserProfile
from plan.models import Plan
from base.models import BaseModel
from datetime import datetime, timedelta
from ledger.models import Ledger, ledger_last_balance

from datetime import timedelta


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

    def highest_ending_date(self):
        details = self.userplandetails.all()
        if not details:
            return None

        highest_ending = max(detail.ending_date() for detail in details)

        # Check if the highest ending date is in the past
        if highest_ending < datetime.now().date():
            return "Expired"
        else:
            return highest_ending

    def remaining_days(self):
        ending_date = self.highest_ending_date()
        if ending_date == "Expired":
            return "Expired"
        today = datetime.now().date()
        remaining = (ending_date - today).days
        return max(0, remaining)


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

    def ending_date(self):
        starting_date = self.userplan.starting_date
        months_to_add = self.plan.default_month

        # Calculate the new month and year
        new_month = starting_date.month + months_to_add
        new_year = starting_date.year + (new_month - 1) // 12
        new_month = (new_month - 1) % 12 + 1

        # Get the last day of the new month
        last_day_of_new_month = calendar.monthrange(new_year, new_month)[1]

        # Ensure the new day is within the valid range
        new_day = min(starting_date.day, last_day_of_new_month)

        return date(new_year, new_month, new_day)


@receiver(post_save, sender=UserPlan)
def create_ledger(sender, instance, created, **kwargs):
    try:
        company_balance = Ledger.objects.latest(
            'created_date').company_balance+instance.total
    except:
        company_balance = instance.total
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
                    balance=last_balance + instance.total,
                    company_balance=company_balance,
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
                    balance=last_balance - instance.total,
                    company_balance=Ledger.objects.latest(
                        'created_date').company_balance-instance.total,
                )
        except Exception as e:
            print(f"Error creating ledger entries: {e}")
            transaction.set_rollback(True)
