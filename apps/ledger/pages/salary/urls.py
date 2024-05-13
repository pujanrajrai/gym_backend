from django.urls import path, include
from . import views
app_name = "salary"

urlpatterns = [
    path('list/', views.list_salary, name='list'),
    path('list_datatable/',
         views.SalaryListView.as_view(), name="salary_datatable"),
    path('create/', views.create_salary, name='create'),
]
