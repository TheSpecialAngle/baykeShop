#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@文件    :queryset.py
@说明    :全局Queryset类
@时间    :2023/01/07 17:18:18
@作者    :幸福关中&轻编程
@版本    :1.0
@微信    :baywanyun
'''

from django.db import models


class BaykeQueryset(models.QuerySet):
    
    def is_del_true(self):
        # 已伪删除
        return self.filter(is_del=True)
    
    def is_del_false(self):
        # 未伪删除
        return self.filter(is_del=False)
    

