from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponseRedirect
from django.contrib import messages
from rental.models.customer import CustomerDocument
from .forms import CustomerDocumentForm

class CustomerDocumentListView(ListView):
    model = CustomerDocument
    template_name = 'customer_file/list.html'
    context_object_name = 'documents'

    def get_queryset(self):
        customer_id = self.kwargs['customer_id']
        return CustomerDocument.objects.filter(customer__id=customer_id)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['customer_id'] = self.kwargs['customer_id']
        context['current'] = 'customer'
        return context

class CustomerDocumentDetailView(DetailView):
    model = CustomerDocument
    template_name = 'document_detail.html'
    context_object_name = 'document'

class CustomerDocumentCreateView(CreateView):
    model = CustomerDocument
    form_class = CustomerDocumentForm
    template_name = 'document_form.html'
    success_url = reverse_lazy('document_list')

class CustomerDocumentUpdateView(UpdateView):
    model = CustomerDocument
    form_class = CustomerDocumentForm
    template_name = 'document_form.html'
    success_url = reverse_lazy('document_list')

def customer_document_delete(request, pk):
    document = get_object_or_404(CustomerDocument, pk=pk)
    if request.method == 'POST':
        document.delete()
        messages.success(request, 'Document deleted successfully.')
        return redirect('document_list')
    return render(request, 'document_confirm_delete.html', {'document': document})
