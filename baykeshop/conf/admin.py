from django.contrib.admin.apps import AdminConfig

class BaykeAdminConfig(AdminConfig):
    """The default AppConfig for admin which does autodiscovery."""

    default = "baykeshop.admin.sites.BaykeAdminSite"