from .utils import issue_user_plan
from django.contrib import messages
from django.http import JsonResponse, HttpResponseRedirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from plan.models import Plan
from accounts.models.users import User
from accounts.models.profiles import UserProfile
from . forms import SearchCustomerForm, CreateUserForm, UserPlanForm
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.contrib.messages.views import SuccessMessageMixin
from plan.models import UserPlan, UserPlanDetail, UnConfirmUserPlanDetail, UnConfirmUserPlan


def getuserprofile(pk):
    user = User.objects.get(pk=pk)
    userprofile = UserProfile.objects.get(user=user)
    return userprofile


def search_customer(request):
    context = {
        "form": SearchCustomerForm(),
        "current": "search_user",
    }
    if request.method == "POST":
        phone_number = request.POST.get("phone_number")
        if phone_number:
            try:
                user = User.objects.get(phone_number=phone_number)
                if user.role == "user":
                    userprofile = UserProfile.objects.get(user=user)
                    return redirect(f'/plan/pages/userplan/current/plan/{user.pk}/')
                else:
                    messages.error(
                        request, "Phone number belongs to staff. Use Other Phone Number")
                    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            except User.DoesNotExist:
                return redirect(f'/plan/pages/userplan/create/user/?phone_number={phone_number}')

    return render(request, 'plan/search_customer.html', context)


class SearchCustomerAPIView(View):
    def get(self, request, *args, **kwargs):
        suggestions = User.objects.filter(
            role='user').values_list('phone_number', flat=True)
        # Convert suggestions to a list and return as JSON
        suggestion_list = list(suggestions)
        return JsonResponse({'suggestions': suggestion_list})


class CreateUser(SuccessMessageMixin, CreateView):
    model = User
    form_class = CreateUserForm
    success_message = 'User Created Successfully'
    template_name = 'plan_user/create_user.html'

    def get_initial(self):
        initial = super().get_initial()
        initial['phone_number'] = self.request.GET.get('phone_number')
        return initial

    def get_success_url(self):
        return reverse_lazy('plan:pages:userplan:create_user_plan', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current'] = 'users'
        return context


def current_plan(request, pk):
    user = User.objects.get(pk=pk)
    userprofile = UserProfile.objects.get(user=user)
    userplan = UserPlan.objects.filter(userprofile=userprofile)
    mycurrent_plan = userplan.first()
    if userplan.count() == 0:
        return redirect(f'/plan/pages/userplan/create/user/plan/{user.pk}/')
    context = {
        "mycurrent_plan": mycurrent_plan,
        "userprofile": userprofile,
        "tab": "current_plan"
    }
    return render(request, 'plan/current_plan.html', context)


def usercreate_plan(request, pk):
    context = {}
    user = User.objects.get(pk=pk)
    if user.role == "user":
        userprofile = UserProfile.objects.get(user=user)
        userplan, created = UnConfirmUserPlan.objects.get_or_create(
            userprofile=userprofile
        )
        myplans = UnConfirmUserPlanDetail.objects.filter(
            userplan__userprofile=userprofile
        )
        context["myplans"] = myplans
        if request.method == "POST":
            # Pass userprofile to the form
            form = UserPlanForm(request.POST, userprofile=userprofile)
            if form.is_valid():
                UnConfirmUserPlanDetail.objects.create(
                    userplan=userplan,
                    # Use cleaned_data to get the selected plan directly from the form
                    plan=form.cleaned_data['plan']
                )
                return redirect(request.META.get('HTTP_REFERER'))
        else:
            # Pass userprofile to the form
            form = UserPlanForm(userprofile=userprofile)
        context["form"] = form
        context["userplan"] = userplan
        context["userprofile"] = userprofile
        context["tab"] = "add_new"
        return render(request, 'plan/create_user_plan.html', context)
    else:
        messages.error(
            request, "only user can have plans other cannot have plans")
        return redirect(request.META.get('HTTP_REFERER'))


def delete_user_plan(request, pk):
    userplan = UnConfirmUserPlanDetail.objects.get(pk=pk)
    userplan.hard_delete()
    messages.error(
        request, "Plan Removed Successfully")
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def issue_userplan(request, pk):
    unconfirm_userplan = UnConfirmUserPlan.objects.get(pk=pk)
    userprofile = unconfirm_userplan.userprofile
    discount = int(request.POST.get("discount"))

    if not discount:
        discount = 0
    response = issue_user_plan(pk=pk, discount=discount)
    message = response["message"]
    mystatus = response["status"]
    if mystatus:
        messages.success(request, f'{message}')
        return redirect('plan:pages:userplan:current_plan', pk=userprofile.user.pk)
    else:
        messages.error(request, f'{message}')
        return redirect(request.META.get('HTTP_REFERER'))
