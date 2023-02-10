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

from baykeShop.models import BaykeUserInfo

User = get_user_model()


class BaykeUserProfileView(LoginRequiredMixin, View):
    
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