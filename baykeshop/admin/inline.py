from django.contrib import admin

from baykeshop.models import (
    BaykePermission, BaykeUserInfo, BaykeShopCategory,
    BaykeShopSKU, BaykeSPUCarousel, BaykeShopSpecOption
)


class BaykeUserInfoInline(admin.StackedInline):
    '''Tabular Inline View for BaykeUserInfo'''
    model = BaykeUserInfo
    

class BaykePermissionInline(admin.TabularInline):
    '''Tabular Inline View for BaykePermission'''

    model = BaykePermission
    min_num = 1
    max_num = 20
    extra = 1
    # raw_id_fields = (,)


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
    

class BaykeShopSpecOptionInline(admin.StackedInline):
    '''Stacked Inline View for '''

    model = BaykeShopSpecOption
    min_num = 1
    max_num = 20
    extra = 1