from django.contrib import admin
from django.utils.html import format_html, format_html_join
from django.utils.safestring import mark_safe
# Register your models here.
from baykeshop.admin.base import BaseModelAdmin
from baykeshop.models import (
    BaykeShopCategory, BaykeShopSPU, 
    BaykeShopSKU, BaykeShopSpec, 
    BaykeBanner, BaykeShopOrderSKUComment
)
from baykeshop.admin.sites import bayke_site
from baykeshop.admin.inline import (
    BaykeShopCategoryInline, BaykeShopSKUInline,
    BaykeSPUCarouselInline, BaykeShopSpecOptionInline
)
from baykeshop.forms.shop.user import BaykeShopSPUForm


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
                (
                    f"{k['spec__name']}:{k['name']}" 
                    for k in u.options.values('spec__name','name',)
                )
                for u in self.get_skus(obj) if u
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
    

@admin.register(BaykeShopOrderSKUComment, site=bayke_site)
class BaykeShopOrderSKUCommentAdmin(BaseModelAdmin):
    """ 商品评论 """
    list_display = ('owner', 'order_sku', 'content', 'ds_comment_sale', 'ds_comment_choices', 'operate')
    
    @admin.display(description="评分")
    def ds_comment_sale(self, obj):
        return obj.comment_choices
    
    @admin.display(description="评价")
    def ds_comment_choices(self, obj):
        return obj.get_comment_choices_display()
    
    # @admin.display(description="操作")
    # def operate(self, obj):
    #     hs = '{} | <a class="button" href="{}">编辑</a> | <a class="button" href="{}"><span class="deletelink">删除</span></a>'
    #     h1 = mark_safe('''
    #         <a class="related-widget-wrapper-link add-related" id="add_id_menus" data-popup="yes" 
    #             href="/baykeadmin/baykeshop/baykemenu/add/?_to_field=id&amp;_popup=1" title="回复评论">
    #         回复
    #         </a>
    #     ''')
    #     h2 = reverse(f'baykeadmin:{obj._meta.app_label}_{obj._meta.model_name}_change', args=(obj.pk, ))
    #     h3 = reverse(f'baykeadmin:{obj._meta.app_label}_{obj._meta.model_name}_delete', args=(obj.pk, ))
    #     return format_html(hs, h1, h2, h3)
    
    def has_add_permission(self, request):
        return False
    

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


@admin.register(BaykeBanner, site=bayke_site)
class BaykeShopBannerAdmin(BaseModelAdmin):
    list_display = ('id', 'imgformat', 'target_url', 'operate')
    
    @admin.display(description="轮播图")
    def imgformat(self, obj):
        return format_html(f'<img src="{obj.img.url}" width="auto" height="100px" />')

    class Media:
        css = {'all': ['baykeadmin/css/ordersku.css']}
