from django.db.models import F
from django.db.utils import IntegrityError
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.template.response import TemplateResponse
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model

User = get_user_model()

from ..models import BaykeShopSKU, BaykeShopingCart


class BaykeShopCartView(LoginRequiredMixin, View):
    
    login_url = reverse_lazy('baykeShop:login')
    redirect_field_name = 'redirect_to'
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
            total += 1
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
        from django.http import QueryDict
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
        
        context = {
            **kwargs
        }
        return TemplateResponse(
            request, 
            [self.template_name or 'baykeShop/order_confirm.html'], 
            context
        )