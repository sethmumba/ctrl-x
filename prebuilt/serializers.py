from rest_framework import serializers
from .models import PrebuiltStore

class PrebuiltStoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = PrebuiltStore
        fields = ['id', 'name', 'description', 'image_url', 'store_link', 'password', 'created_at']
