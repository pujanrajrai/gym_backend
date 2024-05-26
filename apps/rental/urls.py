from django.urls import path, include
from . import views
app_name = "rental"

urlpatterns = [
    path('customer/', include('rental.pages.customer.urls')),
]
