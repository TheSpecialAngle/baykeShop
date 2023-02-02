from django import forms
from baykeShop.widgets import SearchTextInput

class SearchForm(forms.Form):
    
    words = forms.CharField(
        max_length=30, 
        widget=SearchTextInput(attrs={
            'placeholder': 'Search...', 
            ':has-counter': 'false',
            'validation-message': '搜索词不能为空...',
            'value': '手机'
        })
    )
    
    