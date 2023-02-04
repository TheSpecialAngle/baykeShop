from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
# Register your models here.
from baykeAdmin.admin import BaseModelAdmin
from .models import (
    BaykeShopCategory, BaykeShopSPU, 
    BaykeSPUCarousel, BaykeShopSKU, 
    BaykeShopSpec, 
    # BaykeShopSpecGroup, 
    BaykeShopSpecOption
)

class BaykeShopCategoryInline(admin.TabularInline):
    '''Tabular Inline View for BaykeShopCategory'''

    model = BaykeShopCategory
    min_num = 1
    max_num = 20
    extra = 1
    exclude = ('img_map', )
    # raw_id_fields = (,)

class BaykeShopSKUInline(admin.TabularInline):
    '''Stacked Inline View for BaykeShopSKU'''

    model = BaykeShopSKU
    # min_num = 1
    max_num = 20
    extra = 1
    can_delete = False
    # raw_id_fields = (,)

class BaykeSPUCarouselInline(admin.TabularInline):
    '''Tabular Inline View for '''

    model = BaykeSPUCarousel
    min_num = 1
    max_num = 20
    extra = 1
    # raw_id_fields = (,)


@admin.register(BaykeShopCategory)
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
    
    
@admin.register(BaykeShopSPU)
class BaykeShopSPUAdmin(BaseModelAdmin):
    list_display = ('id', 'title', 'operate')
    filter_horizontal = ('category',)
    inlines = (BaykeShopSKUInline, BaykeSPUCarouselInline)
    
    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == 'category':
            kwargs['queryset'] = BaykeShopCategory.objects.filter(parent__isnull=False)
        return super().formfield_for_manytomany(db_field, request, **kwargs)


@admin.register(BaykeShopSKU)
class BaykeShopSKUAdmin(BaseModelAdmin):
    list_display = ('id', 'spu', 'operate')
    # inlines = (BaykeShopSKUInline, )
    filter_horizontal = ('options',)
    # autocomplete_fields = ('options', )


class BaykeShopSpecOptionInline(admin.StackedInline):
    '''Stacked Inline View for '''

    model = BaykeShopSpecOption
    min_num = 1
    max_num = 20
    extra = 1


@admin.register(BaykeShopSpec)
class BaykeShopSpecAdmin(BaseModelAdmin):
    list_display = ('id', 'name', 'operate')
    # search_fields = ('name',)
    inlines = (BaykeShopSpecOptionInline, )


# admin.site.register(BaykeShopSKU)
admin.site.register(BaykeSPUCarousel)
admin.site.register(BaykeShopSpecOption)