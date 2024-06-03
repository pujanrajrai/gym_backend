from django.urls import path
from . import views
app_name = "customer_property"

urlpatterns = [
    path(
        'list/', views.customer_property_list, name='list'
    ),
    path(
        'create/', views.customer_property_create, name='create'
    ),
    path(
        'terminate_contract/<int:pk>', views.terminated_contract, name='terminate_contract'
    ),
]
