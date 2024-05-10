from django.urls import path
from plan.pages.userplan import views
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
        'invoice/print/plan/<str:pk>/', views.invoice_print, name="invoice_print_plan"
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
    path(
        'previous/plan/<str:pk>/', views.previous_plan, name="previous_plan"
    ),
    path(
        'plan/details/<str:pk>/', views.plan_details, name="plan_details"
    ),
    path(
        'print/invoice/<str:pk>/', views.print_invoice, name="print_invoice"
    ),
]
