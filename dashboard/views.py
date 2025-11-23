from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from orders.models import Order
from orders.models import Order, PROGRESS_STEPS


@login_required
def dashboard_home(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'dashboard/home.html', {'orders': orders})

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