from django import forms
from baykeShop.widgets import SearchTextInput

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
    a = forms.CharField(max_length=30)
    b = forms.CharField(max_length=10)
    
    def clean(self):
        print(super().clean())
        return super().clean()