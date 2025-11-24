from django.db.models.signals import post_save
from django.dispatch import receiver
from orders.models import Order
from staff.utils import assign_least_busy_staff  # make sure path is correct
from django.core.mail import send_mail

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

            # Notify staff
            send_mail(
                subject="New Store Task Assigned",
                message=f"You have been assigned a new store: {instance.store_name}",
                from_email=None,
                recipient_list=[staff.email],
                fail_silently=True,
            )
