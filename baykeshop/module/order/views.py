from django.http.response import HttpResponseRedirect
from django.views.generic import ListView, DetailView
from django.contrib import messages


from baykeshop.config.settings import bayke_settings
from baykeshop.public.mixins import LoginRequiredMixin
from baykeshop.models import BaykeShopOrderInfo


class BaykeshopOrderInfoListView(LoginRequiredMixin, ListView):
    """ 订单列表 """
    model = BaykeShopOrderInfo
    template_name = "baykeshop/order/order_list.html"
    context_object_name = "order_list"
    paginate_by = bayke_settings.USER_ORDERINFO_PAGINATE_BY
    paginate_orphans = 2
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['status'] = self.request.GET.get('status') if self.request.GET.get('status') else ''
        return context
    
    def get_queryset(self):
        queryset = super().get_queryset().order_by('-add_date').filter(owner=self.request.user)
        cleaned_data = self.request.GET.dict()
        if cleaned_data and (cleaned_data.get('status') in ['1', '2', '3', '4', '5', '6']):
            queryset = queryset.filter(pay_status=int(cleaned_data['status']))
        return queryset

    def post(self, request, *args, **kwargs):
        orders = BaykeShopOrderInfo.objects.filter(owner=request.user, order_sn=request.POST['order_sn'])
        orders.update(pay_status=4)
        messages.add_message(request, messages.SUCCESS, f'订单{orders.first()}已确认收货！')
        return HttpResponseRedirect(f"{request.path}?status=4")
    

class BaykeShopOrderInfoDetailView(LoginRequiredMixin, DetailView):
    """ 订单结算支付 """
    
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
    

class BaykeShopOrderInfoUserDetailView(BaykeShopOrderInfoDetailView):
    
    template_name = "baykeshop/order/user_order_detail.html"
