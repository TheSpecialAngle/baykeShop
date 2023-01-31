from django.contrib import admin

# Register your models here.
from baykeAdmin.admin import BaseModelAdmin
from .models import (
    BaykeShopCategory, BaykeShopSPU, 
    BaykeSPUCarousel, BaykeShopSKU, 
    BaykeShopSpec, BaykeShopSpecGroup, 
    BaykeShopSpecOption
)

@admin.register(BaykeShopCategory)
class BaykeShopCategoryAdmin(BaseModelAdmin):
    list_display = ('id', 'name', 'operate')


@admin.register(BaykeShopSPU)
class BaykeShopSPUAdmin(BaseModelAdmin):
    list_display = ('id', 'title', 'operate')

# admin.site.register(BaykeShopCategory)
# admin.site.register(BaykeShopSPU)
admin.site.register(BaykeShopSKU)
admin.site.register(BaykeSPUCarousel)
admin.site.register(BaykeShopSpec)
admin.site.register(BaykeShopSpecGroup)
admin.site.register(BaykeShopSpecOption)