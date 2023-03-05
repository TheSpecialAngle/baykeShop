from django.db.models import Q
from django.views.generic.detail import SingleObjectMixin
from django.contrib import messages
from django.views.generic import ListView

from baykeshop.config.settings import bayke_settings
from baykeshop.models import BaykeShopSPU, BaykeShopCategory
from baykeshop.public.forms import SearchForm


class BaykeShopSPUListView(ListView):
    """ 全部商品 """
    template_name = "baykeshop/goods/spus_list.html"
    paginate_by = bayke_settings.GOODS_PAGINATE_BY
    paginate_orphans = bayke_settings.GOODS_PAGINATE_ORPHANS

    def get_queryset(self):
        queryset = BaykeShopSPU.objects.order_by('-add_date')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cates'] = BaykeShopCategory.get_cates().order_by('-add_date')
        context['sub_cates'] = context['cates'].first().baykeshopcategory_set.all()
        return context


class BaykeShopCategoryDetailView(SingleObjectMixin, BaykeShopSPUListView):
    """ 商品分类 """
    
    def get(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=BaykeShopCategory.objects.all())
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cate'] = self.object
        return context

    def get_queryset(self):
        cate = self.object
        if cate.parent is None:
            spus = BaykeShopSPU.objects.filter(
                category__in=cate.baykeshopcategory_set.all()
            ).order_by('-add_date')
        else:
            spus = BaykeShopSPU.objects.filter(
                category__id=self.kwargs['pk']
            ).order_by('-add_date')
        return spus

    
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