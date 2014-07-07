"""Tests for the models of the ``user_profiles`` app."""
from django.test import TestCase

from . import factories


class AsiaPayTransactionTestCase(TestCase):
    """Tests for the ``AsiaPayTransaction`` model class."""
    longMessage = True

    def setUp(self):
        self.txn = factories.AsiaPayTransactionFactory()

    def test_instantiation(self):
        """Test instantiation of the ``AsiaPayTransaction`` model."""
        self.assertTrue(self.txn.pk)

    def test_is_successful(self):
        self.assertTrue(self.txn.is_successful, msg=(
            'Should be True, if transaction is successful.'))

    def test_translate_success_code(self):
        self.assertEqual(
            self.txn.translate_success_code().translate('en'),
            'Succeeded', msg=('Should return a success message if code is 0.'))
        self.txn.success_code = '1'
        self.assertEqual(
            self.txn.translate_success_code().translate('en'), 'Failure',
            msg=('Should return a failure message if code is 1.'))
        self.txn.success_code = '2'
        self.assertEqual(
            self.txn.translate_success_code().translate('en'), 'Error',
            msg=('Should return an error message if code is whether 0 nor 1.'))
