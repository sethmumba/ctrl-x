from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import CustomService, CustomOrder
from .forms import CustomOrderForm
from django.conf import settings
from django.core.mail import send_mail
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
# Create custom order
# -------------------
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
            send_mail(
                subject="Your Custom Order has been received",
                message=f"Hi {order.user.username},\n\n"
                        f"Your order for '{order.service.title}' has been received.\n"
                        f"Budget: {order.budget}\n"
                        f"Status: {order.status}\n\nThank you!",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[order.user.email],
            )

            # -------- Email to Admin --------
            send_mail(
                subject="New Custom Order Submitted",
                message=f"Admin,\n\n"
                        f"User '{order.user.username}' submitted a new order:\n"
                        f"Service: {order.service.title}\n"
                        f"Budget: {order.budget}\n"
                        f"Description: {order.description}\n"
                        f"Assigned Staff: {order.assigned_staff}\n",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.ADMIN_EMAIL],
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