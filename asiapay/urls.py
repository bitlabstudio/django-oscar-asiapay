"""Urls for the ``asiapay`` app."""
from django.conf.urls import patterns, url

from asiapay import views


urlpatterns = patterns(
    '',
    url(r'^redirect/', views.RedirectView.as_view(), name='asiapay-redirect'),
    url(r'^preview/(?P<basket_id>\d+)/$',
        views.SuccessResponseView.as_view(preview=True),
        name='asiapay-success-response'),
    url(r'^fail/(?P<basket_id>\d+)/$', views.FailResponseView.as_view(),
        name='asiapay-fail-response'),
    url(r'^place-order/(?P<basket_id>\d+)/$',
        views.SuccessResponseView.as_view(),
        name='asiapay-place-order'),
)
