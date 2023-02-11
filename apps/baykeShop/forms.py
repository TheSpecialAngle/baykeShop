import re

from django import forms
from django.contrib.auth.forms import AuthenticationForm, UsernameField
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import password_validation
from django.utils.functional import lazy
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from django.utils.html import format_html_join, format_html
from django.core.exceptions import ValidationError

from baykeShop.models import BaykeShopAddress
from baykeShop.widgets import SearchTextInput


def _password_validators_help_text_html(password_validators=None):
    """
    Return an HTML string with all help texts of all configured validators
    in an <ul>.
    """
    help_texts = password_validation.password_validators_help_texts(password_validators)
    help_items = format_html_join('', '<p>{}</p>', ((help_text,) for help_text in help_texts))
    return format_html('<div class="help">{}</div>', help_items) if help_items else ''

password_validators_help_text_html = lazy(_password_validators_help_text_html, str)


class BaykeShopUsernameField(UsernameField):

    def widget_attrs(self, widget):
        return {
            'class': 'input',
            'placeholder':'请输入用户名...',
            **super().widget_attrs(widget)
        }


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
        widget=forms.TextInput(attrs={
            "autofocus": True, 
            "class": "input", 
            "placeholder":" 请输入用户名..."
        }))
    password = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={
            "autocomplete": "current-password", 
            "class": "input", 
            "placeholder":" 请输入密码..."
        }),
    )


class RegisterForm(UserCreationForm):
    
    password1 = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={
            'autocomplete': 'new-password', 
            'class': 'input', 
            "placeholder":" 请输入密码..."
        }),
        help_text=password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        label=_("Password confirmation"),
        widget=forms.PasswordInput(attrs={
            'autocomplete': 'new-password', 
            'class': 'input',
            "placeholder":" 请再次输入用户名..."
        }),
        strip=False,
        help_text=_("Enter the same password as before, for verification."),
    )

    class Meta:
        model = User
        fields = ("username",)
        field_classes = {'username': BaykeShopUsernameField}
        

class BaykeShopAddressForm(forms.ModelForm):
    # 地址表单
    class Meta:
        model = BaykeShopAddress
        exclude = ('email', 'owner')
        
    def clean(self):
        # print(self.cleaned_data)
        return super().clean()
    
    def clean_phone(self):
        phone = self.cleaned_data['phone']
        ret = re.match(r"^1[35678]\d{9}$", phone)
        if not ret:
            raise ValidationError("手机号格式不正确！")
        return phone
