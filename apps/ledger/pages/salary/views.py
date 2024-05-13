# import pytz
from urllib.parse import urlencode
from django.urls import reverse
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
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from decorators import has_roles



@method_decorator(login_required(), name='dispatch')
@method_decorator(has_roles(['admin']), name='dispatch')
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
        queryset = Ledger.objects.filter(entry_type='Salary')
        if user:
            queryset = queryset.filter(user__phone_number=user)
        if from_date:
            queryset = queryset.filter(created_date__gte=from_date)
        if to_date:
            queryset = queryset.filter(created_date__lte=to_date)
        return queryset

    columns = [
        'created_date',
        'user__phone_number',
        'particular',
        '_type',
        'amount',
        'balance',
        'remarks',
        'entry_type',
        'leaserid',
        'company_balance'
    ]



@login_required()
@has_roles(['admin'])
def list_ledger(request):
    context = {"current": "salary"}
    form = LedgerFilterForm(request.GET)
    if form.is_valid():
        context["user"] = request.GET.get('user')
        context["from_date"] = form.cleaned_data['from_date']
        context["to_date"] = form.cleaned_data['to_date']
    else:
        print(form.error)
    context["form"] = form
    return render(request, 'salary/list.html', context)



@login_required()
@has_roles(['admin'])
def create_ledger(request):
    form = LedgerForm()
    context = {'form': form, "current": "salary"}

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
                return render(request, 'salary/create.html', context)

            last_balance = ledger_last_balance(user)

            new_balance = last_balance - Decimal(request.POST['amount'])
            try:
                company_balance = Ledger.objects.latest(
                    'created_date').company_balance-Decimal(request.POST['amount'])
            except:
                company_balance = -Decimal(request.POST['amount'])

            myledger = Ledger.objects.create(
                user=user,
                _type='Credit',
                particular='Employee Salary',
                amount=request.POST['amount'],
                remarks='Salary',
                entry_type='Salary',
                balance=new_balance,
                company_balance=company_balance,
            )
            messages.success(request, 'Ledger created successfully.')
            query_params = {
                'user': '',  # Add your user parameter here
                'from_date': '',  # Add your from_date parameter here
                'to_date': '',  # Add your to_date parameter here
            }
            url = reverse('ledger:pages:salary:list') + \
                '?' + urlencode(query_params)
            return HttpResponseRedirect(url)
        else:
            messages.error(request, 'Ledger creation failed.')
            context['form'] = form

    return render(request, 'ledger/create.html', context)
