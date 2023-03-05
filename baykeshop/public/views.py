from django.db.models import Q
from django.http.response import JsonResponse
from django.views.generic import View, TemplateView, ListView
from django.contrib import messages

from baykeshop.models import BaykeShopSPU
from baykeshop.public.forms import SearchForm
from baykeshop.config.settings import bayke_settings


class HomeTemplateView(TemplateView):
    """ 商城首页 """
    template_name = "baykeshop/index.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cates'] = self.get_queryset()
        return context
    
    def get_queryset(self):
        from baykeshop.models import BaykeShopCategory, BaykeShopSPU
        queryset = BaykeShopCategory.get_cates()
        for cate in queryset:
            cate.spus = BaykeShopSPU.objects.filter(category__in=cate.sub_cates)[:bayke_settings.HOME_GOODS_COUNT]
        return queryset


class BaykeShopSPUListView(ListView):
    """ 全部商品 """
    template_name = "baykeshop/spus_list.html"
    context_object_name = "spus"
    paginate_by = bayke_settings.GOODS_PAGINATE_BY
    paginate_orphans = bayke_settings.GOODS_PAGINATE_ORPHANS

    def get_queryset(self):
        queryset = BaykeShopSPU.objects.all()
        return queryset


class SearchTemplateView(BaykeShopSPUListView):
    """ 搜索视图 """
    template_name = "baykeshop/search.html"

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


class WangEditorUploadImg(View):
    """ 编辑器上传图片接口 """
    def post(self, request, *args, **kwargs):
        perms = [
            request.user.is_authenticated,
            request.user.is_active,
            request.user.is_staff,
            request.user.is_superuser,
            request.user.has_perm('baykeshop.add_baykeupload')
        ]
        if not all(perms):
            return JsonResponse({
                "errno": 1,  # 只要不等于 0 就行
                "message": "无权限上传..."
            })
        from baykeshop.public.forms import BaykeUploadModelForm
        form = BaykeUploadModelForm(request.POST, request.FILES)
        if form.is_valid():
            u = form.save()
            return JsonResponse({
                "errno": 0, 
                "data": {
                    "url": u.img.url, # 图片 src ，必须
                    "alt": u.img.name, # 图片描述文字，非必须
                    "href": u.img.url # 图片的链接，非必须
                }
            })
        return JsonResponse({"errno": 2, "message": "发生保存错误！"})