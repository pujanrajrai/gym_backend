from django.shortcuts import render, get_object_or_404, redirect
from rental.models import CustomerProperty
from .forms import CustomerPropertyForms, CustomerPropertyUpdateForms
from django.contrib import messages
from django.http import HttpResponseRedirect

from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from decorators import is_renta_user




@login_required()
@is_renta_user(['admin'])
def customer_property_create(request):
    form = CustomerPropertyForms()
    if request.method == 'POST':
        form = CustomerPropertyForms(request.POST)
        if form.is_valid():
            try:
                form.save()
            except Exception as e:
                messages.success(request, f'ERROR:{e}')
                return HttpResponseRedirect(request.path_info)
            return redirect('rental:customer_property:list')
    context = {
        "form": form,
        "current": "customer_property"

    }
    return render(request, 'customer_property/create.html', context)




@login_required()
@is_renta_user(['admin'])
def customer_property_list(request):
    customer_properies = CustomerProperty.objects.all()
    context = {
        "customer_properties": customer_properies,
        "current": "customer_property"
    }
    return render(request, 'customer_property/list.html', context)




@login_required()
@is_renta_user(['admin'])
def terminated_contract(request, pk):
    customer_property = CustomerProperty.objects.get(pk=pk)
    customer_property.is_terminated = True
    customer_property.save()
    messages.success(request, f'Contract Terminated Successfully')
    return redirect('rental:customer_property:list')
