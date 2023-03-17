from django.urls import path
from baykeshop.module.payment import views

from baykeshop.module.payment.alipay.notify import AlipayNotifyView

urlpatterns = [
    path("", views.CashRegisterTemplateView.as_view(), name="cash_register"),
    path("paynow/", views.PayNowView.as_view(), name="pay_now"),
    
    path("notify/", AlipayNotifyView.as_view(), name='alipay_notify')
]