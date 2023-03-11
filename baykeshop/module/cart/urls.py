from django.urls import path
from baykeshop.module.cart import views

urlpatterns = [
    path("add/", views.BaykeShopingCartCreateView.as_view(), name="add_cart")
]