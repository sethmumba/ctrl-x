from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_home, name='dashboard-home'),
    path('order/<int:order_id>/', views.order_detail, name='order-detail'),
    path("support/", views.support, name="support"),

]
