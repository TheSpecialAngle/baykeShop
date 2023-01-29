from django.contrib import admin
from baykeAdmin.forms import BaykeAdminLoginForm


class BaykeAdminSite(admin.AdminSite):
    site_header = 'asdasda'
    
    login_form = BaykeAdminLoginForm
    login_template = 'baykeAdmin/login.html'