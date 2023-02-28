#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@文件    :__init__.py
@说明    :表单小部件
@时间    :2023/02/19 18:37:14
@作者    :幸福关中&轻编程
@版本    :1.0
@微信    :baywanyun
'''

from django.forms.widgets import Widget
from django.forms.widgets import (
    TextInput as BaseTextInput,
    Textarea as BaseTextarea
)


class SearchTextInput(BaseTextInput):
    """ 搜索框 """
    input_type = "search"
    template_name = "baykeshop/widgets/input.html"
    
    

class HTMLTextarea(BaseTextarea):
    
    template_name = "baykeadmin/widgets/editor.html"
    
    def __init__(self, attrs=None):
        super().__init__(attrs)

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        return context
    
    class Media:
        # css = {
        #     'all': ('pretty.css',)
        # }
        js = (
            # 'baykeadmin/js/tinymce/tinymce.min.js',
            # 'baykeadmin/js/config.js',
        )
    