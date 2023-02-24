from django.contrib import admin
from django.db.models import Q
from django.contrib.auth.models import Permission
from django.utils.text import capfirst
from django.urls import NoReverseMatch, Resolver404, resolve, reverse


from baykeshop.models import BaykeMenu



class BaykeAdminSite(admin.AdminSite):
    
    
    def get_app_list(self, request):
        
        # 获取当前用户拥有的权限菜单
        menus_queryset = BaykeMenu.objects.filter(
                Q(baykepermission__permission__group__user=request.user)|
                Q(baykepermission__permission__user=request.user)
            ).distinct()
        
        # 如果为超管则赋予所有权限
        if request.user.is_superuser:
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
                    except NoReverseMatch:
                        pass
                
                if perms.get("add"):
                    try:
                        model_dict["add_url"] = reverse(
                            "admin:%s_%s_add" % info, current_app=self.name
                        )
                    except NoReverseMatch:
                        pass
                
                item_model.append(model_dict)
                # item_model.append({model:self._registry[model]})
            menu_dict[menu] = item_model
            menus.append(menu_dict)
        
        print(menus)
        # print(super().get_app_list(request))
        
        return super().get_app_list(request)

bayke_site = BaykeAdminSite(name="baykeadmin")