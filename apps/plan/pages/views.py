# In your app's views.py file

from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from plan.models import Plan

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
        return reverse_lazy('accounts:pages:list')

def plan_delete(request, pk):
    plan = get_object_or_404(Plan, pk=pk)
    plan.delete()
    return redirect('plan_list')
    
