from django.contrib import admin
from baykeshop.admin.options import CustomActions, CustomColumns


class BaseModelAdmin(admin.ModelAdmin, CustomColumns):
    """
    继承了django的ModelAdmin
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
    
    # change_list_template = "baykeAdmin/change_list.html"
    actions = ["mark_delete", "export_as_csv"]

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if self.model._meta.model_name not in ['user', 'group', 'permission', 'logentry']:
            return queryset.filter(is_del=False)
        return queryset
    
    def media(self) -> Media:
        return super().media