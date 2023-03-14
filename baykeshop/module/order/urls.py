from django.urls import path
from baykeshop.module.order import views

urlpatterns = [
    path("list/", views.BaykeshopOrderInfoListView.as_view(), name="order_list"),
    path("<int:slug>/", views.BaykeShopOrderInfoDetailView.as_view(), name="order_detail"),
]