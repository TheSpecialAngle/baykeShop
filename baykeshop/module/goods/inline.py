from django.contrib import admin

from baykeshop.models import (
    BaykeShopCategory, BaykeShopSKU, 
    BaykeSPUCarousel, BaykeShopSpecOption
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
    

class BaykeSPUCarouselInline(admin.StackedInline):
    '''Tabular Inline View for '''

    model = BaykeSPUCarousel
    min_num = 1
    max_num = 20
    extra = 1
    exclude = ('target_url', 'desc')
    # raw_id_fields = (,)
    

class BaykeShopSpecOptionInline(admin.StackedInline):
    '''Stacked Inline View for '''

    model = BaykeShopSpecOption
    min_num = 1
    max_num = 20
    extra = 1