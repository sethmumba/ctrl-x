from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
from .models import PrebuiltStore

def prebuilt_home(request):
    stores = PrebuiltStore.objects.all()
    return render(request, "prebuilt/prebuilt.html", {"stores": stores})

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import PrebuiltStoreSerializer

@api_view(['GET', 'POST'])
def prebuilt_list_create(request):
    if request.method == 'GET':
        stores = PrebuiltStore.objects.all()
        serializer = PrebuiltStoreSerializer(stores, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = PrebuiltStoreSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@login_required
def order_prebuilt_store(request):
    if request.method == "POST":
        store_id = request.POST.get("store_id")
        store = get_object_or_404(PrebuiltStore, id=store_id)

        # Send email to admin
        send_mail(
            subject=f"New Prebuilt Store Order: {store.name}",
            message=f"User {request.user.username} ({request.user.email}) ordered the store: {store.name}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.ADMIN_EMAIL],
        )

        # Send confirmation email to user
        send_mail(
            subject="Your Prebuilt Store Order",
            message=(
                f"Hi {request.user.username},\n\n"
                f"Thank you for ordering '{store.name}'. Our seller will contact you shortly."
            ),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[request.user.email],
        )

        # Redirect to success page
        return redirect("prebuilt_order_success")

    return redirect("dashboard_home")

def prebuilt_order_success(request):
    return render(request, "prebuilt/order_success.html")
