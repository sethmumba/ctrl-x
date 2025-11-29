from django.db.models.signals import post_save
from django.dispatch import receiver
from orders.models import Order
from staff.utils import assign_least_busy_staff  # make sure path is correct
from django.core.mail import send_mail
import threading

def send_email_async(subject, message, from_email, recipient_list):
    """Send email in a separate thread to avoid blocking."""
    threading.Thread(
        target=send_mail,
        args=(subject, message, from_email, recipient_list),
        kwargs={'fail_silently': True}
    ).start()

@receiver(post_save, sender=Order)
def assign_staff_on_payment(sender, instance, created, **kwargs):
    if instance.is_paid and instance.assigned_staff is None:
        staff = assign_least_busy_staff()
        if staff:
            # Update without triggering post_save again
            Order.objects.filter(pk=instance.pk).update(
                assigned_staff=staff,
                progress='assigned'
            )

            # Notify staff asynchronously
            send_email_async(
                subject="New Store Task Assigned",
                message=f"You have been assigned a new store: {instance.store_name}",
                from_email=None,  # None will use DEFAULT_FROM_EMAIL
                recipient_list=[staff.email]
            )
