from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponseRedirect
from django.contrib import messages
from rental.models import Customer, Property, UnconfirmInvoice, CustomerProperty, Invoice
from .forms import CustomForm, IssueInvoiceForm
from django.http import HttpResponseRedirect


def generate_invoice_view(request):
    form = CustomForm()
    if request.method == "POST":
        form = CustomForm(request.POST)
        if form.is_valid():
            include_exclude = form.cleaned_data.get('type1')
            selection_type = form.cleaned_data.get('type2')
            single_select = form.cleaned_data.get('type4')
            multi_select = form.cleaned_data.get('type3')
            month = form.cleaned_data.get('month')
            # Handle property selection based on form inputs
            if include_exclude == "include":
                if selection_type == "all":
                    properties = Property.objects.all()
                elif selection_type == "single":
                    properties = Property.objects.filter(id=single_select)
                elif selection_type == "multiple":
                    properties = Property.objects.filter(id__in=multi_select)
            elif include_exclude == "exclude":
                if selection_type == "all":
                    properties = Property.objects.none()  # No properties selected
                elif selection_type == "single":
                    properties = Property.objects.exclude(id=single_select)
                elif selection_type == "multiple":
                    properties = Property.objects.exclude(id__in=multi_select)

            # Generate UnconfirmInvoice for selected properties
            for property in properties:
                customer_properties = CustomerProperty.objects.filter(
                    myproperty=property, is_terminated=False)
                for customer_property in customer_properties:
                    UnconfirmInvoice.objects.create(
                        customer=customer_property.customer,
                        myproperty=property,
                        month_name=month,  # You can set this dynamically as needed
                        property_rent=property.price_per_month,
                        total_electricity_unit=0,  # Set appropriate values
                        total_electricity_amount=0,  # Set appropriate values
                        total_water_unit=0,  # Set appropriate values
                        total_water_amount=0,  # Set appropriate values
                        total_garbage_amount=property.garbage_cost_per_month,
                        miscellaneous_amount=0,  # Set appropriate values
                        remarks="",
                    )
            return redirect('rental:invoice:unconfirm_invoice_list')
    context = {
        "form": form,
        "current": "generate_invoice"
    }
    return render(request, 'invoice/generate_invoice.html', context)


def unconfirm_invoice_list(request):
    invoices = UnconfirmInvoice.objects.all()
    context = {
        "invoices": invoices
    }
    return render(request, 'invoice/unconfirm_invoice_list.html', context)


def delete_unconfirm_invoice(request, pk):
    invoice = UnconfirmInvoice.objects.get(pk=pk)
    invoice.delete()
    messages.success(request, f'Unconfirm Invoice Deleted Successfully')
    return redirect('rental:invoice:unconfirm_invoice_list')


def issue_invoice(request, pk):
    obj = UnconfirmInvoice.objects.get(pk=pk)
    myproperty = obj.myproperty
    rent_amount = myproperty.price_per_month
    garbage_amount = myproperty.garbage_cost_per_month
    electricity_per_unit_price = myproperty.electricity_per_unit_price
    water_per_unit_price = myproperty.water_per_unit_price

    if request.method == "POST":
        form = IssueInvoiceForm(request.POST, instance=obj)
        if form.is_valid():
            if 'save' in request.POST:
                form.save()
                return HttpResponseRedirect(request.path_info)
            elif 'issue' in request.POST:
                # Create a new Invoice object
                Invoice.objects.create(
                    customer=obj.customer,
                    myproperty=obj.myproperty,
                    month_name=obj.month_name,
                    property_rent=obj.property_rent,
                    total_electricity_unit=obj.total_electricity_unit,
                    total_electricity_amount=obj.total_electricity_amount,
                    total_water_unit=obj.total_water_unit,
                    total_water_amount=obj.total_water_amount,
                    total_garbage_amount=obj.total_garbage_amount,
                    miscellaneous_amount=obj.miscellaneous_amount,
                    total_price=obj.total_price,
                    remarks=obj.remarks,
                    is_cancelled=0  # Assuming default value for is_cancelled
                )
                # Delete the unconfirmed invoice
                obj.delete()
                return redirect('rental:invoice:unconfirm_invoice_list')

    else:
        form = IssueInvoiceForm(instance=obj)

    context = {
        "form": form,
        "rent_amount": rent_amount,
        "garbage_amount": garbage_amount,
        "electricity_per_unit_price": electricity_per_unit_price,
        "water_per_unit_price": water_per_unit_price
    }
    return render(request, 'invoice/issue.html', context)


def invoice_list(request):
    invoices = Invoice.objects.all()
    context = {
        "invoices": invoices,
        "current": "invoice"
    }

    return render(request, 'invoice/list.html', context)


def invoice_details(request, pk):
    invoice = Invoice.objects.get(pk=pk)
    context = {
        "invoice": invoice
    }
    return render(request, 'invoice/details.html', context)


def cancel_invoice(request, pk):
    try:
        invoice = Invoice.objects.get(pk=pk)
        invoice.is_cancelled = True
        invoice.save()
    except Exception as e:
        messages.success(request, f'Error:{e}')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
