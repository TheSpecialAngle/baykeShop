#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@文件    :filter.py
@说明    :商品列表页筛选表单
@时间    :2023/02/19 18:42:58
@作者    :幸福关中&轻编程
@版本    :1.0
@微信    :baywanyun
'''


from django import forms

class ProductFilterForm(forms.Form):
    """ 筛选框 """
    field = forms.CharField(max_length=30)
    order = forms.CharField(max_length=10)