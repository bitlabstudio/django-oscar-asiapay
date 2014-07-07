"""Exceptions for the ``asiapay`` app."""
try:
    from oscar.apps.payment.exceptions import PaymentError
except ImportError:
    class PaymentError(Exception):
        pass


class AsiaPayError(PaymentError):
    pass


class EmptyBasketException(Exception):
    pass


class MissingShippingAddressException(Exception):
    pass


class MissingShippingMethodException(Exception):
    pass
