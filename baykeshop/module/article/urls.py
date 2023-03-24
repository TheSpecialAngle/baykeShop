from django.urls import path
from baykeshop.module.article import views

urlpatterns = [
    path("", views.BaykeArticleListView.as_view(), name="article_list"),
    
]