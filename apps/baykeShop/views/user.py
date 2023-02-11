#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@文件    :user.py
@说明    :用户的个人中心
@时间    :2023/02/10 11:02:26
@作者    :幸福关中&轻编程
@版本    :1.0
@微信    :baywanyun
'''

from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.template.response import TemplateResponse
from django.contrib.auth import get_user_model

from baykeShop.models import BaykeUserInfo, BaykeShopAddress
from baykeShop.forms import BaykeShopAddressForm

User = get_user_model()


class BaykeUserProfileView(LoginRequiredMixin, View):
    """用户信息管理
    """
    template_name = None
    
    def get(self, request, *args, **kwargs):
        
        
        context = {
            **kwargs,
        }
        
        return TemplateResponse(
            request, 
            [self.template_name or 'baykeShop/user/profile.html'],
            context
        )
    

class BaykeUserBalanceView(LoginRequiredMixin, View):
    """余额管理
    """
    
    template_name = None
    
    def get(self, request, *args, **kwargs):
        
        
        context = {
            **kwargs,
        }
        
        return TemplateResponse(
            request, 
            [self.template_name or 'baykeShop/user/balance.html'],
            context
        )
        

class BaykeAddressView(LoginRequiredMixin, View):
    
    """地址管理
    """
    
    template_name = None
    
    def get(self, request, *args, **kwargs):
        address_queryset = BaykeShopAddress.objects.show()
        
        context = {
            "addr_list": address_queryset,
            **kwargs,
        }
        
        return TemplateResponse(
            request, 
            [self.template_name or 'baykeShop/user/address.html'],
            context
        )
        
    def post(self, request, *args, **kwargs):
        form = BaykeShopAddressForm(request.POST)
        addr_default = BaykeShopAddress.objects.show().filter(is_default=True)
        if form.is_valid():
            if form.cleaned_data['is_default']:
                addr_default.update(is_default=False)
            new_addr = form.save(commit=False)
            new_addr.owner = request.user
            new_addr.save()
        return JsonResponse({'code': 'ok', 'message': '保存成功！'})
    
    def put(self, request, *args, **kwargs):
        from django.http import QueryDict
        data = QueryDict(request.body)
        addr_default = BaykeShopAddress.objects.show().filter(is_default=True)
        addr_default.update(is_default=False)
        BaykeShopAddress.objects.filter(id=int(data.get('addr_id'))).update(is_default=True)
        return JsonResponse({'code': 'ok', 'message': '设置默认成功！'})