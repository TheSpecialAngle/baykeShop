from django.urls import path, include

app_name = "baykeshop"

urlpatterns = [
    path("", include('baykeshop.public.urls')),
    path("user/", include('baykeshop.module.user.urls')),
]
