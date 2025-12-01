from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.http import HttpResponse
from django.core.mail import send_mail
from .models import PrebuiltStore

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import PrebuiltStoreSerializer

import logging
import os
logger = logging.getLogger(__name__)

# View to list all prebuilt stores
def prebuilt_home(request):
    stores = PrebuiltStore.objects.all()
    return render(request, "prebuilt/prebuilt.html", {"stores": stores})

#API: List + Create Prebuilt Stores
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


#SENDGRID Email Helper (same logic as staff app)
def send_email_via_sendgrid(subject, message, to_email):
    msg = Mail(
        from_email='support@empxautomations.site',
        to_emails=to_email,
        subject=subject,
        plain_text_content=message
    )
    try:
        sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        response = sg.send(msg)
        logger.info(f"SendGrid Email Sent: {response.status_code}")
        return response.status_code
    except Exception as e:
        logger.error(f"SendGrid Error: {e}")
        return None



#Handle Prebuilt Store Order (Updated to SendGrid)
@login_required
def order_prebuilt_store(request):
    if request.method == "POST":
        store_id = request.POST.get("store_id")
        store = get_object_or_404(PrebuiltStore, id=store_id)

        # EMAIL TO ADMIN
        admin_subject = f"New Prebuilt Store Order: {store.name}"
        admin_message = (
            f"User {request.user.username} ({request.user.email}) "
            f"ordered the prebuilt store: {store.name}"
        )

        send_email_via_sendgrid(admin_subject, admin_message, settings.ADMIN_EMAIL)

        # EMAIL TO USER
        user_subject = "Your Prebuilt Store Order Confirmation"
        user_message = (
            f"Hi {request.user.username},\n\n"
            f"Thank you for ordering '{store.name}'. Our seller will contact you shortly.\n\n"
            f"Regards,\nEmpx Automations Team"
        )

        send_email_via_sendgrid(user_subject, user_message, request.user.email)

        return redirect("prebuilt_order_success")

    return redirect("dashboard_home")


# Order Success Page
def prebuilt_order_success(request):
    return render(request, "prebuilt/order_success.html")
