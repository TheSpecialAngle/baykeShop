from django.contrib import admin
from django.utils.html import format_html, format_html_join
from django.utils.safestring import mark_safe
# Register your models here.
from baykeshop.public.admin import BaseModelAdmin
from baykeshop.models import (
    BaykeShopCategory, BaykeShopSPU, 
    BaykeShopSKU, BaykeShopSpec
)
from baykeshop.public.sites import bayke_site

from baykeshop.module.goods.inline import (
    BaykeShopCategoryInline, BaykeShopSKUInline,
    BaykeSPUCarouselInline, BaykeShopSpecOptionInline
)
from baykeshop.module.goods.forms import BaykeShopSPUForm


@admin.register(BaykeShopCategory, site=bayke_site)
class BaykeShopCategoryAdmin(BaseModelAdmin):
    list_display = ('id', 'name', 'parent', 'operate')
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
    list_display = (
        'id', 
        'dis_cover_pic', 
        'title', 
        'dis_price', 
        'dis_spec', 
        'dis_sales',
        'dis_stock',
        'operate'
    )
    list_display_links = ('title', )
    filter_horizontal = ('category',)
    form = BaykeShopSPUForm
    inlines = (BaykeShopSKUInline, BaykeSPUCarouselInline)
    
    class Media:
        css = {'all': ['baykeadmin/css/ordersku.css']}
    
    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == 'category':
            kwargs['queryset'] = BaykeShopCategory.objects.filter(parent__isnull=False)
        return super().formfield_for_manytomany(db_field, request, **kwargs)

    def get_skus(self, obj):
        return obj.baykeshopsku_set.order_by('price')
    
    @admin.display(description="封面图")
    def dis_cover_pic(self, obj):
        return format_html(mark_safe("<img width='64px' height='64px' src='{}' />"), obj.cover_pic.url)
    
    @admin.display(description="价格")
    def dis_price(self, obj):
        return self.get_skus(obj).first().price
    
    @admin.display(description="包含规格")
    def dis_spec(self, obj):
        return format_html_join(
            '\n', '{}<br>',
            (   
               (f"{k['spec__name']}:{k['name']}" for k in u.options.values('spec__name','name',)) for u in self.get_skus(obj) if u.options.exists() 
            )
        )
    
    @admin.display(description="销量")
    def dis_sales(self, obj):
        from django.db.models import Sum
        return self.get_skus(obj).aggregate(Sum('sales'))['sales__sum']

    @admin.display(description="库存")
    def dis_stock(self, obj):
        from django.db.models import Sum
        return self.get_skus(obj).aggregate(Sum('stock'))['stock__sum']
    

@admin.register(BaykeShopSKU, site=bayke_site)
class BaykeShopSKUAdmin(BaseModelAdmin):
    list_display = ('id', 'spu')
    # inlines = (BaykeShopSKUInline, )
    filter_horizontal = ('options',)
    # autocomplete_fields = ('options', )


@admin.register(BaykeShopSpec, site=bayke_site)
class BaykeShopSpecAdmin(BaseModelAdmin):
    list_display = ('id', 'name', 'operate')
    search_fields = ('name',)
    inlines = (BaykeShopSpecOptionInline, )