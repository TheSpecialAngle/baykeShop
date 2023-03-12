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