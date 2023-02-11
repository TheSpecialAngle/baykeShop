#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@文件    :cart.py
@说明    :购物车模型
@时间    :2023/02/08 21:02:24
@作者    :幸福关中&轻编程
@版本    :1.0
@微信    :baywanyun
'''

from django.db import models
from django.contrib.auth import get_user_model

from baykeCore.models import BaykeModelMixin
from baykeShop.models import BaykeShopSKU

User = get_user_model()


class BaykeShopingCart(BaykeModelMixin):
    # 购物车数据模型
    owner = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name="用户")
    sku = models.ForeignKey(BaykeShopSKU, on_delete=models.PROTECT, verbose_name="商品sku")
    num = models.PositiveIntegerField(default=0, verbose_name="数量")
    
    class Meta:
        verbose_name = '购物车'
        verbose_name_plural = verbose_name
        constraints = [
            models.UniqueConstraint(fields=['owner', 'sku'], name='unique_owner_sku')
        ]
        
    def __str__(self):
        return f'{self.owner}{self.sku}'
    
    @classmethod
    def get_cart_count(cls, user):
        # 当前用户的购物车数量
        return cls.objects.show().filter(owner=user).count()
    

class BaykeShopAddress(BaykeModelMixin):
    """收货地址
    """
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="用户")
    name = models.CharField("签收人", max_length=50)
    phone = models.CharField("手机号", max_length=11)
    email = models.EmailField("邮箱", blank=True, default="", max_length=50)
    province = models.CharField(max_length=150, verbose_name="省")
    city = models.CharField(max_length=150, verbose_name="市")
    county = models.CharField(max_length=150, verbose_name="区/县")
    address = models.CharField(max_length=150, verbose_name="详细地址")
    is_default = models.BooleanField(default=False, verbose_name="设为默认")
    
    class Meta:
        verbose_name = "收货地址"
        verbose_name_plural = verbose_name
       
    def __str__(self):
        return f'{self.name} {self.address}'