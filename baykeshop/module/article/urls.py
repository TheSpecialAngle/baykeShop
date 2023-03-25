from django.urls import path
from baykeshop.module.article import views

urlpatterns = [
    path("", views.BaykeArticleListView.as_view(), name="article_list"),
    path("<int:pk>/", views.BaykeArticleDetailView.as_view(), name="article_detail"),
    path('cate/<int:pk>/', views.BaykeArticleCategoryListView.as_view(), name='article_category_list'),
]