import logging
from decimal import Decimal as D

from django.conf import settings
from django.template.defaultfilters import truncatewords, striptags

from . import models
from . import exceptions


# AsiaPay methods
SET_PAYDOLLAR_CHECKOUT = 'SetPaydollarCheckout'
GET_PAYDOLLAR_CHECKOUT = 'GetPaydollarCheckoutDetails'
DO_PAYDOLLAR_CHECKOUT = 'DoPaydollarCheckoutPayment'
DO_CAPTURE = 'DoCapture'
DO_VOID = 'DoVoid'
REFUND_TRANSACTION = 'RefundTransaction'

SALE, AUTHORIZATION, ORDER = 'Sale', 'Authorization', 'Order'

logger = logging.getLogger('asiapay')


def _format_description(description):
    if description:
        return truncatewords(striptags(description), 12)
    return ''


def _format_currency(amt):
    return amt.quantize(D('0.01'))


def _fetch_response(method, params):
    """
    Fetch the response from AsiaPay and return a transaction object
    """
    url = settings.ASIAPAY_PAYDOLLAR_URL

    # Print easy-to-read version of params for debugging
    param_list = params.items()
    param_list.sort()
    param_str = "\n".join(["%s: %s" % x for x in param_list])
    logger.debug("Making %s request to %s with params:\n%s", method, url,
                 param_str)

    params = {
        'currCode': getattr(settings, 'ASIAPAY_CURRENCY_CODE', '702'),
        'lang': getattr(settings, 'ASIAPAY_LANGUAGE', 'E'),
        'merchantId': settings.ASIAPAY_MERCHANT_ID,
        'amount': 1,
        'orderRef': '00000005',
    }
    # Make HTTP request
    pairs = gateway.post(url, params)

    pairs_str = "\n".join(["%s: %s" % x for x in sorted(pairs.items())
                           if not x[0].startswith('_')])
    logger.debug("Response with params:\n%s", pairs_str)

    # Record transaction data - we save this model whether the txn
    # was successful or not
    txn = models.PaydollarTransaction(
        method=method,
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


def set_txn(basket, shipping_methods, currency, success_url, fail_url,
            update_url=None, action=SALE, user=None, user_address=None,
            shipping_method=None, shipping_address=None, no_shipping=False):
    import ipdb
    ipdb.set_trace()
    amount = basket.total_incl_tax
    if amount <= 0:
        msg = 'Zero value basket is not allowed'
        logger.error(msg)
        raise exceptions.AsiaPayError(msg)

    params = {
        'currCode': getattr(settings, 'ASIAPAY_CURRENCY_CODE', '702'),
        'lang': getattr(settings, 'ASIAPAY_LANGUAGE', 'E'),
        'merchantId': settings.ASIAPAY_MERCHANT_ID,
        'amount': amount,
        'failUrl': fail_url,
        'successUrl': success_url,
        'orderRef': '00000005',
    }

    url = settings.ASIAPAY_PAYDOLLAR_URL
    return url, params


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
