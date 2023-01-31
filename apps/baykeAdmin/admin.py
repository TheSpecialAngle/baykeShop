import csv
from django.contrib import admin
from django.contrib.auth.models import Permission
# Register your models here.
from .models import BaykeMenu, BaykePermission
from .custom import CustomActions, CustomColumns

# 禁用全局删除
# admin.site.disable_action('delete_selected')

    
class BaseModelAdmin(admin.ModelAdmin, CustomColumns):
    """
    继承了django的ModelAdmin
    重写并新增了一些全局方法
    """
    
    change_list_template = "baykeAdmin/change_list.html"
    actions = ["mark_delete", "export_as_csv"]
    
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if self.model._meta.model_name not in ['user', 'group', 'permission']:
            return queryset.filter(is_del=False)
        return queryset
        
    def changelist_view(self, request, extra_context=None):
        permission = BaykePermission.objects.filter(
            permission__content_type__app_label=self.model._meta.app_label
        ).first()
        extra_context = {'menu': permission.menus.name}
        return super().changelist_view(request, extra_context)
    

class BaykePermissionInline(admin.TabularInline):
    '''Tabular Inline View for BaykePermission'''

    model = BaykePermission
    min_num = 1
    max_num = 20
    extra = 1
    # raw_id_fields = (,)

@admin.register(BaykeMenu)
class BaykeMenuAdmin(BaseModelAdmin):
    '''Admin View for BaykeMenu'''

    list_display = ('id', 'name', 'add_date', 'operate')
    list_editable = ('name', )
    list_filter = ('name',)
    search_fields = ('name', )
    # inlines = [
    #     BaykePermissionInline,
    # ]
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "parent":
            kwargs["queryset"] = BaykeMenu.objects.show().filter(parent__isnull=True)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
    
    
@admin.register(Permission)
class PermissionAdmin(BaseModelAdmin):
    '''Admin View for BaykePermission'''

    list_display = ('id', 'name', 'operate')
    search_fields = ('name', )
    readonly_fields = ('codename', 'content_type')
    # inlines = (BaykePermissionInline, )

    
@admin.register(BaykePermission)
class BaykePermissionAdmin(BaseModelAdmin):
    '''Admin View for BaykePermission'''

    list_display = ('id', 'permission_name', 'operate')
    
    @admin.display(description='Name')
    def permission_name(self, obj):
        return f"{obj.permission.name}"
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "menus":
            kwargs["queryset"] = BaykeMenu.objects.show().filter(parent__isnull=True)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)