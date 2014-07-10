"""Urls for the ``asiapay`` app."""
from django.conf.urls import patterns, url

from asiapay import views


urlpatterns = patterns(
    '',
    url(r'^pay-now/$', views.PaymentView.as_view(),
        name='asiapay-pay-now'),
    url(r'^data-feed/$', views.DataFeedView.as_view(),
        name='asiapay-data-feed'),
    url(r'^success/$', views.SuccessResponseView.as_view(),
        name='asiapay-success-response'),
    url(r'^fail/$', views.FailResponseView.as_view(),
        name='asiapay-fail-response'),
)
