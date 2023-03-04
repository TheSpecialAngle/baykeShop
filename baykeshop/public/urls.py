from django.urls import path
from baykeshop.public import views

urlpatterns = [
    path("", views.HomeTemplateView.as_view(), name="home"),
    path("search/", views.SearchTemplateView.as_view(), name="search"),
    path("upload/", views.WangEditorUploadImg.as_view(), name="upload")
]
