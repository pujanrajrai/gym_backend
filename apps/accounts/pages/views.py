from django.contrib.auth import logout
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from accounts.models.users import User
from accounts.models.profiles import StaffProfile, UserProfile
from .forms import CreateAdminForm, CreateStaffForm, CreateUserForm, StaffProfileUpdateForm, UserProfileUpdateForm, AdminProfileUpdateForm
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from decorators import has_roles




@method_decorator(login_required(), name='dispatch')
@method_decorator(has_roles(['admin','staff']), name='dispatch')
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
        return reverse_lazy('accounts:pages:user_list')

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
        return reverse_lazy('accounts:pages:user_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current'] = 'users'
        return context


@method_decorator(login_required(), name='dispatch')
@method_decorator(has_roles(['admin','staff']), name='dispatch')
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
        return reverse_lazy('accounts:pages:user_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current'] = 'users'
        return context



@login_required()
@has_roles(['admin','staff'])
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
@has_roles(['admin','staff'])
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
@method_decorator(has_roles(['admin','staff']), name='dispatch')
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
    import pdb;pdb.set_trace()
    if user.role == "admin":
        return redirect(f'/accounts/pages/admindetail/{user.pk}/')
    elif user.role == "staff":
        staffprofile = StaffProfile.objects.get(user=user)
        return redirect(f'/accounts/pages/staffdetail/{staffprofile.pk}/')
    elif user.role == "user":
        # userprofile = UserProfile.objects.get(user=user)
        return redirect(f'/plan/pages/userplan/create/user/plan/{user.pk}/')
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
@method_decorator(has_roles(['admin','staff']), name='dispatch')
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
