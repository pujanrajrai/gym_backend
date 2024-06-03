from rental.models import Payment, Customer
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from .forms import PaymentForm


def payment_list(request):
    payments = Payment.objects.all()
    context = {
        "payments": payments,
        "current": "payment"

    }
    return render(request, 'payments/list.html', context)


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
