from django import forms
from django.contrib import admin
from django.contrib.admin.options import PermissionDenied
from django.template.response import TemplateResponse
from django.http.response import HttpResponseRedirect
from django.utils.translation import gettext as _


from baykeshop.forms.admin.action import ActionForm
from baykeshop.admin.options import CustomActions, CustomColumns


class BaseModelAdmin(admin.ModelAdmin, CustomColumns):
    """继承了django的ModelAdmin
    重写并新增了一些全局方法
    """
    class Media:
        css = {
            "all": ("baykeshop/css/buefy.min.css",)
        }
        js = (
            "baykeshop/js/vue.js",
            "baykeshop/js/buefy.min.js",
            "baykeadmin/js/request.js",
        )
    
    change_list_template = "baykeadmin/change_list.html"
    actions = ["mark_delete", "export_as_csv"]
    action_form = ActionForm

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if self.model._meta.model_name not in ['user', 'group', 'permission', 'logentry']:
            return queryset.filter(is_del=False)
        return queryset
    
    def changelist_view(self, request, extra_context=None):
        
        opts = self.model._meta
        app_label = opts.app_label
        if not self.has_view_or_change_permission(request):
            raise PermissionDenied
        
        cl = self.get_changelist_instance(request)
        
         
        context = {
            "media": forms.Media(self.Media),
            **(extra_context or {}),
        }
        
        return TemplateResponse(request, self.change_list_template, context)
    
    # def changelist_view(self, request, extra_context=None):
    #     return super().changelist_view(request, extra_context)