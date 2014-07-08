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

from .models import AsiaPayTransaction


Basket = get_model('basket', 'Basket')
logger = logging.getLogger('asiapay')


class FailResponseView(RedirectView):
    permanent = False

    def get(self, request, *args, **kwargs):
        # Please check oscar.apps.order.utils.OrderNumberGenerator to
        # understand the order/basket number procedure.
        try:
            basket = Basket.objects.get(id=int(request.GET['Ref']) - 100000)
        except Basket.DoesNotExist:
            raise Http404
        basket.thaw()
        logger.info("Payment cancelled (token %s) - basket #%s thawed",
                    request.GET.get('token', '<no token>'), basket.id)
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
            payment_method=request.POST.get('payMethod'),
            currency_code=request.POST.get('Cur'),
            prc=request.POST.get('prc'),
            auth_id=request.POST.get('AuthId'),
            success_code=request.POST.get('successcode'),
            payer_auth=request.POST.get('payerAuth'),
            channel_type=request.POST.get('channelType'),
            order_number=request.POST.get('Ref'),
            ip_country=request.POST.get('ipCountry'),
            payment_reference=request.POST.get('PayRef'),
            bank_reference=request.POST.get('Ord') or None,
            account_holder=request.POST.get('Holder'),
            amount=request.POST.get('Amt'),
            transaction_time=request.POST.get('TxTime'),
            eci=request.POST.get('eci'),
            src=request.POST.get('src'),
            remark=request.POST.get('remark'),
            card_issuing_country=request.POST.get('cardIssuingCountry'),
            alert_code=request.POST.get('AlertCode'),
            merchant_id=request.POST.get('MerchantId'),
            exp_month=request.POST.get('expMonth'),
            exp_year=request.POST.get('expYear'),
            source_ip=request.POST.get('sourceIp'),
            pan_first_4=request.POST.get('panFirst4') or '',
            pan_first_6=request.POST.get('panFirst6') or '',
            pan_last_4=request.POST.get('panLast4') or '',
        )
        return HttpResponse('OK')
