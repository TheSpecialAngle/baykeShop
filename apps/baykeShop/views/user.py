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

from django.http import JsonResponse
from django.template.response import TemplateResponse
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password, make_password
from django.db.models import Sum
from baykeCore.common.mixin import LoginRequiredMixin
from baykeShop.models import BaykeShopAddress, BaykeUserInfo, BaykeUserBalanceLog
from baykeShop.forms import BaykeShopAddressForm, BaykeUserInfoForm

User = get_user_model()


class BaykeUserInfoView(LoginRequiredMixin, View):
    
    template_name = None
    
    def get(self, request, *args, **kwargs):
        
        context = { **kwargs,}
        
        return TemplateResponse(
            request, 
            [self.template_name or 'baykeShop/user/profile.html'],
            context
        )

    def post(self, request, *args, **kwargs):
        # 查询如果不存在就创建的快捷方式
        obj, created = BaykeUserInfo.objects.get_or_create(
            owner=request.user,
            defaults={'owner': request.user},
        )
        
        form = BaykeUserInfoForm(request.POST, request.FILES, instance=obj)
        if form.is_valid():
            form.save()
            return JsonResponse({'code': 'ok', 'message': 'success'})
        else:
            return JsonResponse({'code': 'error', 'message': '手机号必须唯一！'})


    def put(self, request, *args, **kwargs):
        from django.http import QueryDict
        data = QueryDict(request.body)
        if not data:
            return JsonResponse({'code': 'error', 'message': '不能为空！'})
        
        if not check_password(data.get('old_password'), request.user.password):
            return JsonResponse({'code':'error', 'message': '您输入的旧密码有误！'})
        
        if data.get('password1') != data.get('password2'):
            return JsonResponse({'code':'error', 'message': '两次密码输入不一致！'})
        
        user = request.user
        user.password = make_password(data.get('password2'))
        user.save()
        
        return JsonResponse({'code':'ok', 'message': '密码修改成功！'})


class BaykeUserBalanceView(LoginRequiredMixin, View):
    """余额管理
    """
    
    template_name = None
    
    def get(self, request, *args, **kwargs):
        
        balancelogs = BaykeUserBalanceLog.objects.filter(owner=request.user)
        minus_balancelogs = balancelogs.filter(change_status=2)
        add_balancelogs = balancelogs.filter(change_status=1)
        
        # amount_add = add_balancelogs.aggregate(Sum('amount'))
        amount_minus = minus_balancelogs.aggregate(Sum('amount'))
        
        context = {
            'balancelogs': balancelogs,
            'minus_balancelogs': minus_balancelogs,
            'add_balancelogs': add_balancelogs,
            'amount_add': request.user.baykeuserinfo.balance + self.get_amount_minus(amount_minus),
            'amount_minus': round(self.get_amount_minus(amount_minus), 2),
            **kwargs,
        }
        
        return TemplateResponse(
            request, 
            [self.template_name or 'baykeShop/user/balance.html'],
            context
        )
    
    def get_amount_add(self, amount_add):
        if amount_add["amount__sum"]:
            return amount_add["amount__sum"]
        else:
            return 0
    
    def get_amount_minus(self, amount_minus):
        if amount_minus["amount__sum"]:
            return amount_minus["amount__sum"]
        else:
            return 0
        

class BaykeAddressView(LoginRequiredMixin, View):
    
    """地址管理
    """
    
    template_name = None
    
    def get(self, request, *args, **kwargs):
        address_queryset = BaykeShopAddress.objects.show().filter(owner=request.user)
        addr_id = request.GET.get('addr_id')
        
        # 点击修改按钮时返回数据回填表单  
        if addr_id:
            addr_list = BaykeShopAddress.objects.show().filter(
                id=int(addr_id), owner=request.user).values(
                'id', 'name', 'phone', 'email', 'province',
                'city', 'county','address','is_default'
            )
            addr_json = dict(addr_list.first())
            return JsonResponse({'code':'ok', 'message': '获取成功', 'formProps':addr_json})
        
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
        addr_default = BaykeShopAddress.objects.show().filter(
            is_default=True, owner=request.user
        )
        addr_id = request.POST.get('addr_id', None)
        
        # 新增
        if form.is_valid() and (not addr_id):
            if form.cleaned_data['is_default']:
                addr_default.update(is_default=False, owner=request.user)
            new_addr = form.save(commit=False)
            new_addr.owner = request.user
            new_addr.save()
            return JsonResponse({'code': 'ok', 'message': '保存成功！'})
        
        # 修改  
        if form.is_valid() and addr_id:
            if form.cleaned_data['is_default']:
                addr_default.update(is_default=False)
            BaykeShopAddress.objects.show().filter(
                    id=int(addr_id), 
                    owner=request.user
                ).update(**form.cleaned_data)
            return JsonResponse({'code':'ok', 'message': '修改成功'})
        
        return JsonResponse({'code': 'error', 'message': '发生错误！'})  
    
    def put(self, request, *args, **kwargs):
        from django.http import QueryDict
        data = QueryDict(request.body)
        addr_default = BaykeShopAddress.objects.show().filter(is_default=True, owner=request.user)
        addr_default.update(is_default=False)
        BaykeShopAddress.objects.filter(id=int(data.get('addr_id')), owner=request.user).update(is_default=True)
        return JsonResponse({'code': 'ok', 'message': '设置默认成功！'})
    
    def delete(self, request, *args, **kwargs):
        # 删除
        from django.http import QueryDict
        data = QueryDict(request.body)
        addr_id = data.get('addr_id')
        BaykeShopAddress.objects.filter(id=int(addr_id), owner=request.user).delete()
        return JsonResponse({'code': 'ok', 'message': '删除成功！'})