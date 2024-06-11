from datetime import date, timedelta, datetime
from django.db.models import Sum
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponseRedirect
from django.contrib import messages
from rental.models.customer import Customer, CustomerDocument
from rental.models import Invoice, Payment
from .forms import CustomerForm, CustomerDocumentForm, DateRangeForm
from django.db.models import Sum, Q

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


# @login_required()
# @is_renta_user(['admin'])


def dashboard_report(request):
    form = DateRangeForm(request.GET or None)
    context = {}

    if form.is_valid():
        date_range = form.cleaned_data.get('date_range')
        from_date = form.cleaned_data.get('from_date')
        to_date = form.cleaned_data.get('to_date')
        customer_id = form.cleaned_data.get('customer')
        context["customer"] = customer_id
        context["from_date"] = from_date
        context["to_date"] = to_date
        context["date_range"] = date_range

        # Filter data based on company if selected
        if customer_id and customer_id != 'All':
            customer_filter = Q(customer=customer_id)
        else:
            customer_filter = Q()

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

        # Calculate total invoice
        total_invoice = Invoice.objects.filter(customer_filter).filter(
            date_filter).aggregate(total_sum=Sum('total_price'))['total_sum'] or 0

        # Calculate total payment
        total_payment = Payment.objects.filter(customer_filter).filter(date_filter).filter(
            is_cancelled=False).aggregate(total_sum=Sum('amount'))['total_sum'] or 0

    else:
        # If form is not valid, set totals to None
        total_invoice = None
        total_payment = None

    context["total_invoice"] = total_invoice
    context["total_payment"] = total_payment
    context["current"] = "dashboard_report"
    context["form"] = form

    return render(request, 'dashboard_rental.html', context)
