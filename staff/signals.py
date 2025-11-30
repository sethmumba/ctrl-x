from django.db.models.signals import post_save
from django.dispatch import receiver
from orders.models import Order
from staff.utils import assign_least_busy_staff  # make sure path is correct
from django.core.mail import send_mail
import threading
from staff.views import send_email_via_sendgrid


def send_email_async_sendgrid(subject, message, to_email):
    threading.Thread(
        target=send_email_via_sendgrid,
        args=(subject, message, to_email)
    ).start()
@receiver(post_save, sender=Order)
def assign_staff_on_payment(sender, instance, created, **kwargs):
    if instance.is_paid and instance.assigned_staff is None:
        staff = assign_least_busy_staff()
        if staff:
            Order.objects.filter(pk=instance.pk).update(
                assigned_staff=staff,
                progress='assigned'
            )

            send_email_async_sendgrid(
                subject="New Store Task Assigned",
                message=f"You have been assigned a new store: {instance.store_name}",
                to_email=staff.email
            )