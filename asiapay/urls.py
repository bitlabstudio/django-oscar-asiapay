"""Urls for the ``asiapay`` app."""
from django.conf.urls import patterns, url

from asiapay import views


urlpatterns = patterns(
    '',
    url(r'^pay-now/$', views.PaymentView.as_view(),
        name='asiapay_pay_now'),
    url(r'^pay-now/(?P<number>\d+)/$', views.PaymentView.as_view(),
        name='asiapay_pay_now'),
    url(r'^data-feed/$', views.DataFeedView.as_view(),
        name='asiapay_data_feed'),
    url(r'^success/$', views.SuccessResponseView.as_view(),
        name='asiapay_success_response'),
    url(r'^fail/$', views.FailResponseView.as_view(),
        name='asiapay_fail_response'),
)
