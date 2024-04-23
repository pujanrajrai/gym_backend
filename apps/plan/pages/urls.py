from django.urls import path
from . import views
app_name = "pages"

urlpatterns = [
    path('list/', views.PlanListView.as_view(), name='list'),
    path('detail/<int:pk>/', views.PlanDetailView.as_view(), name='detail'),
    path('create/', views.PlanCreateView.as_view(), name='create'),
    path('<int:pk>/update/', views.PlanUpdateView.as_view(), name='update'),
    path('<int:pk>/delete/', views.plan_delete, name='delete'),
    path('search/user', views.search_customer, name='search_customer'),
    ]