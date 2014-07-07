"""Tests for the views of the ``user_profiles`` app."""
from django.core.urlresolvers import reverse
from django.test import TestCase

from django_libs.tests.mixins import ViewRequestFactoryTestMixin
from oscar.apps.basket.models import Basket

from . import factories
from .. import models
from .. import views


class FailResponseViewTestCase(ViewRequestFactoryTestMixin, TestCase):
    """Tests for the ``FailResponseView`` view class."""
    view_class = views.FailResponseView

    def setUp(self):
        self.data = {'Ref': '100022'}

    def test_view(self):
        self.is_not_callable(data=self.data)
        self.order = factories.OrderFactory(
            number='100022', status=Basket.FROZEN)
        self.redirects(data=self.data, to=reverse('basket:summary'))


class DataFeedViewTestCase(ViewRequestFactoryTestMixin, TestCase):
    """Tests for the ``DataFeedView`` view class."""
    view_class = views.DataFeedView

    def setUp(self):
        self.data = {
            'payMethod': 'VISA',
            'Cur': '702',
            'prc': '0',
            'AuthId': '574017',
            'panLast4': '5005',
            'successcode': '0',
            'payerAuth': 'U',
            'channelType': 'SPC',
            'Ref': '100022',
            'ipCountry': 'DE',
            'PayRef': '1574017',
            'Ord': '12345678',
            'Holder': 'Testing',
            'Amt': '68.00',
            'TxTime': '2014-07-08 00:54:41.0',
            'eci': '07',
            'src': '0',
            'remark': '',
            'cardIssuingCountry': 'HK',
            'AlertCode': 'R14',
            'panFirst6': '491891',
            'MerchantId': '12103432',
            'expMonth': '7',
            'expYear': '2015',
            'sourceIp': '92.209.35.250',
            'panFirst4': '4918',
        }

    def test_view(self):
        self.is_not_callable(data=self.data)
        self.is_postable(data=self.data, ajax=True)
        self.assertEqual(models.AsiaPayTransaction.objects.count(), 1, msg=(
            'A new transaction should have been saved.'))
