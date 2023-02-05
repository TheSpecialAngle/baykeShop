from django.urls import path
from . import views


app_name = "baykeShop"

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('goods/<int:cate_id>/', views.GoodsView.as_view(), name='goods'),
    path('category/<int:pk>/spus/', views.GoodsListView.as_view(), name='category_spus'),
    path('goods/detail-<int:pk>/', views.GoodDetailView.as_view(), name='detail')
]