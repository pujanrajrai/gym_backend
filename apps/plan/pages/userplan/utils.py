from plan.models import UserPlan, UserPlanDetail, UnConfirmUserPlan, UnConfirmUserPlanDetail
from accounts.models import UserProfile
from django.db import transaction
from datetime import datetime, timedelta


def get_plan_ending_date(months):
    return datetime.now().date() + timedelta(months=months)


def issue_user_plan(pk, discount):
    try:
        unconfirm_userplan = UnConfirmUserPlan.objects.get(pk=pk)
        userprofile = unconfirm_userplan.userprofile
    except UnConfirmUserPlan.DoesNotExist:
        response = {
            "message": "User Plan not found. Couldnot issue",
            "status": False
        }
        return response

    if unconfirm_userplan.unconfirmuserplandetails.count() == 0:
        response = {
            "message": "Cannot Plan with no items",
            "status": False
        }
        return response
    try:
        with transaction.atomic():
            # Create a new credit sales bill
            userplan = UserPlan.objects.create(
                userprofile=userprofile,
                starting_date=unconfirm_userplan.starting_date,
                plan_price=unconfirm_userplan.total_price(),
                discount=discount,
                total=unconfirm_userplan.total_price()-discount,
            )
            # Transfer items from UnconfirmCreditSales to CreditSales
            for unconfirm_item in unconfirm_userplan.unconfirmuserplandetails.all():
                UserPlanDetail.objects.create(
                    userplan=userplan,
                    plan=unconfirm_item.plan,
                )
            # Delete the UnconfirmCreditSales and associated items
            unconfirm_userplan.hard_delete()
        response = {
            "message": "UserPlan Bill issued successfully",
            "status": True
        }
        return response
    except Exception as e:
        print(e)
        response = {
            "message": "Something Went Wrong",
            "status": False
        }
        return response
