#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@文件    :field.py
@说明    :自定义field
@时间    :2023/01/07 18:03:14
@作者    :幸福关中&轻编程
@版本    :1.0
@微信    :baywanyun
'''

from django.db import models
from django.utils.translation import gettext_lazy as _


class TinyMCEField(models.TextField):
    
    description = _("TinyMCE Editor")
    
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        
    def formfield(self, **kwargs):
        return super().formfield(**kwargs)
        
    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        return name, path, args, kwargs
    
    def get_internal_type(self):
        return "TinyMCEField"