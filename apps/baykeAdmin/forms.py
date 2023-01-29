from django import forms
from django.contrib.admin.forms import AdminAuthenticationForm
from django.contrib.auth.forms import UsernameField
from django.utils.translation import gettext_lazy as _


class BaykeAdminLoginForm(AdminAuthenticationForm):
    
    username = UsernameField(widget=forms.TextInput(attrs={
            "autofocus": True, 
            "class": "input",
            "placeholder": _("Please enter a username")
        }
    ))
    password = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={
            "autocomplete": "current-password", 
            "class": "input",
            "placeholder": _("Please enter a password")
        }),
    )