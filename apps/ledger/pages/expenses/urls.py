from django.urls import path, include
from . import views
app_name = "expenses"

urlpatterns = [
    path('list/', views.list_expenses, name='list'),
    path('list_datatable/',
         views.ExpensesListView.as_view(), name="expenses_datatable"),
    path('create/', views.create_expenses, name='create'),
]
