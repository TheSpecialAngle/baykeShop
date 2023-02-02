from django.shortcuts import render
from django.views.generic import View

# Create your views here.
from baykeShop.models import BaykeShopSPU
from baykeShop.templatetags.shop_tags import category_queryset

class HomeView(View):
    
    def get(self, request, *args, **kwargs):
        category_qs = category_queryset(is_home=True)
        subcate_ids = category_qs.exclude(parent__isnull=True).values_list('id', flat=True)
        for cate in category_qs:
            if cate.parent is None:
                cate.goods = BaykeShopSPU.objects.filter(category__in=subcate_ids).distinct()[:10]
        return render(request, 'baykeShop/index.html', context={'category_goods': category_qs})
