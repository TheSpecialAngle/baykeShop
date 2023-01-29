from django.contrib.admin.apps import AdminConfig


class BaykeAdminConfig(AdminConfig):
    default_site = 'bayke.contrib.admin.BaykeAdminSite'