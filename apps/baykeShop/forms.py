from django import forms
from django.contrib.auth.forms import AuthenticationForm, UsernameField
from django.utils.translation import gettext_lazy as _

from baykeShop.widgets import SearchTextInput, TextInput, PasswordInput



class SearchForm(forms.Form):
    # 搜索框
    words = forms.CharField(
        max_length=30, 
        widget=SearchTextInput(attrs={
            'placeholder': 'Search...', 
            ':has-counter': 'false',
            'validation-message': '搜索词不能为空...',
            'value': '手机'
        })
    )
    

class OrderSPUForm(forms.Form):
    # 筛选框
    field = forms.CharField(max_length=30)
    order = forms.CharField(max_length=10)
    

class LoginForm(AuthenticationForm):
    username = UsernameField(
        widget=forms.TextInput(attrs={"autofocus": True, "class": "input"}))
    password = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "current-password", "class": "input"}),
    )