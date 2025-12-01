import os
import logging

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import PrebuiltStore
from .serializers import PrebuiltStoreSerializer

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

# Logger setup
logger = logging.getLogger(__name__)


# ----------------------------
# Helper: Send email via SendGrid
# ----------------------------
def send_email_via_sendgrid(subject, message, to_email):
    msg = Mail(
        from_email=settings.DEFAULT_FROM_EMAIL,
        to_emails=to_email,
        subject=subject,
        plain_text_content=message
    )
    try:
        sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        response = sg.send(msg)
        logger.info(f"SendGrid Email Sent to {to_email}: {response.status_code}")
        return response.status_code
    except Exception as e:
        logger.error(f"SendGrid Error sending email to {to_email}: {e}")
        return None


# ----------------------------
# PAGE: Prebuilt Stores Home
# ----------------------------
def prebuilt_home(request):
    stores = PrebuiltStore.objects.all()
    return render(request, "prebuilt/prebuilt.html", {"stores": stores})


# ----------------------------
# API: List + Create Prebuilt Stores
# ----------------------------
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


# ----------------------------
# ORDER: Handle Prebuilt Store Order
# ----------------------------
@login_required
def order_prebuilt_store(request):
    if request.method == "POST":
        store_id = request.POST.get("store_id")
        store = get_object_or_404(PrebuiltStore, id=store_id)

        logger.info(f"Processing prebuilt store order. Store ID: {store.id}, User: {request.user.username}")

        # --- Email to Admin ---
        admin_subject = f"New Prebuilt Store Order: {store.name}"
        admin_message = (
            f"User {request.user.username} ({request.user.email}) "
            f"ordered the prebuilt store: {store.name}"
        )
        admin_email = settings.ADMIN_EMAIL
        logger.info(f"Attempting to send admin email to: {admin_email}")

        admin_status = send_email_via_sendgrid(admin_subject, admin_message, admin_email)
        if admin_status:
            logger.info(f"Admin email sent successfully: {admin_status}")
        else:
            logger.error(f"Failed to send admin email for store {store.id}")

        # --- Email to User ---
        user_subject = "Your Prebuilt Store Order Confirmation"
        user_message = (
            f"Hi {request.user.username},\n\n"
            f"Thank you for ordering '{store.name}'. Our seller will contact you shortly.\n\n"
            f"Regards,\nEmpx Automations Team"
        )
        user_email = request.user.email
        logger.info(f"Attempting to send confirmation email to user: {user_email}")

        user_status = send_email_via_sendgrid(user_subject, user_message, user_email)
        if user_status:
            logger.info(f"User confirmation email sent successfully: {user_status}")
        else:
            logger.error(f"Failed to send confirmation email to user {user_email}")

        return redirect("prebuilt_order_success")

    logger.warning("Non-POST request received for prebuilt store order")
    return redirect("dashboard_home")


# ----------------------------
# SUCCESS PAGE
# ----------------------------
def prebuilt_order_success(request):
    return render(request, "prebuilt/order_success.html")


# ----------------------------
# SUPPORT SUCCESS PAGE
# ----------------------------
@login_required
def support_success(request):
    return render(request, "dashboard/support_success.html")
