from django.shortcuts import render
from django.http import JsonResponse
from django.core.files.storage import default_storage
from django.views.decorators.csrf import csrf_exempt
from .models import Order
from .utils.dns_check import shopify_subdomain_available
from django.contrib.auth.decorators import login_required
from django.conf import settings
import json

@login_required
def create_store_order(request):
    context = {
        "paypal_client_id": settings.PAYPAL_CLIENT_ID
    }
    return render(request, 'orders/create_order.html', context)

#check dns
@login_required
def check_domain_api(request):
    store_name = request.GET.get("store_name", "")
    if not store_name:
        return JsonResponse({"available": False, "error": "No store name provided"})

    available = shopify_subdomain_available(store_name)
    return JsonResponse({"available": available})


#paypal payment completion + order creation
@csrf_exempt
@login_required
def paypal_complete(request):
    if request.method != "POST":
        return JsonResponse({"status": "invalid_method"}, status=400)

    data = json.loads(request.body)

    paypal_order_id = data.get("paypal_order_id")
    form_data = data.get("form_data")

    if not paypal_order_id:
        return JsonResponse({"status": "missing_paypal_id"}, status=400)

    # Save order
    order = Order.objects.create(
        user=request.user,
        is_paid=True,
        paypal_order_id=paypal_order_id,
        store_name=form_data["store_name"],
        niche=form_data["niche"],
        supplier=form_data["supplier"],
        theme=form_data["theme"],
        color_palette=form_data["color_palette"],
        desired_profit_margin=form_data["profit_margin"],
        markets=form_data["markets"],
    )

    # Logo upload (base64 or filename)
    logo_filename = form_data.get("logo_filename")
    if logo_filename:
        order.logo = logo_filename
        order.save()

    return JsonResponse({"status": "success", "order_id": order.id})
