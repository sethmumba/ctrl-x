from django.contrib import admin
from .models import PrebuiltStore

@admin.register(PrebuiltStore)
class PrebuiltStoreAdmin(admin.ModelAdmin):
    list_display = ('name', 'store_link', 'created_at')
    search_fields = ('name', 'description')
    list_filter = ('created_at',)
