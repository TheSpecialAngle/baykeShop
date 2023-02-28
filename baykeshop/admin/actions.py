from django.contrib import messages
from django.contrib.admin.decorators import action
from django.utils.translation import gettext as _
from django.utils.translation import gettext_lazy
from django.template.response import TemplateResponse


@action(
    permissions=["change"],
    description=gettext_lazy("Shipped Order %(verbose_name_plural)s"),
)
def shipped_order(modeladmin, request, queryset):
    print(modeladmin, queryset)
    return TemplateResponse(request, "baykeadmin/shipped_order.html", {})