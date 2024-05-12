# In your app's views.py file

from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from plan.models import Plan
from accounts.models.users import User
from accounts.models.profiles import UserProfile
from . forms import SearchCustomerForm,CreatePlanForm
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from decorators import has_roles




@method_decorator(login_required(), name='dispatch')
@method_decorator(has_roles(['admin','staff']), name='dispatch')
class PlanListView(ListView):
    model = Plan
    template_name = 'plan/list.html'
    context_object_name = 'plans'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current'] = 'plans'
        return context


@method_decorator(login_required(), name='dispatch')
@method_decorator(has_roles(['admin']), name='dispatch')
class PlanCreateView(CreateView):
    model = Plan
    form_class=CreatePlanForm
    sucess_message='Plan Created Sucessfully'
    template_name = 'plan/create.html'

    def get_success_url(self):
        return reverse_lazy('plan:pages:list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current'] = 'plans'
        return context



@method_decorator(login_required(), name='dispatch')
@method_decorator(has_roles(['admin']), name='dispatch')
class PlanUpdateView(UpdateView):
    model = Plan
    form_class=CreatePlanForm
    sucess_message='Plan Updated Sucessfully'
    template_name = 'plan/update.html'

    def get_success_url(self):
        return reverse_lazy('plan:pages:list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current'] = 'plans'
        return context

@login_required()
@has_roles(['admin'])
def plan_delete(request, pk):
    plan = get_object_or_404(Plan, pk=pk)
    plan.delete()
    return redirect('plan:pages:list')
