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
    
    path("search/", views.SearchView.as_view(), name="search"),
    
    path("cart/", views.BaykeShopCartView.as_view(), name="cart")
]