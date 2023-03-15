from django.urls import path, include

app_name = "baykeshop"

urlpatterns = [
    path("", include('baykeshop.public.urls')),
    path("user/", include('baykeshop.module.user.urls')),
    path("goods/", include('baykeshop.module.goods.urls')),
    path("cart/", include('baykeshop.module.cart.urls')),
    path("payment/", include('baykeshop.module.payment.urls')),
    path("order/", include('baykeshop.module.order.urls')),
    path("comments/", include('baykeshop.module.comments.urls')),
]
