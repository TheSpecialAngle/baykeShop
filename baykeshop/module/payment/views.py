from django.views.generic import TemplateView
from django.urls import reverse
from django.core.cache import cache
from django.db.models import F

from baykeshop.public.mixins import LoginRequiredMixin, JsonResponse
from baykeshop.models import (
    BaykeShopingCart, BaykeShopSKU, BaykeShopOrderInfo, 
    BaykeShopAddress, BaykeShopOrderSKU
)


class CashRegisterTemplateView(LoginRequiredMixin, TemplateView):
    """ 收银台 """
    template_name = "baykeshop/payment/cash_register.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['carts'] = self.get_carts()
        if context['carts']:
            context['count'] = self.get_count(context['carts'])
            context['total'] = self.get_total(context['carts'])
            context['freight'] = self.get_freight(context['carts'])
            context['pay_total'] = self.get_pay_total(context['carts'])
        return context
    
    def get_carts(self):
        cleaned_data = self.request.GET.dict()
        carts = []
        if cleaned_data and cleaned_data.get('cartsID'):
            carts_ids = [int(id) for id in cleaned_data.get('cartsID').split(',')]
            carts = BaykeShopingCart.objects.filter(id__in=carts_ids)
            for cart in carts:
                cart.type = 'cart'
                cart.total_price = cart.sku.price * cart.num
                # 粗略计算运费, 运费为固定，仅与sku有关
                cart.freight = 0
                cart.freight += cart.sku.spu.freight
        elif cleaned_data and cleaned_data.get('skuID'):
            carts = BaykeShopSKU.objects.filter(id=int(cleaned_data.get('skuID')))
            for cart in carts:
                cart.type = 'sku'
                cart.num = int(cleaned_data.get('num'))
                cart.total_price = cart.price * cart.num
                # 粗略计算运费
                cart.freight = cart.spu.freight
        # 缓存订单信息        
        cache.set('carts', carts, None)
        return carts
    
    def get_count(self, carts):
        # 商品总数
        cleaned_data = self.request.GET.dict()
        count = 0
        if cleaned_data and cleaned_data.get('skuID'):
            count = int(cleaned_data.get('num'))
        elif cleaned_data and cleaned_data.get('cartsID'):
            from django.db.models import Sum
            count = carts.aggregate(Sum('num'))['num__sum']
        return count
        
    def get_total(self, carts):
        # 获取商品总价，不含运费
        total = 0
        for cart in carts:
            total += cart.total_price
        return total
            
    def get_freight(self, carts):
        # 获取运费
        freight = 0
        for cart in carts:
            freight += cart.freight
        return freight
    
    def get_pay_total(self, carts):
        # 实际支付金额，含运费
        return self.get_total(carts) + self.get_freight(carts)
    
    def generate_order_sn(self):
        # 当前时间 + userid + 随机数
        import time
        from random import Random
        random_ins = Random()
        order_sn = "{time_str}{user_id}{ranstr}".format(
            time_str = time.strftime("%Y%m%d%H%M%S"),
            user_id = self.request.user.id,
            ranstr = random_ins.randint(10, 99))
        return order_sn
    
    def post(self, request, *args, **kwargs):
        cleaned_data = request.POST.dict()
        addr = BaykeShopAddress.objects.get(id=int(cleaned_data['addr_id']))
        carts = cache.get('carts')
        
        if not carts:
            return JsonResponse({'code': 'err', 'message': '订单过期，请刷新重试！'})
        
        datas = {
            "owner": request.user,
            "order_sn": self.generate_order_sn(),
            "pay_status": 1,
            "total_amount": self.get_pay_total(carts),
            "order_mark": cleaned_data.get('order_mark', ''),
            "name": addr.name,
            "phone": addr.phone,
            "email": addr.email,
            "address": f"{addr.province}{addr.city}{addr.county}{addr.address}"
        }
        # 创建订单
        orderinfo = BaykeShopOrderInfo.objects.create(**datas)
        
        # 创建订单商品
        for cart in carts:
            # 订单商品保存
            sku = cart if cart.type == 'sku' else cart.sku
            spec = ','.join([f"{op.spec.name}:{op.name}" for op in sku.options.all() if op])
            BaykeShopOrderSKU.objects.create(
                order=orderinfo, sku=sku, title=sku.spu.title,
                desc=sku.spu.desc, spec=spec, content=sku.spu.content,
                count=cart.num, price=sku.price
            )
            
            # 加销量 减库存
            BaykeShopSKU.objects.filter(id=sku.id).update(
                stock=F('stock')-int(cart.num), 
                sales=F('sales')+int(cart.num)
            )
            
            # 清理购物车
            if cart.type == 'cart':
                cart.delete()
            
            # 清理缓存
            cache.delete('carts')
                
        pay_url = reverse("baykeshop:order_detail", args=[orderinfo.order_sn])
        return JsonResponse({'code': 'ok', 'message': 'ok', 'pay_url': pay_url})