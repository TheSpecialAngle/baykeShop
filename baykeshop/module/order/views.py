from django.views.generic import DetailView

from baykeshop.public.mixins import LoginRequiredMixin
from baykeshop.models import BaykeShopOrderInfo, BaykeShopOrderSKU


class BaykeShopOrderInfoDetailView(LoginRequiredMixin, DetailView):
    """ 订单详情页 """
    
    model = BaykeShopOrderInfo
    template_name = "baykeshop/order/order_detail.html"
    context_object_name = "order"
    slug_field="order_sn"
    
    def get_queryset(self):
        return super().get_queryset().filter(owner=self.request.user)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pay_methods'] = self.get_pay_methods()
        return context
    
    def get_pay_methods(self):
        pay_methods = BaykeShopOrderInfo.get_pay_method()
        pay_list = [
            { 
                'value': 1,
                'name': pay_methods[1],
                'icon': "/static/baykeshop/img/hdpay.svg",
                'is_default': False,
            },
            { 
                'value': 2,
                'name': pay_methods[2],
                'icon': "/static/baykeshop/img/alipay.svg",
                'is_default': True,
            },
            { 
                'value': 3,
                'name': pay_methods[3],
                'icon': "/static/baykeshop/img/wxpay.svg",
                'is_default': False,
            },
            { 
                'value': 4,
                'name': pay_methods[4],
                'icon': "/static/baykeshop/img/ye.svg",
                'is_default': False,
            }
        ]
        return pay_list