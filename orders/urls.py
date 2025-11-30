from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_store_order, name='create-order'),
   # path('check-domain-api/', views.check_domain_api, name='check-domain-api'),
    path('paypal-complete/', views.paypal_complete, name='paypal-complete'),
    path('privacy-policy/', views.privacy_policy, name='privacy-policy'),
    path('terms-of-service/', views.terms_of_service, name='terms-of-service'),
    path('refund-policy/', views.refund_policy, name='refund-policy'),
    path('learn-more/', views.learn_more, name='learn-more'),
    path("daily-order-status/", views.daily_order_status, name="daily_order_status"),
]
