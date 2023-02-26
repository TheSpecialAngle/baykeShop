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
        
        datas = request.GET
        signature = datas.pop("sign")
        success = alipay.verify(datas, signature)
        
        if not success:
            print("支付信息未验证通过")
            return
        
        if success:
            order_sn = datas.get('out_trade_no')
            trade_no = datas.get('trade_no')
            trade_status = datas.get('trade_status')
            orderID=datas.get('orderID')
            BaykeShopOrderInfo.objects.filter(id=orderID).update(
                pay_status=2, trade_sn=trade_no, pay_time=timezone.now(),
                pay_method=2
            )
            
        context = {
            
            **(extra_context or {})
        }
        
        return HttpResponseRedirect(f'{reverse("baykeshop:order_pay")}?orderID={orderID}')
        # return TemplateResponse(request, [self.template_name or "baykeshop/alipay_notify.html"], context)
    
    def post(self, request, *args, **kwargs):
        return HttpResponse('success')