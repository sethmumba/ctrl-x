from django.shortcuts import render, get_object_or_404, redirect
from orders.models import Order, PROGRESS_STEPS
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.mail import send_mail

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

        # Use PROGRESS_STEPS imported from models
        if new_progress in dict(PROGRESS_STEPS).keys():
            order.progress = new_progress
            order.save()

            # Email subject & message
            subject = f"Your Store '{order.store_name}' Progress Update"
            if new_progress != 'completed':
                message = f"Hi {order.user.username},\n\nYour store '{order.store_name}' status has been updated to: {new_progress}"
            else:
                message = f"""
Hi {order.user.username},

Your dropshipping store '{order.store_name}' is now complete! 🎉

Please follow these steps to take ownership of your Shopify store:

1. Check your email for Shopify login details (provided separately if needed).  
2. Log in to Shopify and verify your store settings.  
3. Change the store password and email to your personal account.  
4. Add payment method and connect apps as desired.  
5. Begin promoting and selling your products!

If you have any questions, reply to this email and our team will assist you.

Thank you for choosing us!
"""

            # Send email
            send_mail(
                subject=subject,
                message=message,
                from_email=None,
                recipient_list=[order.user.email],
                fail_silently=True,
            )

    return redirect('staff-order-detail', order_id=order_id)