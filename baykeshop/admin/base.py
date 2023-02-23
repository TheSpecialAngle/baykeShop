from django.contrib import admin
from django.contrib.admin.options import IncorrectLookupParameters
from django.template.response import SimpleTemplateResponse
from django.http.response import HttpResponseRedirect

from django.contrib.admin import helpers, widgets

from django.utils.translation import gettext as _
from django.core.exceptions import PermissionDenied

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
        from django.contrib.admin.views.main import ERROR_FLAG
        
        opts = self.model._meta
        app_label = opts.app_label
        # 判断是否有编辑权限或查看权限
        if not self.has_view_or_change_permission(request):
            raise PermissionDenied
        
        try:
            cl = self.get_changelist_instance(request)
        except IncorrectLookupParameters:
            # 给出了古怪的查找参数，重定向到错误页
            if ERROR_FLAG in request.GET:
                return SimpleTemplateResponse(
                    "admin/invalid_setup.html",
                    {
                        "title": _("Database error"),
                    },
                )
            # 跳转回当前页
            return HttpResponseRedirect(request.path + "?" + ERROR_FLAG + "=1")
        
        action_failed = False
        selected = request.POST.getlist(helpers.ACTION_CHECKBOX_NAME)

        actions = self.get_actions(request)
        
    
        return super().changelist_view(request, extra_context)