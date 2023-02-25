from django import forms
from django.contrib import admin
from django.contrib.admin.options import PermissionDenied
from django.template.response import TemplateResponse
from django.http.response import HttpResponseRedirect
from django.utils.translation import gettext as _

from baykeshop.models import BaykePermission
from baykeshop.forms.admin.action import ActionForm
from baykeshop.admin.options import CustomActions, CustomColumns


class BaseModelAdmin(admin.ModelAdmin):
    """继承了django的ModelAdmin
    重写并新增了一些全局方法
    """
    
    # change_list_template = "baykeadmin/change_list.html"
    actions = ["mark_delete", "export_as_csv"]
    action_form = ActionForm

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if self.model._meta.model_name not in ['user', 'group', 'permission', 'logentry']:
            return queryset.filter(is_del=False)
        return queryset
    
    def change_view(self, request, object_id, form_url="", extra_context=None):
        return super().change_view(request, object_id, form_url, extra_context)