"""
This ``urls.py`` is only used when running the tests via ``runtests.py``.
As you know, every app must be hooked into yout main ``urls.py`` so that
you can actually reach the app's views (provided it has any views, of course).

"""
from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static

from oscar.core.loading import get_class


basket_app = get_class('basket.app', 'application')
checkout_app = get_class('checkout.app', 'application')

admin.autodiscover()

urlpatterns = static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += staticfiles_urlpatterns()
urlpatterns += i18n_patterns(
    '',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^shop/basket/', include(basket_app.urls)),
    url(r'^shop/checkout/', include(checkout_app.urls)),
    url(r'^shop/checkout/asiapay/', include('asiapay.urls')),
)
