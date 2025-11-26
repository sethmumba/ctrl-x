from django.shortcuts import render
from django.utils import timezone
from orders.models import Order
from django.http import JsonResponse
from django.utils import timezone

def home_page(request):
    today = timezone.now().date()
    daily_orders_count = Order.objects.filter(created_at__date=today).count()
    daily_limit = 6

    return render(request, 'home/home.html', {
        'daily_orders_count': daily_orders_count,
        'daily_limit': daily_limit,
    })


# views.py
def daily_order_status_json(request):
    today = timezone.now().date()
    daily_orders_count = Order.objects.filter(created_at__date=today).count()
    return JsonResponse({'daily_orders_count': daily_orders_count})
