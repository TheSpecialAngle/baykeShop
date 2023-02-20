#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@文件    :spec.py
@说明    :商品规格相关模型
@时间    :2023/02/19 17:41:42
@作者    :幸福关中&轻编程
@版本    :1.0
@微信    :baywanyun
'''


from django.db import models
from baykeshop.models.abstract import AbstractModel


class BaykeShopSpec(AbstractModel):
    """ 规格 """
    name = models.CharField(
        max_length=50,
        unique=True,
        verbose_name="规格"
    )

    class Meta:
        verbose_name = '商品规格'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class BaykeShopSpecOption(AbstractModel):
    """ 规格值 """

    name = models.CharField(
        max_length=50,
        unique=True,
        verbose_name="规格值"
    )
    spec = models.ForeignKey(
        BaykeShopSpec,
        on_delete=models.PROTECT,
        verbose_name="规格"
    )

    class Meta:
        verbose_name = '规格值'
        verbose_name_plural = verbose_name

    def __str__(self):
        return f"{self.spec.name} - {self.name}"
