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


class BaykeCategoryMixin(BaykeModelMixin):
    """
    分类继承基类
    """
    name = models.CharField("分类名称", max_length=50)
    icon = models.CharField("分类icon", max_length=50, blank=True, default="")
    img_map = models.ImageField(
        "分类图标", 
        upload_to="category/imgMap/%Y", 
        max_length=200,
        blank=True,
        null=True
    )
    desc = models.CharField("分类描述", max_length=150, blank=True, default="")

    # TODO

    class Meta:
        abstract = True


class BaykeCarouselMixin(BaykeModelMixin):
    """
    轮播图基类
    """
    img = models.ImageField(
        "轮播图", 
        upload_to="Carousel/%Y/%m", 
        max_length=200,
    )
    target_url = models.CharField(
        "跳转链接", 
        blank=True, 
        default="", 
        max_length=200
    )
    desc = models.CharField("描述", max_length=150, blank=True, default="")

    # TODO

    class Meta:
        abstract = True