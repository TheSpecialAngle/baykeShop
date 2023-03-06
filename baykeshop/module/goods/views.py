from django.db.models import Q
from django.views.generic.detail import SingleObjectMixin
from django.contrib import messages
from django.views.generic import ListView

from baykeshop.config.settings import bayke_settings
from baykeshop.models import BaykeShopSPU, BaykeShopSKU, BaykeShopCategory
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
        if params:
            queryset = self.get_order_queryset(params, spus=queryset)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cates'] = BaykeShopCategory.get_cates().order_by('-add_date')
        context['sub_cates'] = context['cates'].first().baykeshopcategory_set.all()
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
            datas.sort(key=lambda s: s['sales'], reverse=True)
            queryset = [data['spu'] for data in datas ]
        return queryset

    
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
            if params:
                cates = cate.baykeshopcategory_set.all()
                spus = self.get_order_queryset(params, spus=spus, filter={'spu__category__in': cates})
        else:
            spus = BaykeShopSPU.objects.filter(category__id=self.kwargs['pk']).order_by('-add_date')
            # 按销量或价格排序
            if params:
                spus = self.get_order_queryset(params, spus=spus, filter={'spu__category__id':self.kwargs['pk']})
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