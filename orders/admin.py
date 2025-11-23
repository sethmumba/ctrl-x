from django.contrib import admin
from .models import Order

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('store_name', 'user', 'is_paid', 'progress', 'assigned_staff', 'created_at')
    list_filter = ('is_paid', 'progress', 'niche', 'supplier')
    search_fields = ('store_name', 'user__username')
