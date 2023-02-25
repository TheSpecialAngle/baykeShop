from django.contrib import admin
from django.db.models import Q
from django.contrib.auth.models import Permission
from django.utils.text import capfirst
from django.urls import NoReverseMatch, reverse

from baykeshop.conf.bayke import bayke_settings
from baykeshop.models import BaykeMenu



class BaykeAdminSite(admin.AdminSite):
    """ 自定义AdminSite """
    
    def get_app_list(self, request):
        # 判断是否启用了自定义菜单
        if bayke_settings.ADMIN_MENUS:
            return self._build_menus(request)
        
        return super().get_app_list(request)

    def _build_menus(self, request):
        request.breadcrumbs = None
        # 获取当前用户拥有的权限菜单
        menus_queryset = BaykeMenu.objects.filter(
            Q(baykepermission__permission__group__user=request.user)|
            Q(baykepermission__permission__user=request.user)
        ).distinct()
        
        # 如果为超管则赋予所有权限
        if self.has_permission(request) and request.user.is_superuser:
            perms_ids = Permission.objects.values_list('id', flat=True)
            menus_queryset = BaykeMenu.objects.filter(
                baykepermission__permission__id__in=list(perms_ids)
            ).distinct()
            
        menus = []
        
        for menu in menus_queryset:
            menu_dict = {}
            item_model = []
            for perm in menu.baykepermission_set.all():
                model = perm.permission.content_type.model_class()
                
                model_admin = self._registry[model]
                app_label = model._meta.app_label
                
                has_module_perms = model_admin.has_module_permission(request)
                if not has_module_perms:
                    continue
                
                perms = model_admin.get_model_perms(request)
                
                if True not in perms.values():
                    continue
                
                info = (app_label, model._meta.model_name)
                
                model_dict = {
                    "model": model,
                    "name": capfirst(model._meta.verbose_name_plural),
                    "object_name": model._meta.object_name,
                    "perms": perms,
                    "admin_url": None,
                    "add_url": None,
                }
                
                if perms.get("change") or perms.get("view"):
                    model_dict["view_only"] = not perms.get("change")
                    try:
                        model_dict["admin_url"] = reverse(
                            "admin:%s_%s_changelist" % info, current_app=self.name
                        )
                        # breadcrumbs挂载到request对象上
                        if request.path == model_dict["admin_url"]:
                            request.breadcrumbs = {
                                menu.name: {
                                    'name': capfirst(model._meta.verbose_name_plural), 
                                    'url': model_dict["admin_url"]
                                    }
                                }
                    except NoReverseMatch:
                        pass
                
                if perms.get("add"):
                    try:
                        model_dict["add_url"] = reverse(
                            "admin:%s_%s_add" % info, current_app=self.name
                        )
                        # breadcrumbs挂载到request对象上
                        if request.path == model_dict["add_url"]:
                            request.breadcrumbs = {
                                menu.name: {
                                    'name': capfirst(model._meta.verbose_name_plural), 
                                    'url': model_dict["admin_url"]
                                    }
                                }
                    except NoReverseMatch:
                        pass
                
                item_model.append(model_dict)
                
            menu_dict['name'] = menu.name
            menu_dict['app_label'] = app_label
            menu_dict['app_url'] = "#"
            menu_dict['has_module_perms'] = has_module_perms
            menu_dict['models'] = item_model
            menus.append(menu_dict)
        return menus


bayke_site = BaykeAdminSite(name="baykeadmin")