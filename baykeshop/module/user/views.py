from django.views.generic import FormView, CreateView, TemplateView, ListView
from django.contrib.auth import login
from django.contrib.auth import authenticate
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.views import (
    LoginView as BaseLoginView,
    LogoutView as BaseLogoutView
)

from baykeshop.config.settings import bayke_settings
from baykeshop.module.user.forms import LoginForm, RegisterForm
from baykeshop.models import BaykeUserInfo, BaykeShopAddress, BaykeUserBalanceLog
from baykeshop.public.mixins import JsonLoginRequiredMixin, JsonableResponseMixin, LoginRequiredMixin, JsonResponse



class LoginView(SuccessMessageMixin, BaseLoginView):
    """ 登录 """
    next_page = bayke_settings.NEXT_PAGE
    form_class = LoginForm
    redirect_field_name = 'redirect_to'
    template_name = "baykeshop/user/login.html"
    success_message = "%(username)s 登录成功！"

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(
            cleaned_data,
            username=cleaned_data['username'],
        )
        

class LogoutView(BaseLogoutView):
    """ 登出 """
    template_name = 'baykeshop/user/logout.html'
    

class RegisterView(SuccessMessageMixin, FormView):
    """ 注册用户 """
    template_name = 'baykeshop/user/register.html'
    form_class = RegisterForm
    success_url = reverse_lazy("baykeshop:home")
    success_message = "%(username)s 注册成功，已登录！"
    
    def form_valid(self, form):
        if form.is_valid():
            new_user = form.save()
            auth_user = authenticate(username=new_user.username, 
                                     password=form.cleaned_data['password1'])
            BaykeUserInfo.objects.create(owner=auth_user, nickname=auth_user.username)
            login(self.request, auth_user)
        return super().form_valid(form)

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(
            cleaned_data,
            username=cleaned_data['username'],
        )
        

class BaykeShopAddressCreateView(JsonLoginRequiredMixin, JsonableResponseMixin, CreateView):
    """ 添加地址 """
    model = BaykeShopAddress
    fields = ['name', 'phone', 'email', 'province', 'city', 'county', 'address', 'is_default']
    success_url = reverse_lazy('baykeshop:carts')
    
    def form_valid(self, form):
        form.instance.owner = self.request.user
        
        # 修改
        if self.request.POST.get('id') and self.request.POST.get('id').isdigit():
            # 查找默认的
            addr_default = BaykeShopAddress.objects.filter(owner=self.request.user, is_default=True)
            # 修改
            addr = BaykeShopAddress.objects.filter(id=int(self.request.POST.get('id')))
            addr.update(**form.cleaned_data)
            # 处理默认只能有一个
            if form.cleaned_data['is_default']:
                addr_default.exclude(id=addr.first().id).update(is_default=False)
            return JsonResponse({'code':'ok', 'message': '修改成功！'})
        
        # 新增 
        if form.cleaned_data['is_default']:
            BaykeShopAddress.objects.filter(owner=self.request.user, is_default=True).update(is_default=False)
        return super().form_valid(form)
    

class BaykeUserInfoTemplateView(LoginRequiredMixin, TemplateView):
    """ 个人中心 """
    
    template_name = "baykeshop/user/userinfo.html"
    
    
class BaykeUserBalanceLogTemplateView(LoginRequiredMixin, TemplateView):
    """ 余额记录 """
    template_name = "baykeshop/user/balance.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['qs'] = self.get_queryset()
        context['minus_balance'] = self.get_minus_balance()
        context['add_balance'] = self.get_add_balance()
        context['amount_minus'] = round((self.get_amount_minus()['amount__sum'] or 0), 2)
        context['amount_add'] = round(self.get_amount_add(), 2)
        return context
    
    def get_queryset(self):
        return BaykeUserBalanceLog.objects.filter(owner=self.request.user)
    
    def get_minus_balance(self):
        return self.get_queryset().filter(change_status=2)
    
    def get_add_balance(self):
        return self.get_queryset().filter(change_status=1)
    
    def get_amount_minus(self):
        # 累计支出
        from django.db.models import Sum 
        return self.get_queryset().aggregate(Sum('amount'))
    
    def get_amount_add(self):
        # 累计充值
        try:
            amount_add = self.request.user.baykeuserinfo.balance + (self.get_amount_minus()['amount__sum'] or 0)
        except BaykeUserInfo.DoesNotExist:
            BaykeUserInfo.objects.create(owner=self.request.user)
            amount_add = self.request.user.baykeuserinfo.balance + (self.get_amount_minus()['amount__sum'] or 0)
        return amount_add
    

class BaykeShopAddressListView(LoginRequiredMixin, ListView):
    
    model = BaykeShopAddress
    template_name = "baykeshop/user/addr_list.html"
    context_object_name = "address_list"
    
    def get_queryset(self):
        return list(super().get_queryset().filter(owner=self.request.user).values(
            'id', 'name', 'phone', 'email', 'province', 'city', 'county', 'address', 'is_default'))
    
    def post(self, request, *args, **kwargs):
        code = ''
        message = ''
        addr_id = request.POST.get('addr_id')
        if addr_id:
            addr = BaykeShopAddress.objects.filter(id=int(addr_id))
            if addr.exists():
                addr.delete()     
                code = 'ok'
                message = '删除成功!'
            else:
                code = 'err'
                message = '该地址不存在！'
        else:
            code = 'err'
            message = '未传入有效参数！'
        return JsonResponse({'code': code, 'message': message})
    
    