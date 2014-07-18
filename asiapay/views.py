"""Views for the ``asiapay`` app."""
import logging

from django.views.generic import RedirectView, View, TemplateView
from django.conf import settings
from django.contrib import messages
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.translation import ugettext_lazy as _

from oscar.core.loading import get_model

from .models import AsiaPayTransaction


Basket = get_model('basket', 'Basket')
Order = get_model('order', 'Order')
logger = logging.getLogger('asiapay')


# --- START MIXINS ---
class PaymentFormMixin(object):
    """Mixin to provide context data for the AsiaPay POST form."""
    def dispatch(self, request, *args, **kwargs):
        if 'number' in kwargs:
            try:
                self.order = Order.objects.get(number=kwargs['number'])
            except Order.DoesNotExist:
                raise Http404(_("No order found"))
        elif 'checkout_order_id' in self.request.session:
            self.order = Order._default_manager.get(
                pk=self.request.session['checkout_order_id'])
        else:
            raise Http404(_("No order found"))
        return super(PaymentFormMixin, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        # Add bankcard form to the template context
        context = super(PaymentFormMixin, self).get_context_data(**kwargs)
        if getattr(settings, 'ASIAPAY_LOCALTEST_URL', None):
            host = settings.ASIAPAY_LOCALTEST_URL
        else:
            host = Site.objects.get_current().domain
        scheme = 'https' if getattr(
            settings, 'ASIAPAY_CALLBACK_HTTPS', True) else 'http'
        base_url = '{}://{}'.format(scheme, host)
        success_url = base_url + reverse('asiapay_success_response')
        fail_url = base_url + reverse('asiapay_fail_response')
        context.update({
            'asiapay_url': settings.ASIAPAY_PAYDOLLAR_URL,
            'merchant_id': settings.ASIAPAY_MERCHANT_ID,
            'currency_code': getattr(settings, 'ASIAPAY_CURRENCY_CODE', 702),
            'asiapay_lang': getattr(settings, 'ASIAPAY_LANGUAGE', 'E'),
            'asiapay_paytype': getattr(settings, 'ASIAPAY_PAYTYPE', 'N'),
            'order': self.order,
            'success_url': success_url,
            'fail_url': fail_url,
            'error_url': fail_url,
        })
        try:
            context.update({
                'existing_txn': AsiaPayTransaction.objects.get(
                    order_number=self.order.number),
            })
        except AsiaPayTransaction.DoesNotExist:
            pass
        return context
# --- END MIXINS ---


class PaymentView(PaymentFormMixin, TemplateView):
    template_name = "asiapay/payment.html"


class FailResponseView(RedirectView):
    permanent = False

    def dispatch(self, request, *args, **kwargs):
        # Please check oscar.apps.order.utils.OrderNumberGenerator to
        # understand the order/basket number procedure.
        try:
            basket = Basket.objects.get(
                id=int(request.GET.get('Ref', 0)) - 100000)
        except Basket.DoesNotExist:
            try:
                basket = request.basket
            except AttributeError:
                raise Http404
        basket.thaw()
        logger.info(
            "Payment cancelled - basket #{} thawed".format(basket.id))
        return super(FailResponseView, self).dispatch(request, *args, **kwargs)

    def get_redirect_url(self, **kwargs):
        messages.error(self.request, _("AsiaPay transaction cancelled."))
        return getattr(settings, 'ASIAPAY_FAILURE_REDIRECT', reverse(
            'basket:summary'))


class SuccessResponseView(RedirectView):
    permanent = False

    def dispatch(self, request, *args, **kwargs):
        try:
            Order.objects.get(number=request.GET.get('Ref'))
        except Order.DoesNotExist:
            raise Http404
        return super(SuccessResponseView, self).dispatch(
            request, *args, **kwargs)

    def get_redirect_url(self, **kwargs):
        messages.success(
            self.request, _("Your AsiaPay payment was successful."))
        return getattr(settings, 'ASIAPAY_SUCCESS_REDIRECT', reverse(
            'checkout:thank-you'))


class DataFeedView(View):
    @csrf_exempt
    def dispatch(self, request, **kwargs):
        if request.method == 'POST':
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
