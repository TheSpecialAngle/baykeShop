#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@文件    :order.py
@说明    :
@时间    :2023/02/13 16:22:10
@作者    :幸福关中&轻编程
@版本    :1.0
@微信    :baywanyun
'''

import json
from django.db.models import F
from django.views.generic import View, ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.template.response import TemplateResponse
from django.contrib.auth import get_user_model
from django.utils import timezone

from baykeCore.common.mixin import LoginRequiredMixin
from baykeShop.models import (
    BaykeShopOrderInfo, BaykeUserInfo, BaykeUserBalanceLog,
    BaykeShopOrderSKUComment, BaykeShopOrderSKU
)


User = get_user_model()


class BaykeShopOrderPayView(LoginRequiredMixin, View):
    
    template_name = None
    
    def get(self, request, *args, **kwargs):
          
        order_id = request.GET.get('orderID', 0)
        code = ""
        error = None
        extra_context = {}
        try:
            order = BaykeShopOrderInfo.objects.get(id=int(order_id))
            extra_context = {
                "order_sn": order.order_sn,
                "total_amount": order.total_amount,
                "address": order.address,
                "name": order.name,
                "phone": order.phone,
                "desc": order.baykeshopordersku_set.first().desc,
                "paymethod": order.pay_method,
                "pay_time": order.pay_time
            }
        except BaykeShopOrderInfo.DoesNotExist:
            error = "该订单不存在，请先去挑选商品！"
            
        if order.pay_status != 1:
            code = "ok"
            error = "支付成功！"

        context = {
            "code": code,
            "error": error,
            **extra_context,
            **kwargs
        }
        
        return TemplateResponse(
            request, 
            [ self.template_name or 'baykeShop/order_pay.html'],
            context
        )

    def post(self, request, *args, **kwargs):
        data = request.POST
        paymethod = json.loads(data.get('paymethod'))
        order_sn = data.get('order_sn')
        orders = BaykeShopOrderInfo.objects.filter(order_sn=order_sn)
        userinfo = BaykeUserInfo.objects.filter(owner=request.user)
        # 余额支付
        if orders.exists() and userinfo.exists() and paymethod.get('value') == 4:
            order = orders.first()
            user = userinfo.first()
            if user.balance < order.total_amount:
                return JsonResponse({'code':'error', 'message': '余额不足！'})
            
            userinfo.update(balance=F('balance')-order.total_amount-order.freight)
            orders.update(pay_status=2, trade_sn=f"YE{order_sn}", pay_method=4, pay_time=timezone.now())
            BaykeUserBalanceLog.objects.create(
                owner=request.user, 
                amount=order.total_amount, 
                change_status=2,
                change_way=3
            )
            context = {"code": "ok", "message": "支付成功！"}
            return JsonResponse(context)
        else:
            return JsonResponse({'code':'error', 'message': '暂不支持该支付方式或支付信息有误！'})


class BaykeShopOrderListView(LoginRequiredMixin, ListView):
    # 个人中心订单列表页
    paginate_by = 10
    # paginate_orphans = 1
    template_name = "baykeShop/user/orderinfo.html"
    
    def get_queryset(self):
        queryset = BaykeShopOrderInfo.objects.filter(owner=self.request.user).order_by('-add_date')
        if self.request.GET.get('pay_status'):
            queryset = queryset.filter(pay_status=int(self.request.GET.get('pay_status')))
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['label'] = BaykeShopOrderInfo.get_tabs_label(self.request.GET.get('pay_status'))
        context['pay_satus'] = self.get_pay_satus()
        return context
    
    def get_pay_satus(self):
        if self.request.GET.get('pay_status'):
            return f"pay_status={self.request.GET.get('pay_status')}"
        

class BaykeShopOrderDetailView(LoginRequiredMixin, DetailView):
    # 订单详情页
    
    template_name = "baykeShop/user/order_detail.html"
    context_object_name = "order"
    
    def get_queryset(self):
        return BaykeShopOrderInfo.objects.filter(owner=self.request.user)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['label'] = BaykeShopOrderInfo.get_tabs_label(self.get_object().pay_status)
        return context
    
    def post(self, request, *args, **kwargs):
        data = request.POST
        order = self.get_object()
        # 确认收货逻辑
        if data.get('order_id') and data.get('ate') == 'ATE':
            order.pay_status = 4
            order.save()
            return JsonResponse({'code':'ok', 'message':'收货成功！'})
        
        # 订单评价逻辑
        if data.get('ordersku_id') and data.get('content'):
            order_sku = BaykeShopOrderSKU.objects.get(id=int(data.get('ordersku_id')))
            
            # 保存评论内容
            BaykeShopOrderSKUComment.objects.create(
                owner=request.user, 
                order_sku=order_sku,
                content=data.get('content'),
                comment_choices=int(data.get('comment_choices'))
            )
            # 修改评论标识
            order_sku.is_commented = True
            order_sku.save()
            
            # 判断订单所有商品是否都已评价
            commenteds = list(self.get_object().baykeshopordersku_set.values_list('is_commented', flat=True))
            # 更改订单的评价状态
            if len(commenteds) > 0 and all(commenteds):
                order.pay_status = 5
                order.save()
            return JsonResponse({'code':'ok', 'message':'评价成功！'})
        
        return JsonResponse({'code':'error', 'message':'发生错误！'})



class BaykeShopOrderCommentView(LoginRequiredMixin, DetailView):
    template_name = "baykeShop/user/order_detail_comment.html"
    context_object_name = "order"
    
    def get_queryset(self):
        return BaykeShopOrderInfo.objects.filter(owner=self.request.user)