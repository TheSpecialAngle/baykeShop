from django.contrib import admin
from django.utils.translation import gettext as _
from django.utils.translation import gettext_lazy
from django.contrib.admin.apps import AdminConfig


class BaykeAdminSite(admin.AdminSite):
    
     # Text to put at the end of each page's <title>.
    site_title = gettext_lazy("Django site admin")

    # Text to put in each page's <h1>.
    site_header = gettext_lazy("Django administration")

    # Text to put at the top of the admin index page.
    index_title = gettext_lazy("Site administration")



class BaykeAdminConfig(AdminConfig):
    default_site = "baykeshop.admin.sites.BaykeAdminSite"