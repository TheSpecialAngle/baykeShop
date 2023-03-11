from django.db.models import Q
from django.views.generic.detail import SingleObjectMixin
from django.contrib import messages
from django.views.generic import ListView, DetailView

from baykeshop.config.settings import bayke_settings
from baykeshop.models import BaykeShopSPU, BaykeShopSKU, BaykeShopCategory, BaykeShopSpecOption
from baykeshop.public.forms import SearchForm


class BaykeShopSPUListView(ListView):
    """ 全部商品 """
    template_name = "baykeshop/goods/spus_list.html"
    paginate_by = bayke_settings.GOODS_PAGINATE_BY
    paginate_orphans = bayke_settings.GOODS_PAGINATE_ORPHANS

    def get_queryset(self):
        params = self.request.GET.dict()
        # 默认按日期排序
        queryset = BaykeShopSPU.objects.order_by('-add_date')
        # 按销量或价格排序
        if self.get_params_filed(params):
            queryset = self.get_order_queryset(self.get_params_filed(params), spus=queryset)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cates'] = BaykeShopCategory.get_cates().order_by('-add_date')
        context['sub_cates'] = context['cates'].first().baykeshopcategory_set.all()
        context['params'] = self.request.GET.dict()
        return context
    
    def get_order_queryset(self, params, spus, filter={}):
        # 按销量或价格排序
        queryset = []
        # 按价格排序
        if params and params['order'].replace('-', '') == 'price':
            skus = BaykeShopSKU.objects.filter(**filter).order_by(*list(params.values()))
            for sku in skus:
                if sku.spu not in queryset:
                    queryset.append(sku.spu)
        # 按销量排序
        elif params and params['order'].replace('-', '') == 'sales':
            from django.db.models import Sum
            datas = [{'spu': spu, 'sales': spu.baykeshopsku_set.aggregate(Sum('sales'))['sales__sum']} for spu in spus if spu]
            order_reverse = True if params['order'] == '-sales' else False
            datas.sort(key=lambda s: s['sales'], reverse=order_reverse)
            queryset = [ data['spu'] for data in datas ]
        return queryset
    
    def get_params_filed(self, params):
        if params.get('order'):
            return {'order':params.get('order')}
        return None
    
class BaykeShopCategoryDetailView(SingleObjectMixin, BaykeShopSPUListView):
    """ 商品分类 """
    def get(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=BaykeShopCategory.objects.all())
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cate_obj'] = self.object
        context['sub_cates'] = self.get_sub_cates()
        return context
    
    def get_queryset(self):
        cate = self.object
        params = self.request.GET.dict()
        if cate.parent is None:
            spus = BaykeShopSPU.objects.filter(category__in=cate.baykeshopcategory_set.all()).order_by('-add_date')
            # 按销量或价格排序
            if self.get_params_filed(params):
                cates = cate.baykeshopcategory_set.all()
                spus = self.get_order_queryset(self.get_params_filed(params), spus=spus, filter={'spu__category__in': cates})
        else:
            spus = BaykeShopSPU.objects.filter(category__id=self.kwargs['pk']).order_by('-add_date')
            # 按销量或价格排序
            if self.get_params_filed(params):
                spus = self.get_order_queryset(self.get_params_filed(params), spus=spus, filter={'spu__category__id':self.kwargs['pk']})
        return spus
    
    def get_sub_cates(self):
        if self.object.parent:
            return self.object.parent.baykeshopcategory_set.all()
        elif self.object.parent is None:
            return self.object.baykeshopcategory_set.all()
    
    
class SearchTemplateView(BaykeShopSPUListView):
    """ 搜索视图 """
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['word'] = self.request.GET.get('word')
        return context
    
    def get_queryset(self):
        queryset = super().get_queryset()
        form = SearchForm(self.request.GET)
        if form.is_valid():
            word = form.cleaned_data['word']
            queryset = queryset.filter(
                Q(title__icontains=word)|Q(desc__icontains=word)|Q(keywords__icontains=word)
            )
            messages.add_message(self.request, messages.SUCCESS, f'共搜索到{queryset.count()}条数据')
        return queryset


class BaykeShopSPUDetailView(DetailView):
    """ 商品详情页 """
    model = BaykeShopSPU
    template_name = "baykeshop/goods/spu_detail.html"
    context_object_name = "spu"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['skus'], context['specs'] = self.get_skus()
        return context
    
    def get_banners(self, sku_id=None):
        # 轮播图
        spu = self.get_object()
        banners = [ban.img.url for ban in spu.baykespucarousel_set.all()]
        if sku_id is not None:
            try:
                sku = BaykeShopSKU.objects.get(id=sku_id)
                banners.insert(0, sku.cover_pic.url) 
            except BaykeShopSKU.DoesNotExist:
                pass
        return banners
        
    def get_skus(self):
        # 规格商品
        spu = self.get_object()
        skus_queryset = spu.baykeshopsku_set.order_by('price')
        
        # 当前spu下的规格选项
        specs = []
        # 规格选项对应的sku
        skus = {}
        for sku in skus_queryset:
            sku_options_names = sku.options.values_list('name', flat=True)
            options = ','.join(sku_options_names)
            skus[options] = {
                'sku_id': sku.id,
                'price': sku.price.to_eng_string(),
                'org_price': sku.org_price.to_eng_string(),
                'stock': sku.stock,
                'sales': sku.sales,
                'cover_pic': sku.cover_pic.url,
                'banners': self.get_banners(sku_id=sku.id)
            }
            
            # 返回当前spu下的specs
            for op in sku.options.all():
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
        print(skus, specs)
        return skus, specs
    
    
        
        