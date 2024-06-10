# import pytz
from rest_framework.response import Response
from urllib.parse import urlencode
from django.urls import reverse
from django.http import HttpResponse
# import openpyxl
from django.views.generic import View
from django.http import HttpResponseRedirect
from rental.models import *
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib import messages
from .forms import *
from django.contrib.messages.views import SuccessMessageMixin
from django_serverside_datatable.views import ServerSideDatatableView
from datetime import datetime
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from decorators import is_renta_user
from openpyxl import Workbook
from rest_framework import serializers
from rest_framework.views import APIView


from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from decorators import is_renta_user



class LedgerSerializer(serializers.ModelSerializer):
    customer = serializers.SerializerMethodField()

    def get_customer(self, obj):
        mycustomer = obj.customer.name
        return mycustomer

    class Meta:
        model = Ledger
        fields = [
            'created_date',
            'customer',
            'particular',
            '_type',
            'amount',
            'balance',
            'remarks',
            'entry_type',
            'leaserid',
            'company_balance'
        ]


class LedgerListView(APIView):

    def get(self, request, *args, **kwargs):
        draw = int(request.GET.get('draw', 1))
        start = int(request.GET.get('start', 0))
        length = int(request.GET.get('length', 10))
        search_value = request.GET.get('search[value]', '')

        order_column_index = request.GET.get('order[0][column]', 0)
        order_column = request.GET.get(
            f'columns[{order_column_index}][data]', 'created_date')
        order_dir = request.GET.get('order[0][dir]', 'asc')

        customer = request.GET.get('customer')
        from_date_str = request.GET.get('from_date')
        to_date_str = request.GET.get('to_date')

        if from_date_str and from_date_str != 'None':
            from_date = datetime.strptime(from_date_str, '%b %d, %Y')
        else:
            from_date = None

        if to_date_str and to_date_str != 'None':
            to_date = datetime.strptime(to_date_str, '%b %d, %Y')
        else:
            to_date = None

        queryset = Ledger.objects.all()

        if customer:
            queryset = queryset.filter(customer=customer)
        if from_date:
            queryset = queryset.filter(created_date__gte=from_date)
        if to_date:
            queryset = queryset.filter(created_date__lte=to_date)

        if search_value:
            queryset = queryset.filter(
                Q(customer__icontains=search_value) |
                Q(particular__icontains=search_value) |
                Q(_type__icontains=search_value) |
                Q(remarks__icontains=search_value)
            )
        total_records = queryset.count()

        if order_dir == 'desc':
            order_column = f'-{order_column}'

        queryset = queryset.order_by(order_column)[start:start + length]

        serializer = LedgerSerializer(queryset, many=True)

        response = {
            'draw': draw,
            'recordsTotal': total_records,
            'recordsFiltered': total_records,  # Adjust this if you add filters
            'data': serializer.data
        }

        return Response(response)


@login_required()
@is_renta_user(['admin'])
def list_ledger(request):
    context = {"current": "rental_ledger"}
    form = LedgerFilterForm(request.GET)
    if form.is_valid():
        context["customer"] = request.GET.get('customer')
        context["from_date"] = form.cleaned_data['from_date']
        context["to_date"] = form.cleaned_data['to_date']
    else:
        print(form.errors)
    context["form"] = form
    return render(request, 'rental_ledger/list.html', context)


@login_required()
@is_renta_user(['admin'])
def create_ledger(request):
    form = LedgerForm()
    context = {'form': form, "current": "ledger"}

    if request.method == 'POST':
        form = LedgerForm(request.POST)

        if form.is_valid():
            # Get customer based on phone number
            try:
                customer = Customer.objects.get(
                    pk=request.POST['customer'])
            except Customer.DoesNotExist:
                messages.error(request, 'Customer not found.')
                context['form'] = form
                return render(request, 'ledger/create.html', context)

            last_balance = ledger_last_balance(customer)

            # Debit ledger entry
            if request.POST['_type'] == 'Debit':
                new_balance = last_balance - float(request.POST['amount'])
                try:
                    company_balance = Ledger.objects.latest(
                        'created_date').company_balance-float(request.POST['amount'])
                except:
                    company_balance = -float(request.POST['amount'])
            else:
                new_balance = last_balance + float(request.POST['amount'])
                try:
                    company_balance = Ledger.objects.latest(
                        'created_date').company_balance+float(request.POST['amount'])
                except:
                    company_balance = float(request.POST['amount'])

            myledger = Ledger.objects.create(
                customer=customer,
                _type=request.POST['_type'],
                particular=request.POST['particular'],
                amount=request.POST['amount'],
                remarks=request.POST['remarks'],
                entry_type=request.POST['entry_type'],
                balance=new_balance,
                company_balance=company_balance,
            )

            messages.success(request, 'Ledger created successfully.')
            query_params = {
                'customer': '',  # Add your customer parameter here
                'from_date': '',  # Add your from_date parameter here
                'to_date': '',  # Add your to_date parameter here
            }
            url = reverse('rental:ledger:list') + '?' + urlencode(query_params)
            return HttpResponseRedirect(url)
        else:
            messages.error(request, 'Ledger creation failed.')
            context['form'] = form

    return render(request, 'rental_ledger/create.html', context)


@login_required
@is_renta_user(['admin'])
def export_ledger_to_excel(request):
    customer = request.GET.get('customer')
    from_date_str = request.GET.get('from_date')
    to_date_str = request.GET.get('to_date')

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
    if customer:
        queryset = queryset.filter(customer=customer)
    if from_date:
        queryset = queryset.filter(created_date__gte=from_date)
    if to_date:
        queryset = queryset.filter(created_date__lte=to_date)

    workbook = Workbook()
    worksheet = workbook.active

    # Add column headers
    headers = [
        'created_date',
        'Customer',
        'Particular',
        'Debit',
        'Credit',
        'Balance',
        'Company Balance',
        'Remarks',
        'Entry Type',
        'Ledger ID',
    ]
    worksheet.append(headers)

    # Add data rows
    for item in queryset:
        debit = item.amount if item._type == 'Debit' else None
        credit = item.amount if item._type == 'Credit' else None

        row_data = [
            item.created_date.strftime(
                '%Y-%m-%d %H:%M:%S') if item.created_date else None,
            item.customer.phone_number,
            item.particular,
            debit,
            credit,
            item.balance,
            item.company_balance,
            item.remarks,
            item.entry_type,
            item.leaserid,

        ]
        row_data = [str(value) if isinstance(value, datetime)
                    else value for value in row_data]
        worksheet.append(row_data)

    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=ledger_export.xlsx'
    # messages.success(request, 'Ledger exported successfully.')
    workbook.save(response)

    return response
