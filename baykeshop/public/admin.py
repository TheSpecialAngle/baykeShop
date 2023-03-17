from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.translation import gettext as _

from baykeshop.public.sites import bayke_site
from baykeshop.models import BaykeBanner


class BaseModelAdmin(admin.ModelAdmin):
    """继承了django的ModelAdmin
    重写并新增了一些全局方法
    """
    
    change_list_template = "baykeadmin/change_list.html"
    change_form_template = "baykeadmin/change_form.html"
    
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if self.model._meta.model_name not in ['user', 'group', 'permission', 'logentry']:
            return queryset.filter(is_del=False)
        return queryset
    
    def change_view(self, request, object_id, form_url="", extra_context=None):
        return super().change_view(request, object_id, form_url, extra_context)
    
    @admin.display(description="操作")
    def operate(self, obj):
        hs = '<a href="{}">编辑</a> | <a href="{}">删除</a>'
        h1 = reverse(f'baykeadmin:{obj._meta.app_label}_{obj._meta.model_name}_change', args=(obj.pk, ))
        h2 = reverse(f'baykeadmin:{obj._meta.app_label}_{obj._meta.model_name}_delete', args=(obj.pk, ))
        return format_html(hs, h1, h2)
    

@admin.register(BaykeBanner, site=bayke_site)
class BaykeShopBannerAdmin(BaseModelAdmin):
    list_display = ('id', 'imgformat', 'target_url', 'operate')
    
    @admin.display(description="轮播图")
    def imgformat(self, obj):
        return format_html(f'<img src="{obj.img.url}" width="auto" height="100px" />')

    class Media:
        css = {'all': ['baykeadmin/css/ordersku.css']}