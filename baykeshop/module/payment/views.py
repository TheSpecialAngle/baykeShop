from django.views.generic import TemplateView

from baykeshop.public.mixins import LoginRequiredMixin
from baykeshop.models import BaykeShopingCart, BaykeShopSKU, BaykeShopAddress


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
        freight = 0
        if cleaned_data and cleaned_data.get('cartsID'):
            carts_ids = [int(id) for id in cleaned_data.get('cartsID').split(',')]
            carts = BaykeShopingCart.objects.filter(id__in=carts_ids)
            for cart in carts:
                cart.total_price = cart.sku.price * cart.num
                # 粗略计算运费, 运费为固定，仅与sku有关
                cart.freight = 0
                cart.freight += cart.sku.spu.freight
        elif cleaned_data and cleaned_data.get('skuID'):
            carts = BaykeShopSKU.objects.filter(id=int(cleaned_data.get('skuID')))
            for cart in carts:
                cart.num = int(cleaned_data.get('num'))
                cart.total_price = cart.price * cart.num
                # 粗略计算运费
                cart.freight = cart.spu.freight
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
        