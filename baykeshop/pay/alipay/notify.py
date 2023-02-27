from django.views.generic import View
from django.template.response import TemplateResponse
from django.http.response import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.utils import timezone

from baykeshop.pay.alipay.pay import alipay
from baykeshop.core.mixins import LoginRequiredMixin
from baykeshop.models import BaykeShopOrderInfo


class AlipayNotifyView(LoginRequiredMixin, View):
    
    template_name = None
    
    def get(self, request, extra_context=None):
        datas = request.GET.dict()
        signature = datas.pop("sign")
        success = alipay.verify(datas, signature)
        if success:
            order_sn = datas.get('out_trade_no')
            trade_no = datas.get('trade_no')
            # trade_status = datas.get('trade_status')
            order = BaykeShopOrderInfo.objects.filter(order_sn=order_sn)
            order.update(
                pay_status=2, 
                trade_sn=trade_no, 
                pay_time=timezone.now(),
                pay_method=2
            )
            return HttpResponseRedirect(f'{reverse("baykeshop:order_pay")}?orderID={order.first().id}')
        context = {**(extra_context or {})}
        return HttpResponse("发生错误，请联系管理员查看！")
        
    def post(self, request, *args, **kwargs):
        datas = request.POST.dict()
        signature = datas.pop("sign")
        success = alipay.verify(datas, signature)
        if success:
            order_sn = datas.get('out_trade_no')
            trade_no = datas.get('trade_no')
            # trade_status = datas.get('trade_status')
            order = BaykeShopOrderInfo.objects.filter(order_sn=order_sn)
            order.update(
                pay_status=2, 
                trade_sn=trade_no, 
                pay_time=timezone.now(),
                pay_method=2
            )
        return HttpResponse('success')