from django.db import models
from django.contrib.auth.models import User
from staff.utils import assign_least_busy_staff  # make sure you have this function

# -------------------
# Service Model
# -------------------
class CustomService(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    min_price = models.DecimalField(max_digits=10, decimal_places=2)
    max_price = models.DecimalField(max_digits=10, decimal_places=2)
    is_active = models.BooleanField(default=True)

    # NEW: Image URL
    image_url = models.URLField(blank=True, null=True, help_text="URL of the service image")

    def __str__(self):
        return self.title


# -------------------
# Order Model
# -------------------
class CustomOrder(models.Model):
    STATUS_CHOICES = (
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    )

    service = models.ForeignKey(CustomService, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField()
    budget = models.DecimalField(max_digits=10, decimal_places=2)
    assigned_staff = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_custom_orders'
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='in_progress')
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.assigned_staff:
            self.assigned_staff = assign_least_busy_staff()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} - {self.service.title}"
