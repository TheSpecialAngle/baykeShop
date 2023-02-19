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


from django.forms.widgets import TextInput as BaseTextInput


class SearchTextInput(BaseTextInput):
    
    input_type = "search"
    template_name = "baykeshop/widgets/input.html"