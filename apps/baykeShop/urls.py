from django.urls import path
from . import views


app_name = "baykeShop"

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('goods/<int:pk>/skus/', views.GoodsListView.as_view(), name='goods'),
    path('goods/<int:pk>/detail/<int:sku_id>/', views.GoodDetailView.as_view(), name='detail')
]