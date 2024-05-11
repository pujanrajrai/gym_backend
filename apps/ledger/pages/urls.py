from django.urls import path, include
from . import views
app_name = "pages"

urlpatterns = [
    path('list/', views.list_ledger, name='list'),
    path('list_datatable/',
         views.LedgerListView.as_view(), name="ledger_datatable"),
    path('create/', views.create_ledger, name='create'),
]
