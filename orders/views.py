from django.shortcuts import render
from django.http import JsonResponse
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


# Check DNS / domain availability
@login_required
def check_domain_api(request):
    store_name = request.GET.get("store_name", "")
    if not store_name:
        return JsonResponse({"available": False, "error": "No store name provided"})

    available = shopify_subdomain_available(store_name)
    return JsonResponse({"available": available})


# PayPal payment completion + order creation
@csrf_exempt
@login_required
def paypal_complete(request):
    if request.method != "POST":
        return JsonResponse({"status": "invalid_method"}, status=400)

    # Parse JSON
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"status": "invalid_json"}, status=400)

    paypal_order_id = data.get("paypal_order_id")
    form_data = data.get("form_data")

    # Missing PayPal ID
    if not paypal_order_id:
        return JsonResponse({"status": "missing_paypal_id"}, status=400)

    # Missing form data entire block
    if not form_data:
        return JsonResponse({"status": "missing_form_data"}, status=400)

    # Validate required fields
    required_fields = ["store_name", "niche", "supplier", "theme"]

    for field in required_fields:
        if field not in form_data or not form_data[field]:
            return JsonResponse({
                "status": "missing_field",
                "error": f"{field} is required but missing"
            }, status=400)

    # Create order safely
    try:
        order = Order.objects.create(
            user=request.user,
            is_paid=True,
            paypal_order_id=paypal_order_id,

            # Required fields (validated above)
            store_name=form_data["store_name"],
            niche=form_data["niche"],
            supplier=form_data["supplier"],
            theme=form_data["theme"],

            # Optional fields
            full_name=form_data.get("full_name", ""),
            country=form_data.get("country", ""),
            phone=form_data.get("phone", ""),
            desired_profit_margin=form_data.get("profit_margin", ""),
            markets=form_data.get("markets", []),
        )

        # Optional logo
        logo_filename = form_data.get("logo_filename")
        if logo_filename:
            order.logo = logo_filename
            order.save()

        return JsonResponse({"status": "success", "order_id": order.id})

    except Exception as e:
        # Print real error for debugging
        print("ORDER CREATION ERROR:", e)

        return JsonResponse({
            "status": "error",
            "detail": str(e)
        }, status=500)


def learn_more(request):
    return render(request, 'orders/learn-more.html')

