from django.urls import path
from . import views

urlpatterns = [
    path('', views.prebuilt_home, name='prebuilt_home'),              # Page showing prebuilt stores
    path('api/stores/', views.prebuilt_list_create, name='prebuilt_api'),  # API endpoint
    path('order/', views.order_prebuilt_store, name='order_prebuilt'),     # Form submission for orders
    path('order/success/', views.prebuilt_order_success, name='prebuilt_order_success'),

]
