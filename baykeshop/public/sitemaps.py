#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@文件    :sitemaps.py
@说明    :站点地图
@时间    :2023/03/23 21:03:40
@作者    :幸福关中&轻编程
@版本    :1.0
@微信    :baywanyun
'''


from django.contrib.sitemaps import Sitemap
from django.contrib.flatpages.sitemaps import FlatPageSitemap

from baykeshop import models


class BaykeShopSPUSitemap(Sitemap):
    changefreq = "never"
    priority = 0.5

    def items(self):
        return models.BaykeShopSPU.objects.filter(is_del=False)

    def lastmod(self, obj):
        return obj.pub_date
    
    
class BaykeShopCategorySitemap(Sitemap):
    changefreq = "never"
    priority = 0.5

    def items(self):
        return models.BaykeShopCategory.objects.filter(is_del=False)

    def lastmod(self, obj):
        return obj.pub_date
    

sitemaps = {
    'spu': BaykeShopSPUSitemap,
    'cate': BaykeShopCategorySitemap,
    'flatpage': FlatPageSitemap
}