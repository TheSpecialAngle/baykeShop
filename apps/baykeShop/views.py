from django.shortcuts import render, get_list_or_404
from django.views.generic import View

# Create your views here.
from baykeShop.models import BaykeShopSPU, BaykeShopCategory
from baykeShop.templatetags.shop_tags import category_queryset

class CategoryGoods:
    
    def category_goods(self, is_home=False, count=None):
        """
        is_home为True BaykeShopCategory仅查询is_home字段为True的值，否则查询全部
        """
        category_qs = category_queryset()
        if is_home is True:
            category_qs = category_queryset(is_home=True)
        subcate_ids = category_qs.exclude(parent__isnull=True).values_list('id', flat=True)
        for cate in category_qs:
            if cate.parent is None and count is None:
                cate.goods = BaykeShopSPU.objects.filter(category__in=subcate_ids).distinct()
            if cate.parent is None and count:
                cate.goods = BaykeShopSPU.objects.filter(category__in=subcate_ids).distinct()[:count]
        return category_qs
        
        
class HomeView(CategoryGoods, View):
    
    def get(self, request, *args, **kwargs):
        category_qs = self.category_goods(is_home=True, count=10)
        return render(request, 'baykeShop/index.html', context={'category_goods': category_qs})


class GoodsView(CategoryGoods, View):
    
    def get(self, request, cate_id, *args, **kwargs):
        category_qs = self.category_goods()
        try:
            category_parent_queryset = category_qs.filter(parent__id=cate_id)
            sub_cates = None
            if category_parent_queryset.exists():
                # 如果该值存在则说明传的是父级id
                sub_cates = category_parent_queryset
            cate = category_qs.get(id=cate_id)
        except BaykeShopCategory.DoesNotExist:
            pass
        context={
            'category': cate,
            'sub_cates': sub_cates,
            'cates': category_queryset, 
            'cate_id': cate_id, 
        }
        return render(request, 'baykeShop/goods.html', context)
