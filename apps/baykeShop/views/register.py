from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth import authenticate, login
from django.views.generic import FormView
from django.urls import reverse_lazy

from baykeShop.models import BaykeUserInfo
from ..forms import RegisterForm


class RegisterView(SuccessMessageMixin, FormView):
    """
    注册用户 
    """
    template_name = 'baykeShop/user/register.html'
    form_class = RegisterForm
    success_url = reverse_lazy("baykeShop:home")
    success_message = "%(username)s 注册成功，已登录！"
    
    def form_valid(self, form):
        if form.is_valid():
            new_user = form.save()
            auth_user = authenticate(username=new_user.username, 
                                     password=form.cleaned_data['password1'])
            BaykeUserInfo.objects.create(owner=auth_user, nickname=auth_user.username)
            login(self.request, auth_user)
        return super().form_valid(form)

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(
            cleaned_data,
            username=cleaned_data['username'],
        )