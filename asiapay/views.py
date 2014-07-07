"""Views for the ``asiapay`` app."""
import logging

from django.views.generic import RedirectView, View
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponse
from django.db.models import get_model
from django.views.decorators.csrf import csrf_exempt
from django.utils.translation import ugettext_lazy as _

from oscar.apps.checkout.views import PaymentDetailsView
from oscar.core.loading import get_class

from .models import AsiaPayTransaction


ShippingAddress = get_model('order', 'ShippingAddress')
Order = get_model('order', 'Order')
Country = get_model('address', 'Country')
Basket = get_model('basket', 'Basket')
Repository = get_class('shipping.repository', 'Repository')
Applicator = get_class('offer.utils', 'Applicator')
Selector = get_class('partner.strategy', 'Selector')


logger = logging.getLogger('asiapay')


class FailResponseView(RedirectView):
    permanent = False

    def get(self, request, *args, **kwargs):
        try:
            order = Order.objects.get(
                number=request.GET['Ref'], status=Basket.FROZEN)
        except Order.DoesNotExist:
            raise Http404
        order.basket.thaw()
        logger.info("Payment cancelled (token %s) - basket #%s thawed",
                    request.GET.get('token', '<no token>'), order.basket.id)
        return super(FailResponseView, self).get(request, *args, **kwargs)

    def get_redirect_url(self, **kwargs):
        messages.error(self.request, _("AsiaPay transaction cancelled."))
        return reverse('basket:summary')


class SuccessResponseView(PaymentDetailsView):
    permanent = False

    def get(self, request, *args, **kwargs):  # pragma: nocover
        self.handle_place_order_submission(request)
        return super(SuccessResponseView, self).get(request, *args, **kwargs)

    def get_redirect_url(self, **kwargs):  # pragma: nocover
        messages.success(
            self.request, _("Your AsiaPay payment was successful."))
        return reverse('thank-you')


class DataFeedView(View):
    @csrf_exempt
    def dispatch(self, request, **kwargs):
        if not request.method == 'POST':
            raise Http404
        AsiaPayTransaction.objects.create(
            payment_method=request.POST['payMethod'],
            currency_code=request.POST['Cur'],
            prc=request.POST['prc'],
            auth_id=request.POST['AuthId'],
            success_code=request.POST['successcode'],
            payer_auth=request.POST['payerAuth'],
            channel_type=request.POST['channelType'],
            order_number=request.POST['Ref'],
            ip_country=request.POST['ipCountry'],
            payment_reference=request.POST['PayRef'],
            bank_reference=request.POST['Ord'],
            account_holder=request.POST['Holder'],
            amount=request.POST['Amt'],
            transaction_time=request.POST['TxTime'],
            eci=request.POST['eci'],
            src=request.POST['src'],
            remark=request.POST['remark'],
            card_issuing_country=request.POST['cardIssuingCountry'],
            alert_code=request.POST['AlertCode'],
            merchant_id=request.POST['MerchantId'],
            exp_month=request.POST['expMonth'],
            exp_year=request.POST['expYear'],
            source_ip=request.POST['sourceIp'],
            pan_first_4=request.POST['panFirst4'],
            pan_first_6=request.POST['panFirst6'],
            pan_last_4=request.POST['panLast4'],
        )
        return HttpResponse('OK')
