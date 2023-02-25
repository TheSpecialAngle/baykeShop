from django.contrib import admin
from baykeshop.admin.sites import bayke_site
from baykeshop.models import BaykeMenu
from baykeshop.admin.base import BaseModelAdmin


@admin.register(BaykeMenu, site=bayke_site)
class BaykeMenuAdmin(BaseModelAdmin):
    '''Admin View for BaykeMenu'''

    list_display = ('id', 'name')