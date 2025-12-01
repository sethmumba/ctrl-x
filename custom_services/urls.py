from django.urls import path
from . import views

urlpatterns = [
    path('services/', views.services_list, name='services_list'),
    path('order/create/<int:service_id>/', views.create_order, name='create_order'),
    path('order/create/', views.create_order, name='create_order_no_service'),
    path('my-orders/', views.my_orders, name='my_orders'),
    path('staff/orders/', views.staff_orders, name='staff_orders'),
]
