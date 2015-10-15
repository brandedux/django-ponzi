from django import forms
from django.core.exceptions import ValidationError

from .models import AddressPair
from .utils import get_server

class RegisterForm(forms.ModelForm):
    class Meta:
        model = AddressPair
        exclude = ("site_addr",)
        labels = {'user_addr':"Your address"}

    def clean_user_addr(self):
        user_addr = self.cleaned_data['user_addr']
        server = get_server()
        
        if not server.validateaddress(user_addr).isvalid:
            raise ValidationError("Invalid Bitcoin Address")
        return user_addr

