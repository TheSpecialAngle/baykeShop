#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@文件    :models.py
@说明    :站点统计模块
@时间    :2023/03/22 09:15:19
@作者    :幸福关中&轻编程
@版本    :1.0
@微信    :baywanyun
'''

from django.db import models
from baykeshop.public.abstract import AbstractModel, ContentTypeAbstract


class BaykeIPAddress(AbstractModel):
    """ 统计站点来访IP """
    # 当前 IP：111.18.146.46  来自于：中国 陕西 咸阳  移动
    # http://myip.ipip.net/
    ip = models.GenericIPAddressField(null=True, blank=True)
    browser = models.TextField(max_length=500, blank=True, default="")
    address = models.CharField(max_length=150, blank=True, default="")

    class Meta:
        verbose_name = 'BaykeStatsIPAddress'
        verbose_name_plural = 'BaykeStatsIPAddress'

    def __str__(self):
        return self.address


class BaykeStats(ContentTypeAbstract):
    """ pv 和 uv统计 """
    pv = models.BigIntegerField(default=0)
    uv = models.BigIntegerField(default=0)

    class Meta:
        verbose_name = 'BaykeStats'
        verbose_name_plural = 'BaykeStatss'

    def __str__(self):
        return f"pv:{self.pv} | uv: {self.uv}"


