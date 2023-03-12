from django.views.generic import TemplateView

from baykeshop.public.mixins import LoginRequiredMixin
from baykeshop.models import BaykeShopingCart, BaykeShopSKU, BaykeShopAddress


class CashRegisterTemplateView(LoginRequiredMixin, TemplateView):
    """ 收银台 """
    template_name = "baykeshop/payment/cash_register.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['carts'] = self.get_carts()
        return context
    
    def get_carts(self):
        cleaned_data = self.request.GET.dict()
        carts = []
        if cleaned_data and cleaned_data.get('cartsID'):
            carts_ids = [int(id) for id in cleaned_data.get('cartsID').split(',')]
            carts = BaykeShopingCart.objects.filter(id__in=carts_ids)
        elif cleaned_data and cleaned_data.get('skuID'):
            carts = BaykeShopSKU.objects.filter(id=int(cleaned_data.get('skuID')))
            for cart in carts:
                cart.num = int(cleaned_data.get('num'))
        return carts
    
