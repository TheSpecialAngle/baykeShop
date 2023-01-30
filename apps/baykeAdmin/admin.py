from django.contrib import admin

# Register your models here.
from .models import BaykeMenu, BaykePermission


class BaseModelAdmin(admin.ModelAdmin):
    change_list_template = 'baykeAdmin/change/change_list.html'

    def changelist_view(self, request, extra_context=None):
        return super().changelist_view(request, extra_context)

@admin.register(BaykeMenu)
class BaykeMenuAdmin(BaseModelAdmin):
    '''Admin View for BaykeMenu'''

    list_display = ('id', 'name', )
    list_editable = ('name', )
    list_filter = ('name',)
    # inlines = [
    #     Inline,
    # ]
    # raw_id_fields = ('',)
    # readonly_fields = ('',)
    # search_fields = ('',)
    # date_hierarchy = ''
    # ordering = ('',)


# admin.site.register(BaykeMenu)
# admin.site.register(BaykePermission)