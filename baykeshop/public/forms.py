from django import forms
from django.forms.widgets import Textarea as BaseTextarea
from django.contrib.flatpages.forms import FlatpageForm

from baykeshop.config.settings import bayke_settings


class HTMLTextarea(BaseTextarea):
    """ 富文本编辑器 """
    template_name = "baykeadmin/editor.html"
    
    def __init__(self, attrs=None):
        super().__init__(attrs)

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        return context
    
    class Media:
        css = {'all': ('baykeadmin/css/style.css','baykeadmin/css/editor.css')}
        js = ('baykeadmin/js/index.js',)
        
        
class BaykeUploadModelForm(forms.ModelForm):
    """ 上传图片表单 """
    class Meta:
        from baykeshop.models import BaykeUpload
        model = BaykeUpload
        fields = ('img',)
        

class SearchForm(forms.Form):
    """ 搜索表单 """
    template_name = "baykeshop/search_form.html"
    
    word = forms.CharField(
        max_length=36, 
        required=True, 
        widget=forms.TextInput(
            {
                'type': 'search', 
                'class': 'input',
                'placeholder': f'{bayke_settings.SEARCH_VALUE}'
            }
        )
    )
    

class BaykeFlatpageForm(FlatpageForm):
    # 单页面应用
    
    class Meta(FlatpageForm.Meta):
        widgets = {
            'content': HTMLTextarea(),
        }