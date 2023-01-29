from django.contrib import admin

# Register your models here.
from .models import BaykeMenu, BaykePermission


admin.site.register(BaykeMenu)
admin.site.register(BaykePermission)