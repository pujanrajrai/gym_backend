from django.urls import path, include
from . import views
app_name = "payment"

urlpatterns = [
    path(
        'list/', views.payment_list, name='list'
    ),
    path(
        'create/', views.payment_create, name='create'
    ),


]
