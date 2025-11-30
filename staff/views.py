from django.shortcuts import render, get_object_or_404, redirect
from orders.models import Order, PROGRESS_STEPS
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.mail import send_mail
from django.conf import settings

def staff_required(user):
    return user.is_staff

@login_required
@user_passes_test(staff_required)
def staff_dashboard(request):
    orders = Order.objects.filter(assigned_staff=request.user).order_by('-created_at')
    return render(request, 'staff/dashboard.html', {'orders': orders})


@login_required
@user_passes_test(staff_required)
def staff_order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, assigned_staff=request.user)
    
    context = {
        'order': order,
        'progress_choices': PROGRESS_STEPS,  # <-- add this
    }
    return render(request, 'staff/order_detail.html', context)

@login_required
@user_passes_test(staff_required)
def update_order_progress(request, order_id):
    if request.method == 'POST':
        order = get_object_or_404(Order, id=order_id, assigned_staff=request.user)
        new_progress = request.POST.get('progress')

        if new_progress in dict(PROGRESS_STEPS).keys():
            order.progress = new_progress
            order.save()

            subject = f"Your Store '{order.store_name}' Progress Update"

            if new_progress != 'completed':
                message = f"Hi {order.user.username},\n\nYour store '{order.store_name}' status has been updated to: {new_progress}"
            else:
                message = f"""Hi {order.user.username},\n\nYour dropshipping store '{order.store_name}' is now complete! 🎉\n\nFollow the steps to take ownership of your Shopify store..."""

            try:
                send_mail(
                    subject=subject,
                    message=message,
                    from_email='support@empxautomations.site',  # must be verified in SendGrid
                    recipient_list=[order.user.email],
                    fail_silently=False,  # will show errors if it fails
                )
            except Exception as e:
                print("Email failed:", e)

    return redirect('staff-order-detail', order_id=order_id)
