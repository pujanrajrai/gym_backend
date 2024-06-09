from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponseRedirect
from django.contrib import messages
from rental.models.customer import Customer, CustomerDocument
from .forms import CustomerForm, CustomerDocumentForm

from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from decorators import is_renta_user


@method_decorator(login_required(), name='dispatch')
@method_decorator(is_renta_user(['admin']), name='dispatch')
class CustomerListView(ListView):
    model = Customer
    template_name = 'customer/list.html'
    context_object_name = 'customers'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current'] = 'customer'
        return context



@method_decorator(login_required(), name='dispatch')
@method_decorator(is_renta_user(['admin']), name='dispatch')
class CustomerCreateView(CreateView):
    model = Customer
    form_class = CustomerForm
    template_name = 'customer/create.html'
    success_url = reverse_lazy('rental:customer:list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current'] = 'customer'
        return context



@method_decorator(login_required(), name='dispatch')
@method_decorator(is_renta_user(['admin']), name='dispatch')
class CustomerUpdateView(UpdateView):
    model = Customer
    form_class = CustomerForm
    template_name = 'customer/update.html'

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(
            self.request, 'Customer details updated successfully.')
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current'] = 'customer'
        return context

    def get_success_url(self):
        return reverse_lazy('rental:customer:details', kwargs={'pk': self.object.pk})



@login_required()
@is_renta_user(['admin'])
def active_inactive_toggle(request, pk):
    customer = Customer.objects.get(pk=pk)
    active_status = customer.is_active
    if active_status:
        customer.is_active = False
    else:
        customer.is_active = True
    customer.save()
    return redirect(request.META['HTTP_REFERER'])



@login_required()
@is_renta_user(['admin'])
def customer_details(request, pk):
    customer = Customer.objects.get(pk=pk)
    customer_document = CustomerDocument.objects.filter(customer=customer)
    context = {
        'current': 'customer',
        "customer": customer,
        "customer_documents": customer_document
    }
    return render(request, 'customer/details.html', context)



@method_decorator(login_required(), name='dispatch')
@method_decorator(is_renta_user(['admin']), name='dispatch')
class CustomerDocumentCreateView(CreateView):
    model = CustomerDocument
    form_class = CustomerDocumentForm
    template_name = 'customer/document_create.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['customer'] = self.kwargs['pk']
        return kwargs

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(
            self.request, 'Customer document created successfully.')
        return response

    def get_success_url(self):
        return reverse_lazy('rental:customer:details', kwargs={'pk': self.object.customer.pk})



@login_required()
@is_renta_user(['admin'])
def delete_document(request, pk):
    document = CustomerDocument.objects.get(pk=pk)
    document.delete()
    return redirect(request.META['HTTP_REFERER'])
