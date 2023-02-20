#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@文件    :order.py
@说明    :商品订单相关模型
@时间    :2023/02/19 17:45:30
@作者    :幸福关中&轻编程
@版本    :1.0
@微信    :baywanyun
'''


from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model

from baykeshop.models.abstract import AbstractModel
from baykeshop.models.shop.product import BaykeShopSKU

User = get_user_model()


class BaykeShopOrderInfo(AbstractModel):
    """订单信息"""

    class PayMethodChoices(models.IntegerChoices):
        CASH = 1, _('货到付款')
        ALIPAY = 2, _('支付宝')
        WECHATPAY = 3, _('微信支付')
        OVERPAY = 4, _('余额支付')

    class OrderStatusChoices(models.IntegerChoices):
        TOBPAY = 1, _('待支付')
        TOBDELIVER = 2, _('待发货')
        TOBRECEIVED = 3, _('待收货')
        TOBEVALUATE = 4, _('待评价')
        COMPLETE = 5, _('已完成')
        CANCELLED = 6, _('已取消')

    owner = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        verbose_name="用户",
        editable=False
    )
    order_sn = models.CharField(
        blank=True,
        default="",
        unique=True,
        max_length=32,
        editable=False,
        verbose_name="订单号",
        help_text="订单号"
    )
    trade_sn = models.CharField(
        blank=True, null=True,
        unique=True, max_length=64,
        verbose_name="交易号",
        help_text="交易号",
        editable=False
    )
    pay_status = models.IntegerField(
        choices=OrderStatusChoices.choices,
        default=1,
        verbose_name="支付状态",
        help_text="支付状态"
    )
    pay_method = models.IntegerField(
        choices=PayMethodChoices.choices,
        verbose_name="支付方式",
        help_text="支付方式",
        blank=True,
        null=True,
        editable=False
    )
    total_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        verbose_name="商品总金额"
    )
    order_mark = models.CharField(
        blank=True,
        default="",
        max_length=100,
        verbose_name="订单备注",
        help_text="订单备注"
    )
    freight = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        verbose_name="运费",
        blank=True,
        default=0.00
    )
    name = models.CharField("签收人", max_length=50, default="")
    phone = models.CharField("手机号", max_length=11, default="")
    email = models.EmailField("邮箱", blank=True, default="", max_length=50)
    address = models.CharField("地址", max_length=200)
    pay_time = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="支付时间",
        help_text="支付时间",
        editable=False
    )

    class Meta:
        verbose_name = '订单信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.order_sn

    @classmethod
    def get_pay_method(cls):
        # 支付方式列表字典
        return dict(cls.PayMethodChoices.choices)

    @classmethod
    def get_pay_default(cls):
        # 获取支付方式的默认值
        return cls._meta.get_field('pay_method').default

    @classmethod
    def get_tabs_label(cls, pay_status):
        if pay_status is not None:
            label_dict = dict(cls.OrderStatusChoices.choices)
            return label_dict.get(int(pay_status))
        return "全部订单"


class BaykeShopOrderSKU(AbstractModel):
    """订单商品"""
    order = models.ForeignKey(
        BaykeShopOrderInfo,
        on_delete=models.PROTECT,
        verbose_name="订单",
        editable=False
    )
    sku = models.ForeignKey(
        BaykeShopSKU,
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        verbose_name="订单商品",
        editable=False
    )
    title = models.CharField("商品标题", max_length=200, blank=True, default="")
    desc = models.CharField("商品说明", max_length=200, blank=True, default="")
    spec = models.CharField("商品规格", max_length=200, blank=True, default="")
    content = models.TextField("商品详情", blank=True, default="")
    count = models.IntegerField(default=1, verbose_name="数量")
    price = models.DecimalField('单价', max_digits=18, decimal_places=2)
    is_commented = models.BooleanField(default=False, verbose_name="是否已评价")

    class Meta:
        verbose_name = '订单商品'
        verbose_name_plural = verbose_name

    def __str__(self) -> str:
        return self.sku.spu.title
