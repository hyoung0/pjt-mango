from django import forms
from .models import Store


class StoreForm(forms.ModelForm):
    class Meta:
        model = Store
        exclude = ('like_users', 'latitude', 'longitude', )

