#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@文件    :models.py
@说明    :全局模型基类
@时间    :2023/01/07 17:11:04
@作者    :幸福关中&轻编程
@版本    :1.0
@微信    :baywanyun
'''

from django.db import models
from django.utils.translation import gettext_lazy as _

from baykeCore.common.manager import BaykeManager


class BaykeModelMixin(models.Model):
    """全局模型基类    
    """
    add_date = models.DateTimeField(_('添加时间'), auto_now_add=True)
    pub_date = models.DateTimeField(_('更新时间'), auto_now=True)
    is_del = models.BooleanField(default=False, verbose_name=_('删除'), editable=False)
    
    objects = BaykeManager()
    
    # TODO

    class Meta:
        abstract = True
