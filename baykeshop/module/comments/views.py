from django.contrib.contenttypes.models import ContentType
from django.http.response import HttpResponseRedirect
from django.urls import reverse


from baykeshop.models import BaykeShopSKU, BaykeShopOrderSKU

from baykeshop.module.order.views import BaykeShopOrderInfoDetailView
from baykeshop.module.comments.forms import BaykeOrderInfoCommentsModelForm


class BaykeOrderInfoCommentsFormView(BaykeShopOrderInfoDetailView):
    
    template_name = "baykeshop/comments/comments_form.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = BaykeOrderInfoCommentsModelForm()
        return context
    
    def post(self, request, *args, **kwargs):
        form = BaykeOrderInfoCommentsModelForm(request.POST)
        content_type = ContentType.objects.get_for_model(BaykeShopSKU)
        form.instance.content_type = content_type
        form.instance.owner = request.user
        if form.is_valid():
            form.save()
            oskus = BaykeShopOrderSKU.objects.filter(
                    order=self.get_object(), sku__id=form.cleaned_data['object_id']
                )
            oskus.update(is_commented=True)
            
        return HttpResponseRedirect(reverse("baykeshop:spu_detail", args=[oskus.sku.spu.id]))
    
    

    
    