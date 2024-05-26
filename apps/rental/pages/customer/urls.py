from django.urls import path, include
from . import views
app_name = "customer"

urlpatterns = [
    path('customers/', views.CustomerListView.as_view(), name='list'),
    path('customers/<int:pk>/', views.CustomerDetailView.as_view(), name='detail'),
    path('customers/create/', views.CustomerCreateView.as_view(), name='create'),
    path('customers/<int:pk>/update/', views.CustomerUpdateView.as_view(), name='update'),
    path('customers/<int:pk>/delete/', views.customer_delete, name='delete'),
]