#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@文件    :search.py
@说明    :搜索相关表单
@时间    :2023/02/19 18:41:25
@作者    :幸福关中&轻编程
@版本    :1.0
@微信    :baywanyun
'''


from django import forms

from baykeshop.forms.widgets import SearchTextInput
from baykeshop.conf.bayke import bayke_settings


class SearchForm(forms.Form):
    # 搜索框
    words = forms.CharField(
        max_length=30,
        widget=SearchTextInput(attrs={
            'placeholder': 'Search...',
            ':has-counter': 'false',
            'validation-message': '搜索词不能为空...',
            'value': bayke_settings.SEARCH_VALUE
        })
    )
