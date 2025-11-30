from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Order
from .utils.dns_check import shopify_subdomain_available
from django.contrib.auth.decorators import login_required
from django.conf import settings
import json
from django.contrib.auth.models import User
from django.utils import timezone


@login_required
def create_store_order(request):
    context = {
        "paypal_client_id": settings.PAYPAL_CLIENT_ID
    }
    return render(request, 'orders/create_order.html', context)




# PayPal payment completion + order creation

@login_required
@csrf_exempt
def paypal_complete(request):
    if request.method != "POST":
        return JsonResponse({"status": "invalid_method"}, status=400)

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"status": "invalid_json"}, status=400)

    paypal_order_id = data.get("paypal_order_id")
    form_data = data.get("form_data")

    if not paypal_order_id:
        return JsonResponse({"status": "missing_paypal_id"}, status=400)

    if not form_data:
        return JsonResponse({"status": "missing_form_data"}, status=400)

    required_fields = ["store_name", "niche", "supplier", "theme"]

    for field in required_fields:
        if field not in form_data or not form_data[field]:
            return JsonResponse({
                "status": "missing_field",
                "error": f"{field} is required"
            }, status=400)

    # DAILY LIMIT
    today = timezone.now().date()
    orders_today = Order.objects.filter(created_at__date=today).count()

    if orders_today >= 6:
        return JsonResponse({
            "status": "daily_limit_reached",
            "message": "Only 6 orders per day allowed."
        }, status=400)

    try:
        order = Order.objects.create(
            user=request.user,    # <-- your JS must send this
            is_paid=True,
            paypal_order_id=paypal_order_id,
            store_name=form_data["store_name"],
            niche=form_data["niche"],
            supplier=form_data["supplier"],
            theme=form_data["theme"],
            full_name=form_data.get("full_name", ""),
            country=form_data.get("country", ""),
            phone=form_data.get("phone", ""),
            desired_profit_margin=form_data.get("profit_margin", ""),
            markets=form_data.get("markets", []),
        )

        logo_filename = form_data.get("logo_filename")
        if logo_filename:
            order.logo = logo_filename
            order.save()

        return JsonResponse({"status": "success", "order_id": order.id})

    except Exception as e:
        print("ORDER CREATION ERROR:", e)
        return JsonResponse({"status": "error", "detail": str(e)}, status=500)




def learn_more(request):
    return render(request, 'orders/learn-more.html')

@login_required
def daily_order_status(request):
    today = timezone.now().date()
    orders_today = Order.objects.filter(created_at__date=today).count()
    remaining = max(6 - orders_today, 0)
    return JsonResponse({
        "remaining": remaining,
        "limit_reached": remaining == 0
    })