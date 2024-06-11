from django.urls import path, include
from . import views
app_name = "invoice"

urlpatterns = [
    path(
        'generate_invoice/', views.generate_invoice_view, name='generate_invoice'
    ),
    path(
        'unconfirm/list/', views.unconfirm_invoice_list, name='unconfirm_invoice_list'
    ),
    path(
        'delete/unconfirm/invoice/<str:pk>', views.delete_unconfirm_invoice, name='delete_unconfirm_invoice'
    ),
    path(
        'issue/invoice/<str:pk>/', views.issue_invoice, name="issue_invoice"
    ),
    path(
        'list/', views.invoice_list, name='invoice_list'
    ),
    path(
        'details/<str:pk>', views.invoice_details, name='invoice_details'
    ),
    path(
        'cancel/invoice/<str:pk>', views.cancel_invoice, name="cancel_invoice"
    ),
    path(
        'invoice/print/plan/<str:pk>/', views.invoice_print, name="invoice_print"
    ),
]
