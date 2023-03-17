from django.contrib.contenttypes.models import ContentType
from django.http.response import HttpResponseRedirect, Http404
from django.urls import reverse
from django.contrib import messages

from baykeshop.models import BaykeShopSKU, BaykeShopOrderSKU
from baykeshop.templatetags.shop_tags import commented_func
from baykeshop.module.order.views import BaykeShopOrderInfoDetailView
from baykeshop.module.comments.forms import BaykeOrderInfoCommentsModelForm


class BaykeOrderInfoCommentsFormView(BaykeShopOrderInfoDetailView):
    
    template_name = "baykeshop/comments/comments_form.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = BaykeOrderInfoCommentsModelForm()
        return context
    
    def post(self, request, *args, **kwargs):
        
        # 判断评论时机
        if self.get_object().pay_status != 4:
            raise Http404
        
        form = BaykeOrderInfoCommentsModelForm(request.POST)
        content_type = ContentType.objects.get_for_model(BaykeShopSKU)
        form.instance.content_type = content_type
        form.instance.owner = request.user
        if form.is_valid():
            form.save()
            # 修改评论标志
            oskus = BaykeShopOrderSKU.objects.filter(
                    order=self.get_object(), sku__id=form.cleaned_data['object_id']
                )
            oskus.update(is_commented=True)
            # 修改订单状态
            if commented_func(self.get_object()):
                obj = self.get_object()
                obj.pay_status = 5
                obj.save()
            messages.add_message(request, messages.SUCCESS, f'评价发表成功！')
        return HttpResponseRedirect(f'{reverse("baykeshop:spu_detail", args=[oskus.first().sku.spu.id])}?tabsActive=comment')
    
    