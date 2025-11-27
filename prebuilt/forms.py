from django import forms

class PrebuiltOrderForm(forms.Form):
    store_id = forms.IntegerField(widget=forms.HiddenInput)
