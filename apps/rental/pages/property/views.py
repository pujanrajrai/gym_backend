from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, CreateView, UpdateView, DetailView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from rental.models.myproperty import Property
from .forms import PropertyForm

class PropertyListView(ListView):
    model = Property
    template_name = 'property/list.html'
    context_object_name = 'properties'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current'] = 'property'
        return context

class PropertyCreateView(CreateView):
    model = Property
    form_class = PropertyForm
    template_name = 'property/create.html'
    success_url = reverse_lazy('rental:property:list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current'] = 'property'
        return context

class PropertyUpdateView(UpdateView):
    model = Property
    form_class = PropertyForm
    template_name = 'property/update.html'
    success_url = reverse_lazy('rental:property:list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current'] = 'property'
        return context

# class PropertyDetailView(DetailView):
#     model = Property
#     template_name = 'property_detail.html'
#     context_object_name = 'property'

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['current'] = 'property'
#         return context

# @login_required
# def property_delete(request, pk):
#     property = get_object_or_404(Property, pk=pk)
#     if request.method == 'POST':
#         property.delete()
#         return redirect('property_list')
#     return render(request, 'property_confirm_delete.html', {'property': property})
