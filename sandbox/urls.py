from django.conf.urls import patterns, include, url
from django.conf.urls.i18n import i18n_patterns
from django.conf import settings
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static

from apps.app import application
from asiapay.paydollar.dashboard.app import application as paydollar_dashboard

admin.autodiscover()

urlpatterns = patterns(
    '',
    (r'^admin/', include(admin.site.urls)),
    url(r'^i18n/', include('django.conf.urls.i18n')),
)
urlpatterns += i18n_patterns('',
    # AsiaPay Paydollar integration...
    (r'^checkout/asiapay/', include('asiapay.paydollar.urls')),
    # Dashboard views for PayDollar
    (r'^dashboard/asiapay/paydollar/', include(paydollar_dashboard.urls)),
    (r'', include(application.urls)),
)
if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
