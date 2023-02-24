from django.contrib import admin
from django.utils.translation import gettext as _
from django.utils.translation import gettext_lazy
from django.contrib.admin.apps import AdminConfig
from django import forms
from django.apps import apps


class BaykeAdminSite(admin.AdminSite):
    
     # Text to put at the end of each page's <title>.
    site_title = gettext_lazy("Django site admin")

    # Text to put in each page's <h1>.
    site_header = gettext_lazy("Django administration")

    # Text to put at the top of the admin index page.
    index_title = gettext_lazy("Site administration")
    
    index_template = "baykeadmin/index.html"
    
    class Media:
        css = {
            "all": ("baykeshop/css/buefy.min.css",)
        }
        js = (
            "baykeshop/js/vue.js",
            "baykeshop/js/buefy.min.js",
            "baykeadmin/js/request.js",
        )
    
    def get_app_list(self, request, app_label=None):
        return super().get_app_list(request)
    
    def index(self, request, extra_context=None):
        extra_context = {"media": self.media}
        return super().index(request, extra_context)
    
    def each_context(self, request):
        return super().each_context(request)
    
    @property
    def media(self):
        return forms.Media(self.Media)



class BaykeAdminConfig(AdminConfig):
    default_site = "baykeshop.conf.sites.BaykeAdminSite"