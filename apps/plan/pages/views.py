# In your app's views.py file

from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from plan.models import Plan
from accounts.models.users import User
from accounts.models.profiles import UserProfile
from . forms import SearchCustomerForm
from django.shortcuts import render, get_object_or_404, redirect

class PlanListView(ListView):
    model = Plan
    template_name = 'plan/list.html'
    context_object_name = 'plans'

class PlanDetailView(DetailView):
    model = Plan
    template_name = 'plan/detail.html'
    context_object_name = 'plan'

class PlanCreateView(CreateView):
    model = Plan
    template_name = 'plan/create.html'
    fields = ['name', 'price', 'default_month', 'description']

    def get_success_url(self):
        return reverse_lazy('plan:pages:list')

class PlanUpdateView(UpdateView):
    model = Plan
    template_name = 'plan/update.html'
    fields = ['name', 'price', 'default_month', 'description']

    def get_success_url(self):
        return reverse_lazy('plan:pages:list')

def plan_delete(request, pk):
    plan = get_object_or_404(Plan, pk=pk)
    plan.delete()
    return redirect('plan:pages:list')
    

def search_customer(request):
    context = {
        "form": SearchCustomerForm(),
    }
    if request.method == "POST":
        phone_number = request.POST.get("phone_number")
        if phone_number:
            try:
                user = User.objects.get(phone_number=phone_number, role='user')
                userprofile = UserProfile.objects.get(user=user)
                return redirect(f'/accounts/pages/userdetail/{userprofile.pk}/')
            except User.DoesNotExist:
                return redirect(f'/accounts/pages/user/create/?phone_number={phone_number}')

    return render(request, 'plan/search_customer.html', context)
