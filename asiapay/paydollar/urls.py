from django.conf.urls import *
from django.views.decorators.csrf import csrf_exempt

from asiapay.paydollar import views


urlpatterns = patterns('',
    # Views for normal flow that starts on the basket page
    url(r'^redirect/', views.RedirectView.as_view(), name='asiapay-redirect'),
    url(r'^preview/(?P<basket_id>\d+)/$',
        views.SuccessResponseView.as_view(preview=True),
        name='asiapay-success-response'),
    url(r'^cancel/(?P<basket_id>\d+)/$', views.CancelResponseView.as_view(),
        name='asiapay-cancel-response'),
    url(r'^place-order/(?P<basket_id>\d+)/$', views.SuccessResponseView.as_view(),
        name='asiapay-place-order'),
    # Callback for getting shipping options for a specific basket
    url(r'^shipping-options/(?P<basket_id>\d+)/',
        csrf_exempt(views.ShippingOptionsView.as_view()),
        name='asiapay-shipping-options'),
    # View for using AsiaPay as a payment method
    url(r'^payment/', views.RedirectView.as_view(as_payment_method=True),
        name='asiapay-direct-payment'),
)
