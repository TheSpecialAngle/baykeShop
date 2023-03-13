from django.urls import path
from baykeshop.module.user import views

urlpatterns = [
    path("login/", views.LoginView.as_view(), name="login"),
    path("register/", views.RegisterView.as_view(), name="register"),
    path("logout/", views.LogoutView.as_view(), name="logout"),
    path("add/address/", views.BaykeShopAddressCreateView.as_view(), name="add_address"),
    
    path("userinfo/", views.BaykeUserInfoTemplateView.as_view(), name="userinfo"),
    
    path("balance/", views.BaykeUserBalanceLogTemplateView.as_view(), name="balance"),
]
