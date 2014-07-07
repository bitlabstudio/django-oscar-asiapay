"""Views for the ``asiapay`` app."""
from decimal import Decimal as D
import httplib
import logging
import urllib
import urllib2
import urlparse

from django.views.generic import RedirectView
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.db.models import get_model
from django.utils.translation import ugettext_lazy as _

from oscar.apps.checkout.views import PaymentDetailsView, CheckoutSessionMixin
from oscar.apps.payment.exceptions import UnableToTakePayment
from oscar.apps.payment.models import SourceType, Source
from oscar.core.loading import get_class

from .facade import get_asiapay_url
from .exceptions import (
    EmptyBasketException, MissingShippingAddressException,
    MissingShippingMethodException)
from asiapay.exceptions import AsiaPayError

ShippingAddress = get_model('order', 'ShippingAddress')
Country = get_model('address', 'Country')
Basket = get_model('basket', 'Basket')
Repository = get_class('shipping.repository', 'Repository')
Applicator = get_class('offer.utils', 'Applicator')
Selector = get_class('partner.strategy', 'Selector')


logger = logging.getLogger('asiapay.paydollar')


class RedirectView(CheckoutSessionMixin, RedirectView):
    """
    Initiate the transaction with Asiapay and redirect the user
    to AsiaPay's Paydollar Checkout to perform the transaction.
    """
    permanent = False

    # Setting to distinguish if the site has already collected a shipping
    # address.  This is False when redirecting to AsiaPay straight from the
    # basket page but True when redirecting from checkout.
    as_payment_method = False

    def get_redirect_url(self, **kwargs):
        try:
            basket = self.request.basket
            url = self._get_redirect_url(basket, **kwargs)
        except AsiaPayError:
            messages.error(self.request, _(
                "An error occurred communicating with AsiaPay"))
            if self.as_payment_method:
                url = reverse('checkout:payment-details')
            else:
                url = reverse('basket:summary')
            return url
        except EmptyBasketException:
            messages.error(self.request, _("Your basket is empty"))
            return reverse('basket:summary')
        except MissingShippingAddressException:
            messages.error(
                self.request, _("A shipping address must be specified"))
            return reverse('checkout:shipping-address')
        except MissingShippingMethodException:
            messages.error(
                self.request, _("A shipping method must be specified"))
            return reverse('checkout:shipping-method')
        else:
            # Transaction successfully registered with AsiaPay.  Now freeze the
            # basket so it can't be edited while the customer is on the AsiaPay
            # site.
            basket.freeze()

            logger.info("Basket #%s - redirecting to %s", basket.id, url)

            return url

    def _get_redirect_url(self, basket, **kwargs):
        if basket.is_empty:
            raise EmptyBasketException()

        params = {
            'basket': basket,
            'shipping_methods': []          # setup a default empty list
        }                                   # to support no_shipping

        user = self.request.user
        if self.as_payment_method:
            if basket.is_shipping_required():
                # Only check for shipping details if required.
                shipping_addr = self.get_shipping_address(basket)
                if not shipping_addr:
                    raise MissingShippingAddressException()

                shipping_method = self.get_shipping_method(
                    basket, shipping_addr)
                if not shipping_method:
                    raise MissingShippingMethodException()

                params['shipping_address'] = shipping_addr
                params['shipping_method'] = shipping_method
                params['shipping_methods'] = []

        else:
            shipping_methods = Repository().get_shipping_methods(user, basket)
            params['shipping_methods'] = shipping_methods

        if settings.DEBUG:
            # Determine the localserver's hostname to use when
            # in testing mode
            params['host'] = self.request.META['HTTP_HOST']

        if user.is_authenticated():
            params['user'] = user

        import ipdb
        ipdb.set_trace()
        url, post_data = get_asiapay_url(**params)
        for key, value in post_data.iteritems():
            post_data[key] = unicode(value).encode('utf-8')
        data = urllib.urlencode(post_data)
        try:
            response = urllib2.urlopen(url, data=data)
        except (
                urllib2.HTTPError,
                urllib2.URLError,
                httplib.HTTPException), ex:
            self.log_error(
                ex, api_url=url, request_data=data,
                transaction=transaction)
        else:
            parsed_response = urlparse.parse_qs(response.read())
        return get_asiapay_url(**params)


class FailResponseView(RedirectView):
    permanent = False

    def get(self, request, *args, **kwargs):
        basket = get_object_or_404(Basket, id=kwargs['basket_id'],
                                   status=Basket.FROZEN)
        basket.thaw()
        logger.info("Payment cancelled (token %s) - basket #%s thawed",
                    request.GET.get('token', '<no token>'), basket.id)
        return super(FailResponseView, self).get(request, *args, **kwargs)

    def get_redirect_url(self, **kwargs):
        messages.error(self.request, _("AsiaPay transaction cancelled"))
        return reverse('basket:summary')


# Upgrading notes: when we drop support for Oscar 0.6, this class can be
# refactored to pass variables around more explicitly (instead of assigning
# things to self so they are accessible in a later method).
class SuccessResponseView(PaymentDetailsView):
    template_name_preview = 'asiapay/paydollar/preview.html'
    preview = True

    # We don't have the usual pre-conditions (Oscar 0.7+)
    pre_conditions = ()

    def get(self, request, *args, **kwargs):
        """
        Fetch details about the successful transaction from AsiaPay.  We use
        these details to show a preview of the order with a 'submit' button to
        place it.
        """
        try:
            self.payer_id = request.GET['PayerID']
            self.token = request.GET['token']
        except KeyError:
            # Manipulation - redirect to basket page with warning message
            logger.warning("Missing GET params on success response page")
            messages.error(
                self.request,
                _("Unable to determine AsiaPay transaction details"))
            return HttpResponseRedirect(reverse('basket:summary'))

        try:
            self.txn = fetch_transaction_details(self.token)
        except AsiaPayError, e:
            logger.warning(
                "Unable to fetch transaction details for token %s: %s",
                self.token, e)
            messages.error(
                self.request, _('A problem occurred communicating with'
                                ' AsiaPay - please try again later'))
            return HttpResponseRedirect(reverse('basket:summary'))

        # Reload frozen basket which is specified in the URL
        kwargs['basket'] = self.load_frozen_basket(kwargs['basket_id'])
        if not kwargs['basket']:
            logger.warning(
                "Unable to load frozen basket with ID %s", kwargs['basket_id'])
            messages.error(
                self.request,
                _("No basket was found that corresponds to your "
                  "AsiaPay transaction"))
            return HttpResponseRedirect(reverse('basket:summary'))

        logger.info(
            "Basket #%s - showing preview with payer ID %s and token %s",
            kwargs['basket'].id, self.payer_id, self.token)

        return super(SuccessResponseView, self).get(request, *args, **kwargs)

    def load_frozen_basket(self, basket_id):
        # Lookup the frozen basket that this txn corresponds to
        try:
            basket = Basket.objects.get(id=basket_id, status=Basket.FROZEN)
        except Basket.DoesNotExist:
            return None

        # Assign strategy to basket instance
        if Selector:
            basket.strategy = Selector().strategy(self.request)

        # Re-apply any offers
        Applicator().apply(self.request, basket)

        return basket

    def get_context_data(self, **kwargs):
        ctx = super(SuccessResponseView, self).get_context_data(**kwargs)

        if not hasattr(self, 'payer_id'):
            return ctx

        # This context generation only runs when in preview mode
        ctx.update({
            'payer_id': self.payer_id,
            'token': self.token,
            'asiapay_user_email': self.txn.value('EMAIL'),
            'asiapay_amount': D(self.txn.value('AMT')),
        })

        return ctx

    def post(self, request, *args, **kwargs):
        """
        Place an order.

        We fetch the txn details again and then proceed with oscar's standard
        payment details view for placing the order.
        """
        error_msg = _(
            "A problem occurred communicating with AsiaPay "
            "- please try again later"
        )
        try:
            self.payer_id = request.POST['payer_id']
            self.token = request.POST['token']
        except KeyError:
            # Probably suspicious manipulation if we get here
            messages.error(self.request, error_msg)
            return HttpResponseRedirect(reverse('basket:summary'))

        try:
            self.txn = fetch_transaction_details(self.token)
        except AsiaPayError:
            # Unable to fetch txn details from AsiaPay - we have to bail out
            messages.error(self.request, error_msg)
            return HttpResponseRedirect(reverse('basket:summary'))

        # Reload frozen basket which is specified in the URL
        basket = self.load_frozen_basket(kwargs['basket_id'])
        if not basket:
            messages.error(self.request, error_msg)
            return HttpResponseRedirect(reverse('basket:summary'))

        submission = self.build_submission(basket=basket)
        return self.submit(**submission)

    def build_submission(self, **kwargs):
        submission = super(
            SuccessResponseView, self).build_submission(**kwargs)
        # Pass the user email so it can be stored with the order
        submission['order_kwargs']['guest_email'] = self.txn.value('EMAIL')
        # Pass PP params
        submission['payment_kwargs']['payer_id'] = self.payer_id
        submission['payment_kwargs']['token'] = self.token
        submission['payment_kwargs']['txn'] = self.txn
        return submission

    # Warning: This method can be removed when we drop support for Oscar 0.6
    def get_error_response(self):
        # We bypass the normal session checks for shipping address and shipping
        # method as they don't apply here.
        pass

    def handle_payment(self, order_number, total, **kwargs):
        """
        Complete payment with AsiaPay - this calls the 'DoPaydollarCheckout'
        method to capture the money from the initial transaction.
        """
        try:
            confirm_txn = confirm_transaction(
                kwargs['payer_id'], kwargs['token'], kwargs['txn'].amount,
                kwargs['txn'].currency)
        except AsiaPayError:
            raise UnableToTakePayment()
        if not confirm_txn.is_successful:
            raise UnableToTakePayment()

        # Record payment source and event
        source_type, is_created = SourceType.objects.get_or_create(
            name='AsiaPay')
        source = Source(source_type=source_type,
                        currency=confirm_txn.currency,
                        amount_allocated=confirm_txn.amount,
                        amount_debited=confirm_txn.amount)
        self.add_payment_source(source)
        self.add_payment_event('Settled', confirm_txn.amount,
                               reference=confirm_txn.correlation_id)
