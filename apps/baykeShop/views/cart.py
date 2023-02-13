#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@文件    :cart.py
@说明    :购物车相关视图
@时间    :2023/02/13 09:26:52
@作者    :幸福关中&轻编程
@版本    :1.0
@微信    :baywanyun
'''

import json
from django.db.models import F
from django.db.utils import IntegrityError
from django.views.generic import View
from django.http import JsonResponse
from django.template.response import TemplateResponse
from django.http import QueryDict
from django.contrib.auth import get_user_model

User = get_user_model()

from baykeCore.common.mixin import LoginRequiredMixin
from baykeShop.models import (
    BaykeShopSKU, BaykeShopingCart, BaykeShopAddress,
    BaykeShopOrderInfo, BaykeShopOrderSKU
)


class BaykeShopCartView(LoginRequiredMixin, View):
    
    template_name = None

    def get(self, request, *args, **kwargs):
        # 查询出当前用户的购物车商品
        cart_queryset = BaykeShopingCart.objects.show().filter(owner=request.user, sku__stock__gte=1)
        total = 0
        carts = []
        for cart in cart_queryset:
            cart_dict = {}
            cart_dict['id'] = cart.id
            cart_dict['title'] = cart.sku.spu.title
            cart_dict['sku_id'] = cart.sku.id
            cart_dict['cover_pic'] = cart.sku.cover_pic.name
            cart_dict['options'] = list(cart.sku.options.show().values('name', 'spec__name'))
            cart_dict['price'] = cart.sku.price
            cart_dict['stock'] = cart.sku.stock
            cart_dict['sales'] = cart.num
            cart_dict['total_price'] = cart.num * cart.sku.price
            carts.append(cart_dict)
            total += cart.num * cart.sku.price
        
        context = {
            'carts': carts,
            'total': total,
            **kwargs,
        } 
        
        return TemplateResponse(
            request, 
            [self.template_name or 'baykeShop/cart.html'], 
            context
        )
    
    def post(self, request, *args, **kwargs):
        # 加入购物车的方法，返回Json数据
        sku_id = request.POST.get('sku_id')
        sales = request.POST.get('sales')
        total = BaykeShopingCart.get_cart_count(request.user)
        
        # 数据校验
        try:
            sku = BaykeShopSKU.objects.get(id=int(sku_id))
        except BaykeShopSKU.DoesNotExist:
            return JsonResponse({'code': 'error', 'message': '该商品不存在！'})
        if not sales.isdigit() or not int(sales) > 0:
            return JsonResponse({'code': 'error', 'message': '商品数量值不符合要求，请检查！'})
        
        # 加入购物车
        try:
            BaykeShopingCart.objects.create(sku=sku, num=int(sales), owner=request.user)
            # 购物车商品数量+1
            total += int(sales)
        except IntegrityError:
            # 这里处理重复加入购物车的问题
            BaykeShopingCart.objects.show().filter(sku=sku, owner=request.user).update(num=F('num')+int(sales))
        
        context = {
            'code': 'ok',
            'message': '加入购物车成功！',
            'sku_id': sku_id,
            'spu_id': sku.spu.id,
            'total': total,
            **kwargs,
        }
        return JsonResponse(context)
    
    def put(self, request, *args, **kwargs):
        data = QueryDict(request.body)
        cart_id = data.get('cart_id')
        sales = data.get('sales')
        actions = data.get('actions')
        cart = BaykeShopingCart.objects.show().filter(id=int(cart_id), owner=request.user)
        
        # 验证传入的购物车id
        if not cart.exists():
            return JsonResponse({'code': 'error', 'message': '购物车不存在！', **kwargs})
        
        # 如果购物车和数量都传入则修改数量
        if cart and sales and actions == 'update_num':
            cart.update(num=sales)
            return JsonResponse({'code': 'ok', 'message': '购物车数量修改成功！', **kwargs})
        
        # 删除购物车
        if cart and actions == 'delete':
            # cart.update(is_del=True)
            cart.delete()
            return JsonResponse({'code': 'ok', 'message': '删除成功！', **kwargs})
        

class BaykeShopOrderConfirmView(LoginRequiredMixin, View):
    """购物车订单确认页面
    """
    template_name = None
    
    def get(self, request, *args, **kwargs):
        
        addr_queryset = BaykeShopAddress.objects.show().filter(owner=request.user)
        addr_list = list(addr_queryset.values(
            'id', 'name', 'phone', 'email', 'province', 
            'city', 'county', 'address', 'is_default')
        )
        context = {'addr_list': addr_list, **kwargs}
        return TemplateResponse(
            request, 
            [self.template_name or 'baykeShop/order_confirm.html'], 
            context
        )
        
    def post(self, request, *args, **kwargs):
        # 确认订单信息生成订单
        # 并从购物车删除已生成订单的购物车信息
        
        data = request.POST
        address = json.loads(data.get('address'))
        carts = json.loads(data.get('carts'))
        mark = data.get('mark', '')
        
        BaykeShopOrderInfo.objects.create(
            owner=request.user,
            order_mark=mark,
        )
        print(request.POST)
        
        return JsonResponse({'code':'ok', 'message': '生成订单'})
    
    def get_total_price(self, request, cart_ids):
        BaykeShopingCart.objects.filter(
            owner=request.user,
            id__in=cart_ids
        ).aaggregate()