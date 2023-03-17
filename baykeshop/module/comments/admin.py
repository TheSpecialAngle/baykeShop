from django.contrib import admin

from baykeshop.public.admin import BaseModelAdmin
from baykeshop.public.sites import bayke_site
from baykeshop.models import BaykeOrderInfoComments


@admin.register(BaykeOrderInfoComments, site=bayke_site)
class BaykeOrderInfoCommentsAdmin(BaseModelAdmin):
    list_display = ('id', 'owner', 'comment_choices', 'content')
    
    def has_change_permission(self, request, obj=None) -> bool:
        return False
    
    def has_add_permission(self, request) -> bool:
        return False