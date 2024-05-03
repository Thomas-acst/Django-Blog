from django import forms
from .models import Info_User

class UserForm(forms.ModelForm):

    class Meta:
        model = Info_User
        widgets = {
        'password': forms.PasswordInput(),
    }