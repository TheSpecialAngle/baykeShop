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
import time
from django.db.models import F
from django.db.utils import IntegrityError
from django.views.generic import View
from django.http import JsonResponse
from django.template.response import TemplateResponse
from django.http import QueryDict
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()

from baykeshop.core.mixins import LoginRequiredMixin
from baykeshop.models import (
    BaykeShopSKU, BaykeShopingCart, BaykeShopAddress,
    BaykeShopOrderInfo, BaykeShopOrderSKU
)


class BaykeShopCartView(LoginRequiredMixin, View):
    """ 购物车 """
    
    template_name = None

    def get(self, request, *args, **kwargs):
        # 查询出当前用户的购物车商品
        cart_queryset = BaykeShopingCart.objects.filter(owner=request.user, sku__stock__gte=1)
        total = 0
        carts = []
        for cart in cart_queryset:
            cart_dict = {}
            cart_dict['id'] = cart.id
            cart_dict['title'] = cart.sku.spu.title
            cart_dict['sku_id'] = cart.sku.id
            cart_dict['cover_pic'] = cart.sku.cover_pic.url
            cart_dict['options'] = list(cart.sku.options.values('name', 'spec__name'))
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
            [self.template_name or 'baykeshop/cart.html'], 
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
        
        # 验证库存是否充足
        if int(sales) > sku.stock:
            return JsonResponse({'code': 'error', 'message': '库存不足！'})
        
        # 加入购物车
        try:
            BaykeShopingCart.objects.create(sku=sku, num=int(sales), owner=request.user)
            
        except IntegrityError:
            # 这里处理重复加入购物车的问题
            BaykeShopingCart.objects.filter(
                sku=sku, 
                owner=request.user
            ).update(num=F('num')+int(sales))
            
        # 购物车商品数量+1 
        total += int(sales)
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
        cart = BaykeShopingCart.objects.filter(id=int(cart_id), owner=request.user)
    
        
        # 验证传入的购物车id
        if not cart.exists():
            return JsonResponse({'code': 'error', 'message': '购物车不存在！', **kwargs})
        
        # 如果购物车和数量都传入则修改数量
        if cart and sales and actions == 'update_num':
            cart.update(num=sales)
            return JsonResponse({'code': 'ok', 'message': '购物车数量修改成功！', **kwargs})
        
        # 删除购物车
        if cart and actions == 'delete':
            cart.delete()
            return JsonResponse({'code': 'ok', 'message': '删除成功！', **kwargs})
        

class BaykeShopOrderConfirmView(LoginRequiredMixin, View):
    """ 购物车订单确认页面 """
    template_name = None
    
    def get(self, request, *args, **kwargs):
        
        addr_queryset = BaykeShopAddress.objects.filter(owner=request.user)
        addr_list = list(addr_queryset.values(
            'id', 'name', 'phone', 'email', 'province', 
            'city', 'county', 'address', 'is_default')
        )
        context = {'addr_list': addr_list, **kwargs}
        return TemplateResponse(
            request, 
            [self.template_name or 'baykeshop/order_confirm.html'], 
            context
        )
        
    def post(self, request, *args, **kwargs):
        # 确认订单信息生成订单
        # 并从购物车删除已生成订单的购物车信息
        
        data = request.POST
        address = json.loads(data.get('address'))
        carts = json.loads(data.get('carts'))
        mark = data.get('mark', '')

        if not address:
            return JsonResponse({'code':'error', 'message': '请先选择收货地址！'})
        
        # 生成订单
        orderinfo = BaykeShopOrderInfo.objects.create(
            owner=request.user,
            order_mark=mark,
            total_amount=self.get_total_price(carts),
            name=address.get('name'),
            phone=address.get('phone'),
            address=self.get_address(address),
            order_sn=self.generate_order_sn()
        )
        # 商品总价
        total_amount = 0
        for cart in carts:
            skus = BaykeShopSKU.objects.filter(id=int(cart.get('sku_id')))
            _carts = BaykeShopingCart.objects.filter(id=cart.get('id'))
            
            # 计算商品总价
            if cart.get('id') == 0:
                total_amount = skus.first().price
            else:
                total_amount += _carts.first().sku.price * int(cart.get('sales'))

            # 创建订单商品
            BaykeShopOrderSKU.objects.create(
                order=orderinfo,
                sku=skus.first(),
                title=cart.get('title'),
                spec=self._get_sku_options(cart.get('options')),
                desc=f"{cart.get('title')} {self._get_sku_options(cart.get('options'))}",
                content=skus.first().spu.content,
                count=int(cart.get('sales')),
                price=skus.first().price
            )
            
            # 减库存加销量
            skus.update(
                stock=F('stock')-int(cart.get('sales')), 
                sales=F('sales')+int(cart.get('sales'))
            )

            # 判断是否为购物车生成订单，则清理购物车
            if int(cart.get('id')) != 0:
                # 订单商品创建成功后，清理购物车
                _carts.delete()
            
        return JsonResponse({
            'code':'ok', 
            'message': '生成订单成功！', 
            'redirect': reverse('baykeshop:order_pay'),
            'order_id': orderinfo.id
        })
    
    def get_address(self, address):
        # 详细地址
        return f"""
            {address.get('province')}
            {address.get('city')}
            {address.get('county')}
            {address.get('address')}
        """.replace(" ", "")
    
    def generate_order_sn(self):
        # 当前时间 + userid + 随机数
        from random import Random
        random_ins = Random()
        order_sn = "{time_str}{user_id}{ranstr}".format(
            time_str = time.strftime("%Y%m%d%H%M%S"),
            user_id = self.request.user.id,
            ranstr = random_ins.randint(10, 99))
        return order_sn
    
    def _get_sku_options(self, options):
        ops = []
        for op in options:
            if isinstance(op, dict):
                ops.append("{}:{}".format(op.get('spec__name'), op.get('name')))
            else:
                ops.append(op)
        return ','.join(ops)
    
    def get_total_price(self, carts):
        # 商品总价
        total_amount = 0
        # 商品详情页点击立即购买跳转过来数据
        if carts[0].get('id') == 0:
            total_amount = BaykeShopSKU.objects.filter(id=int(carts[0].get('sku_id'))).first().price
        else:
            for cart in carts:
                total_amount += BaykeShopingCart.objects.get(
                    id=cart.get('id')
                ).sku.price * int(cart.get('sales'))
        return total_amount