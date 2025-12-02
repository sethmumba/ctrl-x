from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import CustomService, CustomOrder
from .forms import CustomOrderForm
from django.conf import settings
from .email_utils import send_email  # <---- IMPORTANT
from .serializers import CustomServiceSerializer
from rest_framework.permissions import IsAdminUser
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework.response import Response


# -------------------
# List all services
# -------------------
def services_list(request):
    services = CustomService.objects.filter(is_active=True)
    return render(request, 'custom_services/services_list.html', {'services': services})


# -------------------
# Create custom order with email notifications
# -------------------
@login_required
def create_order(request, service_id=None):
    if request.method == 'POST':
        form = CustomOrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.save()

            # -------- Email to Client --------
            send_email(
                to_email=order.user.email,
                subject="Your Custom Order has been received",
                html_content=f"""
                    <p>Hi {order.user.username},</p>
                    <p>Your order for <strong>{order.service.title}</strong> has been received.</p>
                    <p>Budget: {order.budget}</p>
                    <p>Status: {order.status}</p>
                    <p>Thank you!</p>
                """
            )

            # -------- Email to Admin --------
            send_email(
                to_email=settings.ADMIN_EMAIL,
                subject="New Custom Order Submitted",
                html_content=f"""
                    <p>Admin, a new order was submitted:</p>
                    <p><strong>User:</strong> {order.user.username}</p>
                    <p><strong>Service:</strong> {order.service.title}</p>
                    <p><strong>Budget:</strong> {order.budget}</p>
                    <p><strong>Description:</strong> {order.description}</p>
                    <p><strong>Assigned Staff:</strong> {order.assigned_staff}</p>
                """
            )

            return redirect('my_orders')

    else:
        initial = {}
        if service_id:
            initial['service'] = service_id
        form = CustomOrderForm(initial=initial)

    return render(request, 'custom_services/create_order.html', {'form': form})


# -------------------
# User's orders
# -------------------
@login_required
def my_orders(request):
    orders = CustomOrder.objects.filter(user=request.user)
    return render(request, 'custom_services/my_orders.html', {'orders': orders})


# -------------------
# Staff dashboard
# -------------------
@login_required
def staff_orders(request):
    orders = CustomOrder.objects.filter(assigned_staff=request.user)
    return render(request, 'custom_services/staff_orders.html', {'orders': orders})


# -------------------
# API: Create Custom Service (Admin only)
# -------------------
@api_view(['POST'])
@permission_classes([IsAdminUser])
def api_create_service(request):
    serializer = CustomServiceSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@login_required
def custom_order_detail(request, order_id):
    order = get_object_or_404(CustomOrder, id=order_id, user=request.user)
    return render(request, "custom_services/custom_order_detail.html", {"order": order})