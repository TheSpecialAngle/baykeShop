from django.urls import path
from baykeshop.module.comments import views


urlpatterns = [
    path("<int:slug>/form/", views.BaykeOrderInfoCommentsFormView.as_view(), name="comments_create")
]
