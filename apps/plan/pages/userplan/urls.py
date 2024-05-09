from django.urls import path
from . import views
app_name = "userplan"

urlpatterns = [
    path(
        'search/user', views.search_customer, name='search_customer'
    ),
    path(
        'search/user/api/', views.SearchCustomerAPIView.as_view(), name='search_customer_api'
    ),
    path(
        'create/user/', views.CreateUser.as_view(), name='create_user'
    ),
    path(
        'create/user/plan/<str:pk>/', views.usercreate_plan, name="create_user_plan"
    ),
    path(
        'userplan/delete/<str:pk>/', views.delete_user_plan, name="delete_user_plan"
    ),
    path(
        'issue/plan/<str:pk>/', views.issue_userplan, name="issue_plan"
    ),
    path(
        'current/plan/<str:pk>/', views.current_plan, name="current_plan"
    ),
]
