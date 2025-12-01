from django.contrib import admin
from .models import CustomService, CustomOrder

@admin.register(CustomService)
class CustomServiceAdmin(admin.ModelAdmin):
    list_display = ('title', 'min_price', 'max_price', 'is_active', 'image_url')
    list_filter = ('is_active',)
    search_fields = ('title', 'description')

@admin.register(CustomOrder)
class CustomOrderAdmin(admin.ModelAdmin):
    list_display = ('service', 'user', 'budget', 'assigned_staff', 'status', 'created_at')
    list_filter = ('status',)
    search_fields = ('description', 'user__username', 'service__title')
