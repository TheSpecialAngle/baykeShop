from django.urls import path
from baykeshop.views.shop import home
from baykeshop.views.shop import auth
from baykeshop.views.shop import cart
from baykeshop.views.shop import order
from baykeshop.views.shop import user

from baykeshop.pay.alipay.notify import AlipayNotifyView


app_name = "baykeshop"

urlpatterns = [
    # home
    path('', home.HomeView.as_view(), name="home"),
    path("search/", home.SearchView.as_view(), name="search"),
    path('goods/<int:pk>/skus/', home.GoodsListView.as_view(), name='goods'),
    path('goods/<int:pk>/detail/<int:sku_id>/', home.GoodDetailView.as_view(), name='detail'),
    
    # auth
    path('user/login/', auth.LoginView.as_view(), name='login'),
    path("user/register/", auth.RegisterView.as_view(), name="register"),
    path("user/logout/", auth.LogoutView.as_view(), name="logout"),
    
    # cart
    path("user/cart/", cart.BaykeShopCartView.as_view(), name="cart"),
    path("user/order/confirm/", cart.BaykeShopOrderConfirmView.as_view(), name="order_confirm"),
    
    # order
    path("user/orders/", order.BaykeShopOrderListView.as_view(), name="user_orders"),
    path("user/orders/<int:pk>/", order.BaykeShopOrderDetailView.as_view(), name="user_orders_detail"),
    path("user/order/pay/", order.BaykeShopOrderPayView.as_view(), name="order_pay"),
    
    # user
    path("user/userinfo/", user.BaykeUserInfoView.as_view(), name="user_profile"),
    path("user/balance/", user.BaykeUserBalanceView.as_view(), name="user_balance"),
    path("user/address/", user.BaykeAddressView.as_view(), name="user_address"),
    
    # pay,支付宝回调
    path("alipay/", AlipayNotifyView.as_view(), name="alipay_notify"),
    
]