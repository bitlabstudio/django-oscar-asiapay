"""Factories for the models of the ``asiapay`` app"""
import factory

from oscar.apps.order.models import Order
from oscar.apps.basket.models import Basket

from .. import models


class AsiaPayTransactionFactory(factory.DjangoModelFactory):
    """Factory for the ``AsiaPayTransaction`` model."""
    FACTORY_FOR = models.AsiaPayTransaction

    payment_method = 'VISA'
    currency_code = '702'
    prc = '0'
    auth_id = '574017'
    pan_last_4 = '5005'
    success_code = '0'
    payer_auth = 'U'
    channel_type = 'SPC'
    order_number = '100022'
    ip_country = 'DE'
    payment_reference = '1574017'
    bank_reference = '12345678'
    account_holder = 'Testing'
    amount = '68.00'
    transaction_time = '2014-07-08 00:54:41.0'
    eci = '07'
    src = '0'
    remark = ''
    card_issuing_country = 'HK'
    alert_code = 'R14'
    pan_first_6 = '491891'
    merchant_id = '12103432'
    exp_month = '7'
    exp_year = '2015'
    source_ip = '92.209.35.250'
    pan_first_4 = '4918'


class BasketFactory(factory.DjangoModelFactory):
    """Factory for the ``Basket`` model."""
    FACTORY_FOR = Basket


class OrderFactory(factory.DjangoModelFactory):
    """Factory for the ``Order`` model."""
    FACTORY_FOR = Order

    total_incl_tax = 100
    total_excl_tax = 100
    basket = factory.SubFactory(BasketFactory)
