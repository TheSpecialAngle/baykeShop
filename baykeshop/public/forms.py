from django import forms
from django.forms.widgets import Textarea as BaseTextarea


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
    
    class Meta:
        from baykeshop.models import BaykeUpload
        model = BaykeUpload
        fields = ('img',)