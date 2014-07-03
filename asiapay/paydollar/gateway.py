import urllib
import logging
from decimal import Decimal as D

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.utils.translation import ugettext as _
from django.template.defaultfilters import truncatewords, striptags
from localflavor.us import us_states

from asiapay.paydollar import models
from asiapay import gateway
from asiapay import exceptions


# AsiaPay methods
SET_PAYDOLLAR_CHECKOUT = 'SetPaydollarCheckout'
GET_PAYDOLLAR_CHECKOUT = 'GetPaydollarCheckoutDetails'
DO_PAYDOLLAR_CHECKOUT = 'DoPaydollarCheckoutPayment'
DO_CAPTURE = 'DoCapture'
DO_VOID = 'DoVoid'
REFUND_TRANSACTION = 'RefundTransaction'

SALE, AUTHORIZATION, ORDER = 'Sale', 'Authorization', 'Order'

# It's quite difficult to work out what the latest version of the AsiaPay
# Paydollar API is.  The best way is to look for the 'web version: ...' string in
# the source of https://www.sandbox.asiapay.com/
API_VERSION = getattr(settings, 'ASIAPAY_API_VERSION', '88.0')

logger = logging.getLogger('asiapay.paydollar')


def _format_description(description):
    if description:
        return truncatewords(striptags(description), 12)
    return ''


def _format_currency(amt):
    return amt.quantize(D('0.01'))


def _fetch_response(method, extra_params):
    """
    Fetch the response from AsiaPay and return a transaction object
    """
    # Build parameter string
    params = {
        'METHOD': method,
        'VERSION': API_VERSION,
        'USER': settings.ASIAPAY_API_USERNAME,
        'PWD': settings.ASIAPAY_API_PASSWORD,
        'SIGNATURE': settings.ASIAPAY_API_SIGNATURE,
    }
    params.update(extra_params)

    if getattr(settings, 'ASIAPAY_SANDBOX_MODE', True):
        url = 'https://api-3t.sandbox.asiapay.com/nvp'
    else:
        url = 'https://api-3t.asiapay.com/nvp'

    # Print easy-to-read version of params for debugging
    param_list = params.items()
    param_list.sort()
    param_str = "\n".join(["%s: %s" % x for x in param_list])
    logger.debug("Making %s request to %s with params:\n%s", method, url,
                 param_str)

    # Make HTTP request
    pairs = gateway.post(url, params)

    pairs_str = "\n".join(["%s: %s" % x for x in sorted(pairs.items())
                           if not x[0].startswith('_')])
    logger.debug("Response with params:\n%s", pairs_str)

    # Record transaction data - we save this model whether the txn
    # was successful or not
    txn = models.PaydollarTransaction(
        method=method,
        version=API_VERSION,
        ack=pairs['ACK'],
        raw_request=pairs['_raw_request'],
        raw_response=pairs['_raw_response'],
        response_time=pairs['_response_time'],
    )
    if txn.is_successful:
        txn.correlation_id = pairs['CORRELATIONID']
        if method == SET_PAYDOLLAR_CHECKOUT:
            txn.amount = params['PAYMENTREQUEST_0_AMT']
            txn.currency = params['PAYMENTREQUEST_0_CURRENCYCODE']
            txn.token = pairs['TOKEN']
        elif method == GET_PAYDOLLAR_CHECKOUT:
            txn.token = params['TOKEN']
            txn.amount = D(pairs['PAYMENTREQUEST_0_AMT'])
            txn.currency = pairs['PAYMENTREQUEST_0_CURRENCYCODE']
        elif method == DO_PAYDOLLAR_CHECKOUT:
            txn.token = params['TOKEN']
            txn.amount = D(pairs['PAYMENTINFO_0_AMT'])
            txn.currency = pairs['PAYMENTINFO_0_CURRENCYCODE']
    else:
        # There can be more than one error, each with its own number.
        if 'L_ERRORCODE0' in pairs:
            txn.error_code = pairs['L_ERRORCODE0']
        if 'L_LONGMESSAGE0' in pairs:
            txn.error_message = pairs['L_LONGMESSAGE0']
    txn.save()

    if not txn.is_successful:
        msg = "Error %s - %s" % (txn.error_code, txn.error_message)
        logger.error(msg)
        raise exceptions.AsiaPayError(msg)

    return txn


def set_txn(basket, shipping_methods, currency, return_url, cancel_url, update_url=None,
            action=SALE, user=None, user_address=None, shipping_method=None,
            shipping_address=None, no_shipping=False, asiapay_params=None):
    """
    Register the transaction with AsiaPay to get a token which we use in the
    redirect URL.  This is the 'SetPaydollarCheckout' from their documentation.

    There are quite a few options that can be passed to AsiaPay to configure
    this request - most are controlled by ASIAPAY_* settings.
    """
    # Default parameters (taken from global settings).  These can be overridden
    # and customised using the asiapay_params parameter.
    _params = {
        'CUSTOMERSERVICENUMBER': getattr(
            settings, 'ASIAPAY_CUSTOMER_SERVICES_NUMBER', None),
        'SOLUTIONTYPE': getattr(settings, 'ASIAPAY_SOLUTION_TYPE', None),
        'LANDINGPAGE': getattr(settings, 'ASIAPAY_LANDING_PAGE', None),
        'BRANDNAME': getattr(settings, 'ASIAPAY_BRAND_NAME', None),

        # Display settings
        'PAGESTYLE': getattr(settings, 'ASIAPAY_PAGESTYLE', None),
        'HDRIMG': getattr(settings, 'ASIAPAY_HEADER_IMG', None),

        # Think these settings maybe deprecated in latest version of AsiaPay's
        # API
        'HDRBACKCOLOR': getattr(settings, 'ASIAPAY_HEADER_BACK_COLOR', None),
        'HDRBORDERCOLOR': getattr(
            settings, 'ASIAPAY_HEADER_BORDER_COLOR', None),

        'LOCALECODE': getattr(settings, 'ASIAPAY_LOCALE', None),

        'ALLOWNOTE': getattr(settings, 'ASIAPAY_ALLOW_NOTE', True),
        'CALLBACKTIMEOUT': getattr(settings, 'ASIAPAY_CALLBACK_TIMEOUT', 3)
    }
    confirm_shipping_addr = getattr(settings, 'ASIAPAY_CONFIRM_SHIPPING', None)
    if confirm_shipping_addr and not no_shipping:
        _params['REQCONFIRMSHIPPING'] = 1
    if asiapay_params:
        _params.update(asiapay_params)

    locale = _params.get('LOCALECODE', None)
    if locale:
        valid_choices = ('AU', 'DE', 'FR', 'GB', 'IT', 'ES', 'JP', 'US')
        if locale not in valid_choices:
            raise ImproperlyConfigured(
                "'%s' is not a valid locale code" % locale)

    # Boolean values become integers
    _params.update((k, int(v)) for k, v in _params.iteritems() if isinstance(v, bool))

    # Remove None values
    params = dict((k, v) for k, v in _params.iteritems() if v is not None)

    # AsiaPay have an upper limit on transactions.  It's in dollars which is a
    # fiddly to work with.  Lazy solution - only check when dollars are used as
    # the AsiaPay currency.
    amount = basket.total_incl_tax
    if currency == 'USD' and amount > 10000:
        msg = 'AsiaPay can only be used for orders up to 10000 USD'
        logger.error(msg)
        raise exceptions.AsiaPayError(msg)

    if amount <= 0:
        msg = 'Zero value basket is not allowed'
        logger.error(msg)
        raise exceptions.AsiaPayError(msg)

    # PAYMENTREQUEST_0_AMT should include tax, shipping and handling
    params.update({
        'PAYMENTREQUEST_0_AMT': amount,
        'PAYMENTREQUEST_0_CURRENCYCODE': currency,
        'RETURNURL': return_url,
        'CANCELURL': cancel_url,
        'PAYMENTREQUEST_0_PAYMENTACTION': action,
    })

    # Add item details
    index = 0
    for index, line in enumerate(basket.all_lines()):
        product = line.product
        params['L_PAYMENTREQUEST_0_NAME%d' % index] = product.get_title()
        params['L_PAYMENTREQUEST_0_NUMBER%d' % index] = (product.upc if
                                                         product.upc else '')
        desc = ''
        if product.description:
            desc = _format_description(product.description)
        params['L_PAYMENTREQUEST_0_DESC%d' % index] = desc
        # Note, we don't include discounts here - they are handled as separate
        # lines - see below
        params['L_PAYMENTREQUEST_0_AMT%d' % index] = _format_currency(
            line.unit_price_incl_tax)
        params['L_PAYMENTREQUEST_0_QTY%d' % index] = line.quantity

    # If the order has discounts associated with it, the way AsiaPay suggests
    # using the API is to add a separate item for the discount with the value
    # as a negative price.  See "Integrating Order Details into the Paydollar
    # Checkout Flow"
    # https://cms.asiapay.com/us/cgi-bin/?cmd=_render-content&content_ID=developer/e_howto_api_ECCustomizing

    # Iterate over the 3 types of discount that can occur
    for discount in basket.offer_discounts:
        index += 1
        name = _("Special Offer: %s") % discount['name']
        params['L_PAYMENTREQUEST_0_NAME%d' % index] = name
        params['L_PAYMENTREQUEST_0_DESC%d' % index] = _format_description(name)
        params['L_PAYMENTREQUEST_0_AMT%d' % index] = _format_currency(
            -discount['discount'])
        params['L_PAYMENTREQUEST_0_QTY%d' % index] = 1
    for discount in basket.voucher_discounts:
        index += 1
        name = "%s (%s)" % (discount['voucher'].name,
                            discount['voucher'].code)
        params['L_PAYMENTREQUEST_0_NAME%d' % index] = name
        params['L_PAYMENTREQUEST_0_DESC%d' % index] = _format_description(name)
        params['L_PAYMENTREQUEST_0_AMT%d' % index] = _format_currency(
            -discount['discount'])
        params['L_PAYMENTREQUEST_0_QTY%d' % index] = 1
    for discount in basket.shipping_discounts:
        index += 1
        name = _("Shipping Offer: %s") % discount['name']
        params['L_PAYMENTREQUEST_0_NAME%d' % index] = name
        params['L_PAYMENTREQUEST_0_DESC%d' % index] = _format_description(name)
        params['L_PAYMENTREQUEST_0_AMT%d' % index] = _format_currency(
            -discount['discount'])
        params['L_PAYMENTREQUEST_0_QTY%d' % index] = 1

    # We include tax in the prices rather than separately as that's how it's
    # done on most British/Australian sites.  Will need to refactor in the
    # future no doubt.

    # Note that the following constraint must be met
    #
    # PAYMENTREQUEST_0_AMT = (
    #     PAYMENTREQUEST_0_ITEMAMT +
    #     PAYMENTREQUEST_0_TAXAMT +
    #     PAYMENTREQUEST_0_SHIPPINGAMT +
    #     PAYMENTREQUEST_0_HANDLINGAMT)
    #
    # Hence, if tax is to be shown then it has to be aggregated up to the order
    # level.
    params['PAYMENTREQUEST_0_ITEMAMT'] = _format_currency(
        basket.total_incl_tax)
    params['PAYMENTREQUEST_0_TAXAMT'] = _format_currency(D('0.00'))

    # Instant update callback information
    if update_url:
        params['CALLBACK'] = update_url

    # Contact details and address details - we provide these as it would make
    # the AsiaPay registration process smoother is the user doesn't already have
    # an account.
    if user:
        params['EMAIL'] = user.email
    if user_address:
        params['SHIPTONAME'] = user_address.name
        params['SHIPTOSTREET'] = user_address.line1
        params['SHIPTOSTREET2'] = user_address.line2
        params['SHIPTOCITY'] = user_address.line4
        params['SHIPTOSTATE'] = user_address.state
        params['SHIPTOZIP'] = user_address.postcode
        params['SHIPTOCOUNTRYCODE'] = user_address.country.iso_3166_1_a2

    # Shipping details (if already set) - we override the SHIPTO* fields and
    # set a flag to indicate that these can't be altered on the AsiaPay side.
    if shipping_method and shipping_address:
        params['ADDROVERRIDE'] = 1
        # It's recommend not to set 'confirmed shipping' if supplying the
        # shipping address directly.
        params['REQCONFIRMSHIPPING'] = 0
        params['SHIPTONAME'] = shipping_address.name
        params['SHIPTOSTREET'] = shipping_address.line1
        params['SHIPTOSTREET2'] = shipping_address.line2
        params['SHIPTOCITY'] = shipping_address.line4
        params['SHIPTOSTATE'] = shipping_address.state
        params['SHIPTOZIP'] = shipping_address.postcode
        params['SHIPTOCOUNTRYCODE'] = shipping_address.country.iso_3166_1_a2

        # For US addresses, we need to try and convert the state into 2 letter
        # code - otherwise we can get a 10736 error as the shipping address and
        # zipcode don't match the state. Very silly really.
        if params['SHIPTOCOUNTRYCODE'] == 'US':
            key = params['SHIPTOSTATE'].lower().strip()
            if key in us_states.STATES_NORMALIZED:
                params['SHIPTOSTATE'] = us_states.STATES_NORMALIZED[key]

    elif no_shipping:
        params['NOSHIPPING'] = 1

    # Shipping charges
    params['PAYMENTREQUEST_0_SHIPPINGAMT'] = _format_currency(D('0.00'))
    max_charge = D('0.00')
    for index, method in enumerate(shipping_methods):
        is_default = index == 0
        params['L_SHIPPINGOPTIONISDEFAULT%d' % index] = 'true' if is_default else 'false'
        charge = method.charge_incl_tax
        if charge > max_charge:
            max_charge = charge
        if is_default:
            params['PAYMENTREQUEST_0_SHIPPINGAMT'] = _format_currency(charge)
            params['PAYMENTREQUEST_0_AMT'] += charge
        params['L_SHIPPINGOPTIONNAME%d' % index] = unicode(method.name)
        params['L_SHIPPINGOPTIONAMOUNT%d' % index] = _format_currency(charge)

    # Set shipping charge explicitly if it has been passed
    if shipping_method:
        max_charge = charge = shipping_method.charge_incl_tax
        params['PAYMENTREQUEST_0_SHIPPINGAMT'] = _format_currency(charge)
        params['PAYMENTREQUEST_0_AMT'] += charge

    # Both the old version (MAXAMT) and the new version (PAYMENT...) are needed
    # here - think it's a problem with the API.
    params['PAYMENTREQUEST_0_MAXAMT'] = _format_currency(amount + max_charge)
    params['MAXAMT'] = _format_currency(amount + max_charge)

    # Handling set to zero for now - I've never worked on a site that needed a
    # handling charge.
    params['PAYMENTREQUEST_0_HANDLINGAMT'] = _format_currency(D('0.00'))

    # Ensure that the total is formatted correctly.
    params['PAYMENTREQUEST_0_AMT'] = _format_currency(
        params['PAYMENTREQUEST_0_AMT'])

    txn = _fetch_response(SET_PAYDOLLAR_CHECKOUT, params)

    # Construct return URL
    if getattr(settings, 'ASIAPAY_SANDBOX_MODE', True):
        url = 'https://www.sandbox.asiapay.com/webscr'
    else:
        url = 'https://www.asiapay.com/webscr'
    params = (('cmd', '_paydollar-checkout'),
              ('token', txn.token),)
    return '%s?%s' % (url, urllib.urlencode(params))


def get_txn(token):
    """
    Fetch details of a transaction from AsiaPay using the token as
    an identifier.
    """
    return _fetch_response(GET_PAYDOLLAR_CHECKOUT, {'TOKEN': token})


def do_txn(payer_id, token, amount, currency, action=SALE):
    """
    DoPaydollarCheckoutPayment
    """
    params = {
        'PAYERID': payer_id,
        'TOKEN': token,
        'PAYMENTREQUEST_0_AMT': amount,
        'PAYMENTREQUEST_0_CURRENCYCODE': currency,
        'PAYMENTREQUEST_0_PAYMENTACTION': action,
    }
    return _fetch_response(DO_PAYDOLLAR_CHECKOUT, params)


def do_capture(txn_id, amount, currency, complete_type='Complete',
               note=None):
    """
    Capture payment from a previous transaction

    See https://cms.asiapay.com/uk/cgi-bin/?&cmd=_render-content&content_ID=developer/e_howto_api_soap_r_DoCapture
    """
    params = {
        'AUTHORIZATIONID': txn_id,
        'AMT': amount,
        'CURRENCYCODE': currency,
        'COMPLETETYPE': complete_type,
    }
    if note:
        params['NOTE'] = note
    return _fetch_response(DO_CAPTURE, params)


def do_void(txn_id, note=None):
    params = {
        'AUTHORIZATIONID': txn_id,
    }
    if note:
        params['NOTE'] = note
    return _fetch_response(DO_VOID, params)


FULL_REFUND = 'Full'
PARTIAL_REFUND = 'Partial'
def refund_txn(txn_id, is_partial=False, amount=None, currency=None):
    params = {
        'TRANSACTIONID': txn_id,
        'REFUNDTYPE': PARTIAL_REFUND if is_partial else FULL_REFUND,
    }
    if is_partial:
        params['AMT'] = amount
        params['CURRENCYCODE'] = currency
    return _fetch_response(REFUND_TRANSACTION, params)
