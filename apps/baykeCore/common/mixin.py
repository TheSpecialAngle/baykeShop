from django.contrib.auth.mixins import LoginRequiredMixin as BaseLoginRequiredMixin
from django.urls import reverse_lazy


class LoginRequiredMixin(BaseLoginRequiredMixin):
    # 验证类登录
    login_url = reverse_lazy('baykeShop:login')
    redirect_field_name = 'redirect_to'


