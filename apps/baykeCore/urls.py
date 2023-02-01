from django.urls import path
from . import views

app_name = "bayke"

urlpatterns = [
    path('', views.IndexTemplateView.as_view(), name='index'),
]