from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_page, name='home'),
    # urls.py
path('order/daily-order-status-json/', views.daily_order_status_json, name='daily_order_status_json')

]
