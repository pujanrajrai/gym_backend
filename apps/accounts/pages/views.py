from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from accounts.models.users import User
from accounts.models.profiles import StaffProfile,UserProfile
from .forms import CreateAdminForm,CreateStaffForm,CreateUserForm,StaffProfileUpdateForm,UserProfileUpdateForm
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.contrib import messages
from django.shortcuts import redirect,get_object_or_404

class UserListView(ListView):
    model = User
    template_name = 'users/list.html'
    context_object_name = 'users'


class CreateAdmin(SuccessMessageMixin, CreateView):
    model = User
    form_class = CreateAdminForm
    success_message = 'Admin Created Successfully'
    template_name = 'admin/create.html'

    def get_success_url(self):
        return reverse_lazy('accounts:pages:user_list')
 

class CreateStaff(SuccessMessageMixin, CreateView):
    model = User
    form_class = CreateStaffForm
    success_message = 'Staff Created Successfully'
    template_name = 'staff/create.html'

    def get_success_url(self):
        return reverse_lazy('accounts:pages:user_list')
 


class CreateUser(SuccessMessageMixin, CreateView):
    model = User
    form_class = CreateUserForm
    success_message = 'User Created Successfully'
    template_name = 'users/create.html'

    def get_success_url(self):
        return reverse_lazy('accounts:pages:user_list')
 


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


class StaffProfileDetailView(DetailView):
    model = StaffProfile
    template_name = 'staff/detail.html'
    context_object_name = 'staff_detail'

class UserProfileDetailView(DetailView):
    model = UserProfile
    template_name = 'users/detail.html'
    context_object_name = 'user_detail'



def profile_redirect(request, id):
    user = User.objects.get(pk=id)
    if user.role == "admin":
        pass
        # adminprofile = AdminProfile.objects.get(user=user)
        # return redirect(f'/dashboard/user/admindetail/{adminprofile.pk}/')
    elif user.role == "staff":
        staffprofile = StaffProfile.objects.get(user=user)
        return redirect(f'/accounts/pages/staffdetail/{staffprofile.pk}/')
    elif user.role == "user":
        userprofile = UserProfile.objects.get(user=user)
        return redirect(f'/accounts/pages/userdetail/{userprofile.pk}/')
    else:
        pass
        # raise Httpresponse error something went wrong



class StaffProfileUpdateView(SuccessMessageMixin, UpdateView):
    form_class = StaffProfileUpdateForm
    success_message = 'Staff Profile Updated Successfully'
    model = StaffProfile
    template_name = 'staff/update.html'

    def get_success_url(self):
        user_id = StaffProfile.objects.get(pk=self.kwargs['pk']).id
        return reverse_lazy('accounts:pages:staff_detail', kwargs={'pk': user_id})

class UserProfileUpdateView(SuccessMessageMixin, UpdateView):
    form_class = UserProfileUpdateForm
    success_message = 'User Profile Updated Successfully'
    model = UserProfile
    template_name = 'users/update.html'

    def get_success_url(self):
        user_id = UserProfile.objects.get(pk=self.kwargs['pk']).id
        return reverse_lazy('accounts:pages:user_detail', kwargs={'pk': user_id})