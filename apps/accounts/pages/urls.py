from django.urls import path, include
from . import views
app_name = "pages"

urlpatterns = [
    path('user/list', views.UserListView.as_view(), name="user_list"),
    path('admin/create', views.CreateAdmin.as_view(), name="admin_create"),
    path('staff/create', views.CreateStaff.as_view(), name="staff_create"),
    path('user/create', views.CreateUser.as_view(), name="user_create"),
    path('<int:id>/user/block', views.block_user, name="block_user"),
    path('<int:id>/user/unblock', views.unblock_user, name="unblock_user"),
    path('profileredirect/<int:id>/',views.profile_redirect, name="profile_redirect"),
    path('staffdetail/<str:pk>/',views.StaffProfileDetailView.as_view(), name="staff_detail"),
    path('userdetail/<str:pk>/',views.UserProfileDetailView.as_view(), name="user_detail"),
    path('staff/<str:pk>/update/', views.StaffProfileUpdateView.as_view(),name='staff_profile_update'),
    path('user/<str:pk>/update/', views.UserProfileUpdateView.as_view(),name='user_profile_update'),
]
