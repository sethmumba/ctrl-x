from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from orders.models import Order
from orders.models import Order, PROGRESS_STEPS


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
    # Fetch the order for this user
    order = get_object_or_404(Order, id=order_id, user=request.user)

    # Human-readable status
    human_status = dict(PROGRESS_STEPS).get(order.progress, "")

    # Determine index of current progress
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




from django.core.mail import send_mail
from django.shortcuts import render
from .forms import SupportForm

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

            send_mail(
                subject,
                final_message,
                "empxautomations@gmail.com",      # your sending address
                ["empxautomations@gmail.com"],    # where YOU receive support requests
            )

            return render(request, "dashboard/success.html")

    else:
        form = SupportForm()

    return render(request, "dashboard/support.html", {"form": form})
