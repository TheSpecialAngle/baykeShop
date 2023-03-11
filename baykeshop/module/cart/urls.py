from django.urls import path
from baykeshop.module.cart import views

urlpatterns = [
    path("", views.BaykeShopingCartListView.as_view(), name="carts"),
    path("add/", views.BaykeShopingCartCreateView.as_view(), name="add_cart"),
    path("update/num/", views.BaykeShopingCartUpdateView.as_view(), name="update_cart")
]