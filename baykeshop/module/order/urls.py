from django.urls import path
from baykeshop.module.order import views

urlpatterns = [
    path("list/", views.BaykeshopOrderInfoListView.as_view(), name="order_list"),
    path("<int:slug>/", views.BaykeShopOrderInfoDetailView.as_view(), name="order_detail"),
    path("detail/<int:slug>/", views.BaykeShopOrderInfoUserDetailView.as_view(), name="user_order_detail")
]