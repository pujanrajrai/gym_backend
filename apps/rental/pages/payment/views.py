from django.shortcuts import get_object_or_404
from rental.models import Payment, Customer, ledger_last_balance
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from .forms import PaymentForm
from django.http import JsonResponse

from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from decorators import is_renta_user



@login_required()
@is_renta_user(['admin'])
def payment_list(request):
    payments = Payment.objects.all()
    context = {
        "payments": payments,
        "current": "payment"

    }
    return render(request, 'payments/list.html', context)



@login_required()
@is_renta_user(['admin'])
def payment_create(request):
    if request.method == "POST":
        form = PaymentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('rental:payment:list')
    else:
        form = PaymentForm()
    context = {
        "form": form,
        "current": "payment"
    }
    return render(request, 'payments/create.html', context)



@login_required()
@is_renta_user(['admin'])
def due_amount(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    customer_balance = ledger_last_balance(customer)
    return JsonResponse({"balance": customer_balance})
