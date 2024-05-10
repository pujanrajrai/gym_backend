# In your app's models.py file

from django.db import models
from accounts.models import UserProfile
from plan.models import Plan
from base.models import BaseModel
from datetime import datetime, timedelta


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
