from django.urls import path
from baykeshop.module.goods import views

urlpatterns = [
    path("", views.BaykeShopSPUListView.as_view(), name="spus"),
    path("cate/<int:pk>/", views.BaykeShopCategoryDetailView.as_view(), name="cate_detail"),
    path("search/", views.SearchTemplateView.as_view(), name="search"),
    path("spu/<int:pk>/", views.BaykeShopSPUDetailView.as_view(), name="spu_detail"),
]