from django.contrib import admin
from django.contrib.auth.models import Permission, Group
from django.db.models import Q
from django.urls import NoReverseMatch, reverse

from baykeAdmin.forms import BaykeAdminLoginForm
from baykeAdmin.models import BaykeMenu, BaykePermission


class BaykeAdminSite(admin.AdminSite):
    
    login_form = BaykeAdminLoginForm
    login_template = 'baykeAdmin/login.html'
    
    index_template = 'baykeAdmin/index.html'
    
    def get_app_list(self, request, app_label=None):
        menus = []
        if request.user.is_authenticated:
            user = request.user
            # 获取用户拥有权限的菜单
            menus_queryset = BaykeMenu.objects.filter(
                Q(baykepermission__permission__group__user=user)|
                Q(baykepermission__permission__user=user)
            ).distinct()

            for menu in menus_queryset:
                menu_dict = {}
                menu_dict['id'] = menu.id
                menu_dict['name'] = menu.name
                menu_dict['parent'] = menu.parent.id if menu.parent else None
                menu_dict['children'] = self._menu_children_list(user, menu.baykepermission_set.show())
                menus.append(menu_dict)
        return menus
    
    def _menu_children_list(self, user, queryset):
        
        children = []
        
        for q in queryset:
            q_dict = {}
            q_dict['per_name'] = q.permission.name
            q_dict['codename'] = q.permission.codename
            q_dict['app_label'] = q.permission.content_type.app_label
            q_dict['object_name'] = q.permission.content_type.name
            q_dict['model'] = q.permission.content_type.model
            q_dict['model_obj'] = q.permission.content_type.model_class
            q_dict['info'] = q.permission.content_type.natural_key()
            q_dict['perms'] = {
                'view': user.has_perm(f"{q_dict['app_label']}.view_{q_dict['model']}"),
                'change': user.has_perm(f"{q_dict['app_label']}.change_{q_dict['model']}"),
                'add': user.has_perm(f"{q_dict['app_label']}.add_{q_dict['model']}"),
                'delete': user.has_perm(f"{q_dict['app_label']}.delete_{q_dict['model']}"),
            }
            
            if q_dict['perms']['view'] or q_dict['perms']['change']:
                q_dict['view_only'] = not q_dict['perms']['change']
                
                try:
                    q_dict["admin_url"] = reverse(
                        "admin:%s_%s_changelist" % q_dict['info'], current_app=self.name
                    )
                    children.append(q_dict)
                except NoReverseMatch:
                    pass
            
            if q_dict['perms']['add']:
                try:
                    q_dict["add_url"] = reverse(
                            "admin:%s_%s_add" % q_dict['info'], current_app=self.name
                        )
                    # children.append(q_dict)
                except NoReverseMatch:
                    pass
                
        return children
            
            
            