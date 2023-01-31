from django.contrib import admin
from django.contrib.auth.models import Permission
# Register your models here.
from .models import BaykeMenu, BaykePermission

# 禁用全局删除
admin.site.disable_action('delete_selected')

class BaseModelAdmin(admin.ModelAdmin):
    
    change_list_template = "baykeAdmin/change_list.html"
    
    def changelist_view(self, request, extra_context=None):
        permission = BaykePermission.objects.filter(
            permission__content_type__app_label=self.model._meta.app_label).first()
        extra_context = {'menu': permission.menus.name}
        return super().changelist_view(request, extra_context)
    

@admin.register(BaykeMenu)
class BaykeMenuAdmin(BaseModelAdmin):
    '''Admin View for BaykeMenu'''

    list_display = ('id', 'name', 'add_date')
    list_editable = ('name', )
    list_filter = ('name',)
    search_fields = ('name', )
    # inlines = [
    #     Inline,
    # ]
    # raw_id_fields = ('',)
    # readonly_fields = ('',)
    # search_fields = ('',)
    # date_hierarchy = ''
    # ordering = ('',)
    # list_per_page = 1


@admin.register(BaykePermission)
class BaykePermissionAdmin(BaseModelAdmin):
    '''Admin View for BaykePermission'''

    list_display = ('id', 'permission_name', 'add_date')
    # list_editable = ('name', )
    # list_filter = ('name',)
    # search_fields = ('name', )
    
    @admin.display(description='Name')
    def permission_name(self, obj):
        return f"{obj.permission.name}"