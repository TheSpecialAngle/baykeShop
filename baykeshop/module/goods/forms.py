from django import forms
from baykeshop.models import BaykeShopSPU
from baykeshop.public.forms import HTMLTextarea



class BaykeShopSPUForm(forms.ModelForm):
    # 商品表单
    class Meta:
        model = BaykeShopSPU
        fields = "__all__"
        widgets = {
            'content': HTMLTextarea(),
        }