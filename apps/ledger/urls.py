from django.urls import path, include
from . import views
app_name = "ledger"

urlpatterns = [
    path('pages/', include('ledger.pages.urls')),
]
