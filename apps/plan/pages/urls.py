from django.urls import path, include
from . import views
app_name = "pages"

urlpatterns = [
    path('list/', views.PlanListView.as_view(), name='list'),
    path('create/', views.PlanCreateView.as_view(), name='create'),
    path('<int:pk>/update/', views.PlanUpdateView.as_view(), name='update'),
    path('<int:pk>/delete/', views.plan_delete, name='delete'),
    path('userplan/', include('plan.pages.userplan.urls'))
]
