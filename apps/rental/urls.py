from django.urls import path, include
from . import views
app_name = "rental"

urlpatterns = [
    path('customer/', include('rental.pages.customer.urls')),
    path('customer/file', include('rental.pages.customer_file.urls')),
    path('property/', include('rental.pages.property.urls')),
]
