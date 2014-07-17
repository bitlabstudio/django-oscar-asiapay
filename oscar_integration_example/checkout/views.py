"""Views for the custom ``checkout`` app."""
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect

from oscar.apps.checkout.views import (
    PaymentDetailsView as OscarPaymentDetailsView,
)


class PaymentDetailsView(OscarPaymentDetailsView):
    def dispatch(self, request, **kwargs):
        if not self.preview:
            return HttpResponseRedirect(reverse('checkout:preview'))
        return super(PaymentDetailsView, self).dispatch(request, **kwargs)
