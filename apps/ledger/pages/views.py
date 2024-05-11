# import pytz
from django.http import HttpResponse
# import openpyxl
from django.views.generic import View
from decimal import Decimal
from django.http import HttpResponseRedirect
from ledger.models import *
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib import messages
from .forms import *
from django.contrib.messages.views import SuccessMessageMixin
from django_serverside_datatable.views import ServerSideDatatableView
from datetime import datetime
from accounts.models.users import User


class LedgerListView(ServerSideDatatableView):
    def get_queryset(self):
        user = self.request.GET.get('user')
        from_date_str = self.request.GET.get('from_date')
        to_date_str = self.request.GET.get('to_date')

        if from_date_str and from_date_str != 'None':
            # Use '%b' for abbreviated month
            from_date = datetime.strptime(from_date_str, '%b %d, %Y')
        else:
            from_date = None

        if to_date_str and to_date_str != 'None':
            # Use '%b' for abbreviated month
            to_date = datetime.strptime(to_date_str, '%b %d, %Y')
        else:
            to_date = None
        queryset = Ledger.objects.all()
        if user:
            queryset = queryset.filter(user__phone_number=user)
        if from_date:
            queryset = queryset.filter(created_date__gte=from_date)
        if to_date:
            queryset = queryset.filter(created_date__lte=to_date)
        return queryset

    columns = [
        'created_date',
        'user__email',
        'particular',
        '_type',
        'amount',
        'balance',
        'remarks',
        'entry_type',
        'leaserid',
    ]


def list_ledger(request):
    context = {"current": "ledger"}
    form = LedgerFilterForm(request.GET)
    if form.is_valid():
        context["user"] = request.GET.get('user')
        context["from_date"] = form.cleaned_data['from_date']
        context["to_date"] = form.cleaned_data['to_date']
    else:
        print(form.error)
    context["form"] = form
    return render(request, 'ledger/list.html', context)


def create_ledger(request):
    form = LedgerForm()
    context = {'form': form, "current": "ledger"}

    if request.method == 'POST':
        form = LedgerForm(request.POST)

        if form.is_valid():
            # Get user based on phone number
            try:
                user = User.objects.get(
                    phone_number=request.POST['user'])
            except User.DoesNotExist:
                messages.error(request, 'User not found.')
                context['form'] = form
                return render(request, 'ledger/create.html', context)

            last_balance = ledger_last_balance(user)

            # Debit ledger entry
            if request.POST['_type'] == 'Debit':
                new_balance = last_balance - Decimal(request.POST['amount'])
            else:
                new_balance = last_balance + Decimal(request.POST['amount'])

            myledger = Ledger.objects.create(
                user=user,
                _type=request.POST['_type'],
                particular=request.POST['particular'],
                amount=request.POST['amount'],
                remarks=request.POST['remarks'],
                entry_type=request.POST['entry_type'],
                balance=new_balance
            )

            messages.success(request, 'Ledger created successfully.')
            return redirect('ledger:pages:list')
        else:
            messages.error(request, 'Ledger creation failed.')
            context['form'] = form

    return render(request, 'ledger/create.html', context)
