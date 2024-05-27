from django.urls import path, include
from . import views
app_name = "customer_file"

urlpatterns = [
    path('<int:customer_id>/documents/', views.CustomerDocumentListView.as_view(), name='list'),
    path('documents/<int:pk>/', views.CustomerDocumentDetailView.as_view(), name='detail'),
    path('documents/create/', views.CustomerDocumentCreateView.as_view(), name='create'),
    path('documents/<int:pk>/update/', views.CustomerDocumentUpdateView.as_view(), name='update'),
    path('documents/<int:pk>/delete/', views.customer_document_delete, name='delete'),
]