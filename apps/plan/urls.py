from django.urls import path, include

app_name = "plan"

urlpatterns = [
    path('pages/', include('plan.pages.urls'))

]
