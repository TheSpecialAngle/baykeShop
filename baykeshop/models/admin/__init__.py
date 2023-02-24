#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@文件    :__init__.py
@说明    :管理后台相关模型
@时间    :2023/02/19 17:05:29
@作者    :幸福关中&轻编程
@版本    :1.0
@微信    :baywanyun
'''

from django.db import models
from django.contrib.auth.models import Permission
from django.contrib.auth import get_user_model
from baykeshop.models.abstract import AbstractModel

User = get_user_model()


class BaykeMenu(AbstractModel):
    """ 菜单 """
    name = models.CharField(max_length=50, unique=True)
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        editable=False
    )
    sort = models.PositiveSmallIntegerField(default=1)

    class Meta:
        ordering = ['-sort']
        verbose_name = 'BaykeMenu'
        verbose_name_plural = 'BaykeMenus'

    def __str__(self):
        return self.name


class BaykePermission(AbstractModel):
    """ 权限规则 """
    permission = models.OneToOneField(
        Permission,
        on_delete=models.CASCADE,
        verbose_name="权限",
        blank=True,
        null=True
    )
    # owner = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    url = models.CharField("url", max_length=150, blank=True, default="")
    menus = models.ForeignKey(BaykeMenu, on_delete=models.CASCADE)
    icon = models.CharField(blank=True, default="", max_length=50)

    class Meta:
        verbose_name = '权限规则'
        verbose_name_plural = verbose_name

    def __str__(self):
        return f"{self.permission.name}  "
