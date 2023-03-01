import re
from django import forms
from django.core.exceptions import ValidationError

from baykeshop.conf.bayke import bayke_settings
from baykeshop.models import (
    BaykeShopAddress, BaykeUserInfo, BaykeShopSPU, BaykeUpload
)
from baykeshop.forms.widgets import HTMLTextarea



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
        ret = re.match(bayke_settings.PHONE_REGX, phone)
        if not ret:
            raise ValidationError("手机号格式不正确！")
        return phone


class BaykeUserInfoForm(forms.ModelForm):
    
    class Meta:
        model = BaykeUserInfo
        fields = ['owner', 'avatar', 'nickname']
        
    def clean(self):
        return super().clean()
    

class BaykeShopSPUForm(forms.ModelForm):
    # 商品表单
    class Meta:
        model = BaykeShopSPU
        fields = "__all__"
        widgets = {
            'content': HTMLTextarea(),
        }


class BaykeUploadModelForm(forms.ModelForm):
    
    class Meta:
        model = BaykeUpload
        fields = ('img',)