from rest_framework import serializers
from .models import CustomService

class CustomServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomService
        fields = ['id', 'title', 'description', 'min_price', 'max_price', 'is_active', 'image_url']
