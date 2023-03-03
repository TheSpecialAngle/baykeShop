from django.urls import path
from baykeshop.public.views import HomeTemplateView

urlpatterns = [
    path("", HomeTemplateView.as_view(), name="home")
]
