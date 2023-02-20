#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@文件    :home.py
@说明    :商城首页相关公开视图
@时间    :2023/02/19 18:23:59
@作者    :幸福关中&轻编程
@版本    :1.0
@微信    :baywanyun
'''


from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.views.generic import View, DetailView, ListView
from django.views.generic.detail import SingleObjectMixin
from django.template.response import TemplateResponse

# Create your views here.
from baykeshop.models import (
    BaykeShopSPU, BaykeShopCategory, BaykeShopSKU,
    BaykeShopSpecOption
)

from baykeshop.forms.filter import ProductFilterForm

        
class HomeView(View):
    # 首页视图
    goods_count = 10
    template_name = None
    
    def get(self, request, *args, **kwargs):
        category_qs = BaykeShopCategory.objects.filter(parent__isnull=True, is_home=True)
        for cate in category_qs:
            sub_cates = BaykeShopCategory.objects.filter(parent=cate).values_list('id', flat=True)
            cate.goods = BaykeShopSKU.objects.filter(
                spu__category__id__in=list(sub_cates)).order_by('-add_date').distinct()[:self.goods_count]
        context = {'category_goods': category_qs, **kwargs}
        return TemplateResponse(request, [self.template_name or 'baykeshop/index.html'], context)


class GoodsListView(SingleObjectMixin, ListView):
    # 商品列表页
    paginate_by = 24
    paginate_orphans = 4
    template_name = "baykeshop/goods.html"
    
    def get(self, request, *args, **kwargs):
        self.form = ProductFilterForm(request.GET)
        self.object = self.get_object(queryset=BaykeShopCategory.objects.all())
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.object
        context['parent_cates'] = self.get_category()
        context['sub_cates'] = self.get_category(self.object)
        context['form'] = self.form
        context['order'] = self.request.GET.get('order' )
        context['field'] = self.request.GET.get('field')
        return context

    def get_queryset(self):
        category = self.object
        queryset = BaykeShopSKU.objects.filter(spu__category=category).order_by('-add_date').distinct()
        if category.parent is None:
            sub_cates = category.baykeshopcategory_set.values_list('id', flat=True)
            queryset = BaykeShopSKU.objects.filter(
                spu__category__id__in=sub_cates).order_by('-add_date').distinct()
        # 筛选
        if self.form.is_valid():
            field = self.form.cleaned_data['field']
            order = self.form.cleaned_data['order']
            field_name = f'-{field}' if order == 'asc' else f'{field}'
            queryset = queryset.order_by(f"{field_name}").distinct() 
        return queryset
    
    def get_category(self, obj=None):
        """获取分类信息
            obj为当前分类对象
            - 如果为None则返回一级分类
            - 如果传入对象父级不存在则返回所有的下级
            - 如果传入对象父级存在则返回该父级所有的下级
        """
        cates = BaykeShopCategory.objects.filter(parent__isnull=True)
        if obj is not None and obj.parent is None:
            cates = obj.baykeshopcategory_set.all()
        elif obj is not None and obj.parent:
            cates = BaykeShopCategory.objects.filter(parent=obj.parent)
        return cates
        
        
class GoodDetailView(DetailView):
    """ 商品详情页 """
    template_name = "baykeshop/detail.html"
    queryset = BaykeShopSPU.objects.all()
    context_object_name = "good"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['options_skus'], context['specs'] = self.get_options_skus()
        context['current_sku_options'] = self.get_current_sku_options()
        context['banners'] = self.get_spu_banners()
        context['sku'] = self.get_current_sku()
        context['sku_id'] = self.kwargs.get('sku_id')
        return context
    
    def get_sku_queryset(self):
        # 当前spu下的sku queryset数据
        good = self.get_object()
        skus_queryset = good.baykeshopsku_set.all()
        return skus_queryset
    
    def get_current_sku(self):
        # spu进入后显示的sku
        sku = get_object_or_404(BaykeShopSKU, pk=self.kwargs.get('sku_id'))
        return sku
    
    def get_current_sku_options(self):
        # 对应的sku规格
        current_sku = self.get_current_sku()
        current_sku_options = list(current_sku.options.values_list('name', flat=True))
        return current_sku_options  
    
    def get_options_skus(self):
        specs = []
        skus = {}
        skus_queryset = self.get_sku_queryset()
    
        for sku in skus_queryset:
            sku_options = sku.options.all()
            sku_options_names = sku_options.values_list('name', flat=True)
            options = ','.join(sku_options_names)
            skus[options] = {
                'sku_id': sku.id,
                'price': str(sku.price),
                'org_price': str(sku.org_price),
                'stock': sku.stock,
                'sales': sku.sales,
                'cover_pic': sku.cover_pic.path
            }
            # 返回当前spu下的specs
            for op in sku_options:
                spec_dict = {
                    'spec': op.spec.name, 
                    'options': list(
                        BaykeShopSpecOption.objects.filter(
                            spec=op.spec
                            ).values_list('name', flat=True)
                        )
                }
                # 防止重复加入 
                if spec_dict not in specs:
                    specs.append(spec_dict)
        return skus, specs
    
    def get_spu_banners(self):
        # 商品轮播图
        spu = self.get_object()
        banners_queryset = spu.baykespucarousel_set.all()
        banners = banners_queryset.values(
            'img', 'target_url', 'desc'
        )
        if not banners_queryset:
            banners = [{'img': str(spu.cover_pic), 'desc': spu.title}]
        return list(banners)


class SearchView(ListView):
    """ 搜索功能 """ 
    paginate_by = 24
    paginate_orphans = 4
    template_name = "baykeshop/search.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['words'] = self.request.GET.get('words')
        return context
    
    def get_queryset(self):
        queryset = BaykeShopSKU.objects.all()
        words = self.request.GET.get('words')
        if words:
            queryset = queryset.filter(
                Q(spu__title__icontains=f'{words}')|
                Q(spu__desc__icontains=f'{words}')|
                Q(spu__content__icontains=f'{words}')
            ).order_by('-add_date')
        return queryset