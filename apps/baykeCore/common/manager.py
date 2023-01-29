#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@文件    :manager.py
@说明    :全局管理器manager入口
@时间    :2023/01/07 17:33:02
@作者    :幸福关中&轻编程
@版本    :1.0
@微信    :baywanyun
'''


from django.db import models
from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder
from .queryset import BaykeQueryset



class BaykeManager(models.Manager):
    
    def get_queryset(self):
        return BaykeQueryset(self.model, using=self._db)
    
    def is_del_false(self):
        return self.get_queryset().is_del_false()
    
    def is_del_true(self):
        return self.get_queryset().is_del_true()
    
    def show(self):
        return self.is_del_false()
