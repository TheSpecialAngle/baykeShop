from django.contrib import admin
from django.utils.html import format_html
# Register your models here.
from baykeshop.admin.base import BaseModelAdmin
from baykeshop.models import (
    BaykeShopCategory, BaykeShopSPU, 
    BaykeSPUCarousel, BaykeShopSKU, 
    BaykeShopSpec, BaykeShopSpecOption,
    BaykeShopOrderInfo, BaykeShopOrderSKU,
    BaykeBanner
)
from baykeshop.admin.sites import bayke_site
from baykeshop.admin.inline import (
    BaykeShopCategoryInline, BaykeShopSKUInline,
    BaykeSPUCarouselInline, BaykeShopSpecOptionInline
)
    

@admin.register(BaykeShopCategory, site=bayke_site)
class BaykeShopCategoryAdmin(BaseModelAdmin):
    list_display = ('id', 'name', 'parent')
    exclude = ('parent',)
    inlines = (BaykeShopCategoryInline, )
    # search_fields = ('parent__name',)
    # autocomplete_fields = ('parent', )
    
    def get_queryset(self, request):
        return super().get_queryset(request).filter(parent__isnull=True)
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'parent':
            kwargs['queryset'] = BaykeShopCategory.objects.filter(parent__isnull=True)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
    
    
@admin.register(BaykeShopSPU, site=bayke_site)
class BaykeShopSPUAdmin(BaseModelAdmin):
    list_display = ('id', 'title')
    filter_horizontal = ('category',)
    inlines = (BaykeShopSKUInline, BaykeSPUCarouselInline)
    
    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == 'category':
            kwargs['queryset'] = BaykeShopCategory.objects.filter(parent__isnull=False)
        return super().formfield_for_manytomany(db_field, request, **kwargs)


@admin.register(BaykeShopSKU, site=bayke_site)
class BaykeShopSKUAdmin(BaseModelAdmin):
    list_display = ('id', 'spu')
    # inlines = (BaykeShopSKUInline, )
    filter_horizontal = ('options',)
    # autocomplete_fields = ('options', )


@admin.register(BaykeShopSpec, site=bayke_site)
class BaykeShopSpecAdmin(BaseModelAdmin):
    list_display = ('id', 'name')
    # search_fields = ('name',)
    inlines = (BaykeShopSpecOptionInline, )


@admin.register(BaykeBanner)
class BaykeShopBannerAdmin(BaseModelAdmin):
    list_display = ('id', 'imgformat', 'target_url')
    
    @admin.display(description="轮播图")
    def imgformat(self, obj):
        if obj.img:
            return format_html(f'<img src="{obj.img.url}" width="auto" height="100px" />')


# admin.site.register(BaykeShopSKU)
admin.site.register(BaykeSPUCarousel)
admin.site.register(BaykeShopSpecOption)
# bayke_site.register(BaykeShopOrderInfo)
admin.site.register(BaykeShopOrderSKU)