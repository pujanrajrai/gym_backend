from django.urls import path, include
from . import views
app_name = "pages"

urlpatterns = [
    path('list/', views.list_ledger, name='list'),
    path('list_datatable/',
         views.LedgerListView.as_view(), name="ledger_datatable"),
    path('create/', views.create_ledger, name='create'),
    path('export/', views.export_ledger_to_excel, name='export_ledger_to_excel'),
    path('salary/', include('ledger.pages.salary.urls')),
    path('expesnses/', include('ledger.pages.expenses.urls')),

]
