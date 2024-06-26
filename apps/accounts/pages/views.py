from openpyxl import Workbook
from django.db.models import Sum, Q
from datetime import date, timedelta, datetime
from django.db.models import Prefetch
from datetime import datetime, timedelta
from django.contrib.auth import logout
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from accounts.models.users import User
from accounts.models.profiles import StaffProfile, UserProfile
from .forms import CreateAdminForm, CreateStaffForm, CreateUserForm, StaffProfileUpdateForm, UserProfileUpdateForm, AdminProfileUpdateForm, DateRangeForm
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from decorators import has_roles
from plan.models.userplan import UserPlan, UserPlanDetail
# from django.utils import timezone
from django.shortcuts import render
from django.http import HttpResponse
from ledger.models import Ledger


@method_decorator(login_required(), name='dispatch')
@method_decorator(has_roles(['admin']), name='dispatch')
class UserListView(ListView):
    model = User
    template_name = 'users/list.html'
    context_object_name = 'users'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current'] = 'users'
        return context

    def get_queryset(self):
        queryset = super().get_queryset()

        tab = self.request.GET.get('tab')
        if tab == None:
            tab = "user"
        if tab == 'admin':
            return queryset.filter(role='admin')
        elif tab == 'staff':
            return queryset.filter(role='staff')
        elif tab == 'user':
            return queryset.filter(role='user')
        return queryset


@method_decorator(login_required(), name='dispatch')
@method_decorator(has_roles(['admin']), name='dispatch')
class CreateAdmin(SuccessMessageMixin, CreateView):
    model = User
    form_class = CreateAdminForm
    success_message = 'Admin Created Successfully'
    template_name = 'admin/create.html'

    def get_success_url(self):
        return reverse_lazy('accounts:pages:user_list') + '?tab=admin'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current'] = 'users'
        return context


@method_decorator(login_required(), name='dispatch')
@method_decorator(has_roles(['admin']), name='dispatch')
class CreateStaff(SuccessMessageMixin, CreateView):
    model = User
    form_class = CreateStaffForm
    success_message = 'Staff Created Successfully'
    template_name = 'staff/create.html'

    def get_success_url(self):
        return reverse_lazy('accounts:pages:user_list') + '?tab=staff'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current'] = 'users'
        return context


@method_decorator(login_required(), name='dispatch')
@method_decorator(has_roles(['admin']), name='dispatch')
class CreateUser(SuccessMessageMixin, CreateView):
    model = User
    form_class = CreateUserForm
    success_message = 'User Created Successfully'
    template_name = 'users/create.html'

    def get_initial(self):
        initial = super().get_initial()
        initial['phone_number'] = self.request.GET.get('phone_number')
        return initial

    def get_success_url(self):
        return reverse_lazy('accounts:pages:user_list') + '?tab=user'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current'] = 'users'
        return context


@login_required()
@has_roles(['admin'])
def block_user(request, id):
    try:
        user = get_object_or_404(User, pk=id)

    except User.DoesNotExist:
        messages.error(request, 'User not found')
        return redirect('accounts:pages:user_list')
    except Exception as e:
        messages.error(
            request, 'Something went wrong. Could not block the user')
        return redirect('accounts:pages:user_list')
    if user.role != "superadmin":
        if not user == request.user:
            user.is_blocked = True
            user.save()
            messages.success(request, 'User blocked successfully')
            # Replace 'your_redirect_view_name' with the appropriate URL name
            return redirect('accounts:pages:user_list')
        else:
            messages.error(request, 'You cannot block yourself')
            return redirect('accounts:pages:user_list')
    else:
        messages.error(request, 'Super admin cannot be blocked')
        return redirect('accounts:pages:user_list')


@login_required()
@has_roles(['admin'])
def unblock_user(request, id):
    try:
        user = get_object_or_404(User, pk=id)
        user.is_blocked = False
        user.save()
        messages.success(request, 'User unblocked successfully')
        # Replace 'your_redirect_view_name' with the appropriate URL name
        return redirect('accounts:pages:user_list')
    except User.DoesNotExist:
        messages.error(request, 'User not found')
        return redirect('accounts:pages:user_list')
    except Exception as e:
        messages.error(
            request, 'Something went wrong. Could not unblock user.')
        return redirect('accounts:pages:user_list')


@method_decorator(login_required(), name='dispatch')
@method_decorator(has_roles(['admin']), name='dispatch')
class StaffProfileDetailView(DetailView):
    model = StaffProfile
    template_name = 'staff/detail.html'
    context_object_name = 'staff_detail'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current'] = 'users'
        return context


@method_decorator(login_required(), name='dispatch')
@method_decorator(has_roles(['admin']), name='dispatch')
class UserProfileDetailView(DetailView):
    model = UserProfile
    template_name = 'users/detail.html'
    context_object_name = 'user_detail'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current'] = 'users'
        return context


@method_decorator(login_required(), name='dispatch')
@method_decorator(has_roles(['admin']), name='dispatch')
class AdminProfileDetailView(DetailView):
    model = User
    template_name = 'admin/detail.html'
    context_object_name = 'admin_detail'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current'] = 'users'
        return context


def profile_redirect(request, id):
    user = User.objects.get(pk=id)
    if user.role == "admin":
        return redirect(f'/accounts/pages/admindetail/{user.pk}/')
    elif user.role == "staff":
        staffprofile = StaffProfile.objects.get(user=user)
        return redirect(f'/accounts/pages/staffdetail/{staffprofile.pk}/')
    elif user.role == "user":
        # userprofile = UserProfile.objects.get(user=user)
        return redirect(f'/plan/pages/userplan/current/plan/{user.pk}/')
    else:
        pass
        # raise Httpresponse error something went wrong


@method_decorator(login_required(), name='dispatch')
@method_decorator(has_roles(['admin']), name='dispatch')
class StaffProfileUpdateView(SuccessMessageMixin, UpdateView):
    form_class = StaffProfileUpdateForm
    success_message = 'Staff Profile Updated Successfully'
    model = StaffProfile
    template_name = 'staff/update.html'

    def get_success_url(self):
        user_id = StaffProfile.objects.get(pk=self.kwargs['pk']).id
        return reverse_lazy('accounts:pages:staff_detail', kwargs={'pk': user_id})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current'] = 'users'
        return context


@method_decorator(login_required(), name='dispatch')
@method_decorator(has_roles(['admin']), name='dispatch')
class AdminProfileUpdateView(SuccessMessageMixin, UpdateView):
    form_class = AdminProfileUpdateForm
    success_message = 'Admin Profile Updated Successfully'
    model = User
    template_name = 'admin/update.html'

    def get_success_url(self):
        user_id = User.objects.get(pk=self.kwargs['pk']).id
        return reverse_lazy('accounts:pages:admin_detail', kwargs={'pk': user_id})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current'] = 'users'
        return context


@method_decorator(login_required(), name='dispatch')
@method_decorator(has_roles(['admin']), name='dispatch')
class UserProfileUpdateView(SuccessMessageMixin, UpdateView):
    form_class = UserProfileUpdateForm
    success_message = 'User Profile Updated Successfully'
    model = UserProfile
    template_name = 'users/update.html'

    def get_success_url(self):
        user_profile = UserProfile.objects.get(pk=self.kwargs['pk'])
        user_id = user_profile.user.id
        return reverse_lazy('plan:pages:userplan:create_user_plan', kwargs={'pk': user_id})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current'] = 'users'
        return context


def logout_view(request):
    logout(request)
    return redirect('accounts:pages:users:login')


def custom_login(request):
    context = {"captcha_form": CaptchaFieldForm()}
    if request.user.is_authenticated:
        if request.user:
            return redirect('shipments:pages:shipments:list')
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        form = CaptchaFieldForm(request.POST)
        if not form.is_valid():
            context['captcha_errors'] = "Captcha Not Correct"
            context['username'] = username
            return render(request, 'accounts/usermanagement/login.html', context)
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('shipments:pages:shipments:list')
        else:
            context['errors'] = "User name or password is incorrect"
            context['username'] = username
            return render(request, 'accounts/usermanagement/login.html', context)
    return render(request, 'accounts/usermanagement/login.html', context)


# def expire_plan_list(request):
#     users = User.objects.filter(role="user")
#     context = {
#         "users": users,
#         "current": "expiry"
#     }
#     return render(request, 'users/aboutoexpire.html', context)


def expire_plan_list(request):
    # Fetch users with related data using select_related and prefetch_related
    users = User.objects.filter(role="user").select_related('user_profile').prefetch_related(
        Prefetch(
            'user_profile__userplan',
            queryset=UserPlan.objects.select_related(
                'userprofile').prefetch_related('userplandetails__plan')
        )
    )
    for user in users:
        for plan in user.user_profile.userplan.all():
            plan.highest_ending_date_value = plan.highest_ending_date()
            plan.remaining_days_value = plan.remaining_days()

    context = {
        "users": users,
        "current": "expiry"
    }
    return render(request, 'users/aboutoexpire.html', context)


@login_required
@has_roles(['admin'])
def dashboard_report(request):
    form = DateRangeForm(request.GET or None)
    context = {}

    if form.is_valid():
        date_range = form.cleaned_data.get('date_range')
        from_date = form.cleaned_data.get('from_date')
        to_date = form.cleaned_data.get('to_date')
        user_id = form.cleaned_data.get('user')
        context["user"] = user_id
        context["from_date"] = from_date
        context["to_date"] = to_date
        context["date_range"] = date_range

        # Filter data based on company if selected
        if user_id and user_id != 'All':
            user_filter = Q(userprofile__user=user_id)
        else:
            user_filter = Q()

        # Filter data based on date range
        if date_range == DateRangeForm.CUSTOM:
            # Custom date range
            date_filter = Q(created_date__range=[from_date, to_date])
        else:
            # Predefined date ranges
            today = date.today()
            if date_range == DateRangeForm.TODAY:
                date_filter = Q(created_date__range=[
                                today, today+timedelta(days=1)])
            elif date_range == DateRangeForm.YESTERDAY:
                date_filter = Q(created_date__range=[
                    today - timedelta(days=1), today])
            elif date_range == DateRangeForm.THIS_WEEK:
                start_of_week = today - timedelta(days=today.weekday())
                date_filter = Q(created_date__range=[
                                start_of_week, start_of_week + timedelta(days=6)])
            elif date_range == DateRangeForm.THIS_MONTH:
                start_of_month = today.replace(day=1)
                end_of_month = start_of_month.replace(
                    day=1, month=start_of_month.month + 1) - timedelta(days=1)
                date_filter = Q(created_date__range=[
                                start_of_month, end_of_month])
            elif date_range == DateRangeForm.LAST_MONTH:
                start_of_last_month = (today.replace(
                    day=1) - timedelta(days=1)).replace(day=1)
                end_of_last_month = start_of_last_month.replace(
                    day=1, month=start_of_last_month.month + 1) - timedelta(days=1)
                date_filter = Q(created_date__range=[
                                start_of_last_month, end_of_last_month])
            elif date_range == DateRangeForm.LAST_THREE_MONTHS:
                three_months_ago = today - timedelta(days=90)
                date_filter = Q(created_date__range=[
                                three_months_ago, today])
            elif date_range == DateRangeForm.THIS_YEAR:
                start_of_year = date(today.year, 1, 1)
                end_of_year = date(today.year, 12, 31)
                date_filter = Q(created_date__range=[
                                start_of_year, end_of_year])
            else:
                date_filter = Q()  # No filtering

        # Apply filters to queryset for each model
        total_income = UserPlan.objects.filter(user_filter).filter(
            date_filter).aggregate(total_sum=Sum('total'))['total_sum'] or 0

        # Calculate total salary
        total_salary = Ledger.objects.filter(date_filter).filter(
            entry_type="salary").aggregate(total_sum=Sum('amount'))['total_sum'] or 0

        # Calculate total expenses
        total_expenses = Ledger.objects.filter(date_filter).filter(
            entry_type="expenses").aggregate(total_sum=Sum('amount'))['total_sum'] or 0

        pl = total_income-total_salary-total_expenses
        # import pdb;pdb.set_trace()

    else:
        # If form is not valid, set totals to None
        total_income = None
        pl = None
        total_salary = None
        total_expenses = None

    context["total_income"] = total_income
    context["pl"] = pl
    context["total_salary"] = total_salary
    context["total_expenses"] = total_expenses
    context["current"] = "dashboard"
    context["form"] = form

    return render(request, 'dashboard.html', context)


@login_required
@has_roles(['admin'])
def dashboard_export(request):
    date_range = request.GET.get('date_range')
    from_date_str = request.GET.get('from_date')
    to_date_str = request.GET.get('to_date')
    user_id = request.GET.get('user')
    # Convert from_date and to_date from string to date using the correct format
    date_format = '%B %d, %Y'
    try:
        from_date = datetime.strptime(
            from_date_str, date_format) if from_date_str else None
    except Exception as e:
        from_date = None
    try:
        to_date = datetime.strptime(
            to_date_str, date_format) if to_date_str else None
    except Exception as e:
        to_date = None
    # Filter data based on company if selected
    if user_id and user_id != 'All':
        user_filter = Q(userprofile__user=user_id)
    else:
        user_filter = Q()
    # Filter data based on date range
    if date_range == DateRangeForm.CUSTOM:

        # Custom date range
        date_filter = Q(created_date__range=[from_date, to_date])
    else:
        # Predefined date ranges
        today = date.today()
        if date_range == DateRangeForm.TODAY:
            date_filter = Q(created_date__range=[
                            today, today+timedelta(days=1)])

        elif date_range == DateRangeForm.YESTERDAY:
            date_filter = Q(created_date__range=[
                today - timedelta(days=1), today])
        elif date_range == DateRangeForm.THIS_WEEK:
            start_of_week = today - timedelta(days=today.weekday())
            date_filter = Q(created_date__range=[
                            start_of_week, start_of_week + timedelta(days=6)])
        elif date_range == DateRangeForm.THIS_MONTH:
            start_of_month = today.replace(day=1)
            end_of_month = start_of_month.replace(
                day=1, month=start_of_month.month + 1) - timedelta(days=1)
            date_filter = Q(created_date__range=[
                            start_of_month, end_of_month])
        elif date_range == DateRangeForm.LAST_MONTH:
            start_of_last_month = (today.replace(
                day=1) - timedelta(days=1)).replace(day=1)
            end_of_last_month = start_of_last_month.replace(
                day=1, month=start_of_last_month.month + 1) - timedelta(days=1)
            date_filter = Q(created_date__range=[
                            start_of_last_month, end_of_last_month])
        elif date_range == DateRangeForm.LAST_THREE_MONTHS:
            three_months_ago = today - timedelta(days=90)
            date_filter = Q(created_date__range=[
                            three_months_ago, today])
        elif date_range == DateRangeForm.THIS_YEAR:
            start_of_year = date(today.year, 1, 1)
            end_of_year = date(today.year, 12, 31)
            date_filter = Q(created_date__range=[
                            start_of_year, end_of_year])
        else:
            date_filter = Q()  # No filtering
    queryset = UserPlan.objects.filter(user_filter).filter(date_filter)

    workbook = Workbook()
    worksheet = workbook.active

    # Add column headers
    headers = [
        'Date',
        'Full Name',
        'Phone Number',
        'Address',
        'Plan Name',
        'Starting Date',
        'Ending Date',
        'Remaining Days',
        'Total Cost',

    ]
    worksheet.append(headers)

    # Add data rows
    for item in queryset:
        # import pdb;pdb.set_trace()
        row_data = [
            item.created_date,
            item.userprofile.fullname,
            item.userprofile.user.phone_number,
            item.userprofile.address,
            item.userplandetails.first().plan.name if item.userplandetails else None,
            item.starting_date.strftime(
                '%Y-%m-%d %H:%M:%S') if item.created_date else None,
            item.highest_ending_date() if item.highest_ending_date() else None,
            item.remaining_days(),
            item.total,

        ]
        row_data = [str(value) if isinstance(value, datetime)
                    else value for value in row_data]
        worksheet.append(row_data)

    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=dashboard_export.xlsx'
    # messages.success(request, 'Ledger exported successfully.')
    workbook.save(response)

    return response
