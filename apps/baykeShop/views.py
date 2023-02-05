from django.shortcuts import render
from django.views.generic import View, DetailView, ListView
from django.views.generic.detail import SingleObjectMixin

# Create your views here.
from baykeShop.models import (
    BaykeShopSPU, BaykeShopCategory, BaykeShopSKU, BaykeShopSpecOption,
    BaykeShopSpec
)
from .forms import OrderSPUForm

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
    # 商品列表页
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
        
        # 分类下的商品数据
        goods_queryset = self.cate_goods(cate)
        
        # 结果排序
        order = self.request.GET.get('order')
        field = self.request.GET.get('field')
        
        if order == 'esc' and field:
            goods_queryset = goods_queryset.order_by(f'-baykeshopsku__{field}')
        elif order == 'asc' and field:
            goods_queryset = goods_queryset.order_by(f'baykeshopsku__{field}')
            
        context={
            'category': cate,
            'goods_queryset': goods_queryset,
            'sub_cates': sub_cates,
            'cates': category_queryset, 
            'cate_id': cate_id, 
            'order': order,
            'field': field
        }
        return render(request, 'baykeShop/goods.html', context)

    def cate_goods(self, cate):
        """按分类筛选商品数据
        cate 商品分类对象
        """ 
        goods_queryset = BaykeShopSPU.objects.show().filter(category=cate).order_by('-pub_date')
        if cate.parent is None:
            subcate_ids = cate.baykeshopcategory_set.show().values_list('id', flat=True)
            goods_queryset = BaykeShopSPU.objects.show().filter(
                category__id__in=list(subcate_ids)
            ).order_by('-pub_date').distinct()
        return goods_queryset


class GoodsListView(SingleObjectMixin, ListView):
    
    paginate_by = 24
    paginate_orphans = 4
    template_name = "baykeShop/category_spus.html"
    
    def get(self, request, *args, **kwargs):
        self.form = OrderSPUForm(request.GET)
        self.object = self.get_object(queryset=BaykeShopCategory.objects.show())
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
        queryset = category.baykeshopspu_set.order_by('-add_date').distinct()
        if category.parent is None:
            sub_cates = category.baykeshopcategory_set.values_list('id', flat=True)
            print(sub_cates)
            queryset = BaykeShopSPU.objects.show().filter(
                category__id__in=list(sub_cates)).order_by('-add_date').distinct()

            print(queryset)
           
        if self.form.is_valid():
            field = self.form.cleaned_data['field']
            order = self.form.cleaned_data['order']
            field_name = f'-baykeshopsku__{field}' if order == 'asc' else f'baykeshopsku__{field}'
            queryset = queryset.order_by(f"{field_name}").distinct()
            
        # queryset = queryset.values(
        #         'id', 'title', 'category', 
        #         'cover_pic', 'baykeshopsku__price', 
        #         'baykeshopsku__cover_pic'
        #     )
        return queryset
    
    def get_category(self, object=None):
        """获取分类信息
            object为当前分类对象
            - 如果为None则返回一级分类
            - 如果传入对象父级不存在则返回所有的下级
            - 如果传入对象父级存在则返回该父级所有的下级
        """
        cates = BaykeShopCategory.objects.show().filter(parent__isnull=True)
        if object is not None and object.parent is None:
            cates = object.baykeshopcategory_set.show()
        elif object is not None and object.parent:
            cates = BaykeShopCategory.objects.show().filter(parent=object.parent)
        return cates
    
    def get_filter_queryset(self, queryset):
        form = self.form
        if form.is_valid():
            field = form.cleaned_data['field']
            order = form.cleaned_data['order']
            
            for spu in queryset:
                sku = spu.baykeshopsku_set.show().first()
                if order == 'asc':
                    sku = spu.baykeshopsku_set.show().order_by(f'-{field}').first()
                elif order == 'esc':
                    sku = spu.baykeshopsku_set.show().order_by(f'{field}').first()
                spu.price = sku.price
                spu.cost_price = sku.cost_price
                spu.org_price = sku.org_price
                spu.stock = sku.stock
                spu.sales = sku.sales
        return queryset
        
        
class GoodDetailView(DetailView):
    
    template_name = "baykeShop/detail.html"
    queryset = BaykeShopSPU.objects.show()
    context_object_name = "good"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['options_skus'], context['specs'] = self.get_options_skus()
        context['sku_options_first'] = self.get_sku_first_options()
        context['banners'] = self.get_spu_banners()
        return context
    
    def get_sku_queryset(self):
        good = self.get_object()
        skus_queryset = good.baykeshopsku_set.show()
        return skus_queryset
    
    def get_sku_first_options(self):
        # spu下的第一个sku的options
        skus_queryset = self.get_sku_queryset()
        sku_options_first = list(skus_queryset.first().options.values_list('name', flat=True))
        return sku_options_first         
    
    def get_options_skus(self):
        specs = []
        skus = {}
        skus_queryset = self.get_sku_queryset()
    
        for sku in skus_queryset:
            sku_options = sku.options.show()
            sku_options_names = sku_options.values_list('name', flat=True)
            # sku_dict = {}
            options = ','.join(sku_options_names)
            skus[options] = {
                'price': str(sku.price),
                'org_price': str(sku.org_price),
                'stock': sku.stock,
                'sales': sku.sales
            }
            # 返回当前spu下的specs
            for op in sku_options:
                spec_dict = {
                    'spec': op.spec.name, 
                    'options': list(BaykeShopSpecOption.objects.filter(spec=op.spec).values_list('name', flat=True))
                }
                if spec_dict not in specs:
                    specs.append(spec_dict)
        return skus, specs
    
    def get_spu_banners(self):
        spu = self.get_object()
        banners_queryset = spu.baykespucarousel_set.show()
        banners = banners_queryset.values(
            'img', 'target_url', 'desc'
        )
        if not banners_queryset:
            banners = [{'img': str(spu.cover_pic), 'desc': spu.title}]
        
        return list(banners)