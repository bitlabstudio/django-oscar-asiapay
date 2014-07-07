"""Views for the custom ``checkout`` app."""
from django import http
from django.conf import settings
from django.core.urlresolvers import reverse
from django.contrib.sites.models import Site

from oscar.apps.checkout.views import (
    PaymentDetailsView as OscarPaymentDetailsView,
)


class PaymentDetailsView(OscarPaymentDetailsView):
    def dispatch(self, request, **kwargs):
        if not self.preview:
            return http.HttpResponseRedirect(reverse('checkout:preview'))
        return super(PaymentDetailsView, self).dispatch(request, **kwargs)

    def get_context_data(self, **kwargs):
        # Add bankcard form to the template context
        context = super(PaymentDetailsView, self).get_context_data(**kwargs)
        if getattr(settings, 'ASIAPAY_LOCALTEST_URL', None):
            host = settings.ASIAPAY_LOCALTEST_URL
        else:
            host = Site.objects.get_current().domain
        scheme = 'https' if getattr(
            settings, 'ASIAPAY_CALLBACK_HTTPS', True) else 'http'
        base_url = '{}://{}'.format(scheme, host)
        success_url = base_url + reverse('asiapay-success-response')
        fail_url = base_url + reverse('asiapay-fail-response')
        context.update({
            'asiapay_url': settings.ASIAPAY_PAYDOLLAR_URL,
            'merchant_id': settings.ASIAPAY_MERCHANT_ID,
            'currency_code': getattr(settings, 'ASIAPAY_CURRENCY_CODE', 702),
            'asiapay_lang': getattr(settings, 'ASIAPAY_LANGUAGE', 'E'),
            'asiapay_paytype': getattr(settings, 'ASIAPAY_PAYTYPE', 'N'),
            'order_number': self.generate_order_number(self.request.basket),
            'success_url': success_url,
            'fail_url': fail_url,
            'error_url': fail_url,
        })
        return context
