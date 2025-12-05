from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from orders.models import Order, PROGRESS_STEPS
from .forms import SupportForm
import requests
from django.http import JsonResponse
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import os
import logging

logger = logging.getLogger(__name__)


@login_required
def dashboard_home(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')

    context = {
        'orders': orders,
        'total_orders': orders.count(),
        'in_progress_orders': orders.exclude(progress='completed').count(),
        'completed_orders': orders.filter(progress='completed').count(),
    }

    return render(request, 'dashboard/home.html', context)


@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    human_status = dict(PROGRESS_STEPS).get(order.progress, "")
    step_keys = [step[0] for step in PROGRESS_STEPS]
    try:
        order_progress_index = step_keys.index(order.progress)
    except ValueError:
        order_progress_index = 0  # fallback if progress is invalid

    return render(request, 'dashboard/order_detail.html', {
        'order': order,
        'human_status': human_status,
        'PROGRESS_STEPS': PROGRESS_STEPS,
        'order_progress_index': order_progress_index,
    })


# -------------------------------
# SendGrid Email Helper
# -------------------------------
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


# -------------------------------
# Support View (Updated to SendGrid)
# -------------------------------
def support(request):
    if request.method == "POST":
        form = SupportForm(request.POST)
        if form.is_valid():
            subject = "Support Request: " + form.cleaned_data["subject"]
            message = form.cleaned_data["message"]
            user_email = request.user.email if request.user.is_authenticated else "Unknown email"
            user_name = request.user.username if request.user.is_authenticated else "Anonymous"

            final_message = f"""
From: {user_name}
Email: {user_email}

Message:
{message}
"""

            # Send support email via SendGrid
            send_email_via_sendgrid(subject, final_message, "empxautomations@gmail.com")

            return render(request, "dashboard/success.html")
    else:
        form = SupportForm()

    return render(request, "dashboard/support.html", {"form": form})
