from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.staff_dashboard, name='staff-dashboard'),
    path('order/<int:order_id>/', views.staff_order_detail, name='staff-order-detail'),
    path('order/<int:order_id>/update-progress/', views.update_order_progress, name='update-order-progress'),
]
