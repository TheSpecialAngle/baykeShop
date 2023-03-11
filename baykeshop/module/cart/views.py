from django.views.generic import CreateView
from django.db.models import F
from django.db.utils import IntegrityError
from django.contrib import messages
from django.urls import reverse_lazy
from baykeshop.models import BaykeShopingCart, BaykeShopAddress
from baykeshop.public.mixins import JsonableResponseMixin, JsonLoginRequiredMixin, JsonResponse


class BaykeShopingCartCreateView(JsonLoginRequiredMixin, JsonableResponseMixin, CreateView):
    """ 加入购物车 """
    model = BaykeShopingCart
    fields = ['sku', 'num']
    success_url = reverse_lazy('baykeshop:add_cart')
    
    def form_valid(self, form):
        form.instance.owner = self.request.user
        try:
            self.object = form.save()
            messages.add_message(self.request, messages.SUCCESS, f'已成功加入购物车！')
        except IntegrityError:
            carts = BaykeShopingCart.objects.filter(owner=self.request.user, sku=form.cleaned_data['sku'])
            carts.update(num=F('num')+int(form.cleaned_data['num']))
            self.object = carts.first()
            messages.add_message(self.request, messages.SUCCESS, f'已成功加入购物车！')
            return JsonResponse({'pk': self.object.id, 'code': 'ok', 'message': '已成功加入购物车！'}, json_dumps_params={'ensure_ascii': False})
        return super().form_valid(form)