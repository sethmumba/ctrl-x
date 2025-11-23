from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

SUPPLIER_CHOICES = [
    ('cj', 'CJ Dropshipping'),
    ('dsers', 'DSers'),
]

THEME_CHOICES = [
    ('dawn', 'Dawn'),
    ('refresh', 'Refresh'),
    ('spotlight', 'Spotlight'),
]

NICHE_CHOICES = [
    ('fashion', 'Fashion'),
    ('pets', 'Pets'),
    ('beauty', 'Beauty'),
    ('electronics', 'Electronics'),
    ('home', 'Home & Kitchen'),
    ('fitness', 'Fitness'),
]

MARKET_CHOICES = [
    ('all', 'Worldwide'),
    ('us', 'United States'),
    ('uk', 'United Kingdom'),
    ('ca', 'Canada'),
    ('au', 'Australia'),
    ('eu', 'Europe'),
]

PROGRESS_STEPS = [
    ('paid', 'Payment Received'),
    ('assigned', 'Staff Assigned'),
    ('started', 'Store Creation Started'),
    ('products', 'Products Imported'),
    ('branding', 'Branding/Theme Configured'),
    ('review', 'Store Ready for Review'),
    ('completed', 'Store Delivered'),
]

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)

    # Payment info
    is_paid = models.BooleanField(default=False)
    paypal_order_id = models.CharField(max_length=200, blank=True, null=True)

    # Store details
    store_name = models.CharField(max_length=50)
    niche = models.CharField(max_length=30, choices=NICHE_CHOICES)
    supplier = models.CharField(max_length=20, choices=SUPPLIER_CHOICES)
    theme = models.CharField(max_length=20, choices=THEME_CHOICES)
    color_palette = models.CharField(max_length=100)
    desired_profit_margin = models.CharField(max_length=20)

    logo = models.ImageField(upload_to='logos/', blank=True, null=True)

    # Market selection (multiple choices)
    markets = models.JSONField(default=list)

    # Progress tracking
    progress = models.CharField(
        max_length=20,
        choices=PROGRESS_STEPS,
        default='paid'
    )

    # Staff assignment
    assigned_staff = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL,
        related_name="assigned_orders",
        null=True,
        blank=True
    )

    def __str__(self):
        return f"{self.store_name} ({self.user.username})"

    class Meta:
        ordering = ['-created_at']
