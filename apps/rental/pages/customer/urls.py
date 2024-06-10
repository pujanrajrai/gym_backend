from django.urls import path, include
from . import views
app_name = "customer"

urlpatterns = [
    path(
        'customers/', views.CustomerListView.as_view(), name='list'
    ),
    path(
        'customers/create/', views.CustomerCreateView.as_view(), name='create'
    ),
    path(
        'customers/<int:pk>/update/', views.CustomerUpdateView.as_view(), name='update'
    ),
    path(
        'customer/active/status/toggle/<str:pk>', views.active_inactive_toggle, name="customer_active_status_toggle"
    ),
    path(
        'details/<str:pk>/', views.customer_details, name="details"
    ),
    path(
        'document/create/<str:pk>/', views.CustomerDocumentCreateView.as_view(), name="document_create"
    ),
    path(
        'delete/document/<str:pk>/', views.delete_document, name="delete_document"
    ),
    path('dashboard/report/', views.dashboard_report,
         name='dashboard_report'),

]
