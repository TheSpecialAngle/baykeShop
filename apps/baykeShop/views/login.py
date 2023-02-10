from django.contrib.auth.views import (
    LoginView as BaseLoginView,
    LogoutView as BaseLogoutView
)
from django.http.response import JsonResponse

from ..forms import LoginForm


class LoginView(BaseLoginView):
    # 登录
    next_page = 'baykeShop:home'
    form_class = LoginForm
    redirect_field_name = 'redirect_to'
    template_name = "baykeShop/user/login.html"


class LogoutView(BaseLogoutView):
    # 退出
    template_name = 'baykeShop/user/logout.html'