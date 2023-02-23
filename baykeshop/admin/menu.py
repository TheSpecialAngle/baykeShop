from django.contrib import admin

from baykeshop.models import BaykeMenu


@admin.register(BaykeMenu)
class BaykeMenuAdmin(admin.ModelAdmin):
    '''Admin View for BaykeMenu'''

    list_display = ('id', 'name', 'icon')
    # list_filter = ('',)
    # inlines = [
    #     Inline,
    # ]
    # raw_id_fields = ('',)
    # readonly_fields = ('',)
    # search_fields = ('',)
    # date_hierarchy = ''
    # ordering = ('',)