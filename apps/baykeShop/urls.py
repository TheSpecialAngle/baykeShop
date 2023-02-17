from django.urls import path
from . import views


app_name = "baykeShop"

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('goods/<int:pk>/skus/', views.GoodsListView.as_view(), name='goods'),
    path('goods/<int:pk>/detail/<int:sku_id>/', views.GoodDetailView.as_view(), name='detail'),
    
    path('user/login/', views.LoginView.as_view(), name='login'),
    path("user/register/", views.RegisterView.as_view(), name="register"),
    path("user/logout/", views.LogoutView.as_view(), name="logout"),
    path("user/cart/", views.BaykeShopCartView.as_view(), name="cart"),
    path("user/order/confirm/", views.BaykeShopOrderConfirmView.as_view(), name="order_confirm"),
    path("user/order/pay/", views.BaykeShopOrderPayView.as_view(), name="order_pay"),
    
    path("user/userinfo/", views.BaykeUserInfoView.as_view(), name="user_profile"),
    path("user/balance/", views.BaykeUserBalanceView.as_view(), name="user_balance"),
    path("user/address/", views.BaykeAddressView.as_view(), name="user_address"),
    path("user/orders/", views.BaykeShopOrderListView.as_view(), name="user_orders"),
    path("user/orders/<int:pk>/", views.BaykeShopOrderDetailView.as_view(), name="user_orders_detail"),
    
    path("search/", views.SearchView.as_view(), name="search"),
    
]