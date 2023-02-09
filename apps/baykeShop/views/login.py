from django.contrib.auth.views import (
    LoginView as BaseLoginView,
    LogoutView as BaseLogoutView
)
from django.http.response import JsonResponse

from ..forms import LoginForm


class LoginView(BaseLoginView):
    next_page = 'baykeShop:home'
    form_class = LoginForm
    redirect_field_name = 'redirect_to'
    template_name = "baykeShop/user/login.html"


class LogoutView(BaseLogoutView):
    
    template_name = 'baykeShop/user/logout.html'