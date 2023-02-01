from django.contrib import admin
from django.contrib.auth.models import Permission, User, Group
from django.contrib.admin.models import LogEntry
from django.contrib.auth.admin import (
    UserAdmin as BaseUserAdmin, 
    GroupAdmin as BaseGroupAdmin
)
# Register your models here.
from .models import BaykeMenu, BaykePermission
from .custom import CustomActions, CustomColumns

# 禁用全局删除
# admin.site.disable_action('delete_selected')

admin.site.unregister(User)
admin.site.unregister(Group)
    
class BaseModelAdmin(admin.ModelAdmin, CustomColumns):
    """
    继承了django的ModelAdmin
    重写并新增了一些全局方法
    """
    
    # change_list_template = "baykeAdmin/change_list.html"
    actions = ["mark_delete", "export_as_csv"]
    
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if self.model._meta.model_name not in ['user', 'group', 'permission', 'logentry']:
            return queryset.filter(is_del=False)
        return queryset
    
    def get_permission(self):
        permission = BaykePermission.objects.filter(
            permission__content_type__app_label=self.model._meta.app_label
        )
        return permission
    
    def changelist_view(self, request, extra_context=None):
        permission = self.get_permission().first()
        extra_context = {'menu': permission}
        return super().changelist_view(request, extra_context)
    
    def change_view(self, request, object_id, form_url="", extra_context=None):
        permission = self.get_permission().first()
        extra_context = {'menu': permission}
        return super().change_view(request, object_id, form_url, extra_context)


@admin.register(User)
class UserAdmin(BaseUserAdmin, BaseModelAdmin):
    pass

@admin.register(Group)
class GroupAdmin(BaseGroupAdmin, BaseModelAdmin):
    pass


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
    
    
@admin.register(LogEntry)
class LogEntryAdmin(BaseModelAdmin):
    '''Admin View for '''

    list_display = (
        'id', 'action_time', 'user', 'content_type', 
        'object_id', 'object_repr', 'action_flag', 'change_message'
    )
    
    def has_add_permission(self, request) -> bool:
        return False
    
    def has_change_permission(self, request, obj=None) -> bool:
        return False