from django.urls import path
from baykeshop.module.payment import views

urlpatterns = [
    path("", views.CashRegisterTemplateView.as_view(), name="cash_register"),
]