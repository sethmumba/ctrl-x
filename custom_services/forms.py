from django import forms
from .models import CustomOrder

class CustomOrderForm(forms.ModelForm):
    class Meta:
        model = CustomOrder
        fields = ['service', 'description', 'budget']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }
