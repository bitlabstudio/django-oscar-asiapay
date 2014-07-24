"""Models for the ``asiapay`` app."""
from django.db import models
from django.utils.translation import ugettext_lazy as _


class AsiaPayTransaction(models.Model):
    """
    Modal, which contains information about an AsiaPay transaction:

    :payment_method: Method of the payment (e.g. VISA).
    :currency_code: Asiapay currency code.
    :prc: Primary response code (primary bank host status code).
    :src: Secondary response code (primary bank host status code).
    :auth_id: Approval code.
    :success_code: Success code of the transaction.
    :payer_auth: Payer authentication status.
    :channel_type: AsiaPay channel type.
    :order_number: Number of the relevant order.
    :ip_country: Country of payer's IP.
    :payment_reference: PayDollar reference number.
    :bank_reference: Bank reference number (ORD).
    :account_holder: Name of the account holder.
    :amount: Transaction amount.
    :transaction_time: Datetime of the transaction.
    :eci: ECI value (for 3D enabled merchants).
    :remark: Additional remark.
    :card_issuing_country: Card issuing country (marked with an asterisk if on
      high risk country list).
    :alert_code: Alert code of the transaction.
    :merchant_id: Merchant ID (set in settings).
    :exp_month: Expiration month of the card.
    :exp_year: Expiration year of the card.
    :source_ip: IP address of the payer.
    :pan_first_4: First four digits of card.
    :pan_first_6: First six digits of card.
    :pan_last_4: Last four digits of card.

    """
    payment_method = models.CharField(
        verbose_name=_('Payment method'),
        max_length=10,
    )

    currency_code = models.CharField(
        verbose_name=_('Currency'),
        max_length=3,
        choices=(
            ('344', 'HKD'),
            ('156', 'CNY (RMB)'),
            ('036', 'AUD'),
            ('124', 'CAD'),
            ('764', 'THB'),
            ('410', 'KRW'),
            ('784', 'AED'),
            ('356', 'INR'),
            ('840', 'USD'),
            ('392', 'JPY'),
            ('978', 'EUR'),
            ('446', 'MOP'),
            ('458', 'MYR'),
            ('682', 'SAR'),
            ('096', 'BND'),
            ('702', 'SGD'),
            ('901', 'TWD'),
            ('826', 'GBP'),
            ('608', 'PHP'),
            ('360', 'IDR'),
            ('554', 'NZD'),
            ('704', 'VND'),
        )
    )

    prc = models.IntegerField(
        verbose_name=_('Primary bank host status'),
    )

    src = models.IntegerField(
        verbose_name=_('Secondary bank host status'),
    )

    auth_id = models.CharField(
        verbose_name=_('Auth ID'),
        max_length=128,
        blank=True,
    )

    success_code = models.SmallIntegerField(
        verbose_name=_('Success code'),
    )

    payer_auth = models.CharField(
        verbose_name=_('Payer auth status'),
        max_length=1,
        choices=(
            ('Y', '3-D card succeeded'),
            ('N', '3-D card failed'),
            ('P', '3-D secure check pending'),
            ('A', 'Card is not 3-D secure enrolled'),
            ('U', '3-D secure check not processed'),
        )

    )

    channel_type = models.CharField(
        verbose_name=_('AsiaPay channel type'),
        max_length=3,
        choices=(
            ('SPC', 'Client Post Through Browser'),
            ('DPC', 'Direct Client Side Connection'),
            ('DPS', 'Server Side Direct Connection'),
            ('SCH', 'Schedule Payment'),
            ('DPL', 'Direct Payment Link Connection'),
            ('MOT', 'Moto Connection'),
            ('RTL', 'RetailPay Connection'),
            ('BPP', 'Batch Payment Process'),
            ('MOB', 'Mobile Payment Connection'),
        )
    )

    order_number = models.CharField(
        verbose_name=_('Order number'),
        max_length=128,
    )

    ip_country = models.CharField(
        verbose_name=_('Country of payer\'s IP'),
        max_length=3,
    )

    payment_reference = models.BigIntegerField(
        verbose_name=_('Payment Reference'),
    )

    bank_reference = models.BigIntegerField(
        verbose_name=_('Bank reference (ORD)'),
        blank=True, null=True,
    )

    account_holder = models.CharField(
        verbose_name=_('Account holder'),
        max_length=128,
    )

    amount = models.FloatField(
        verbose_name=_('Amount'),
    )

    transaction_time = models.DateTimeField(
        verbose_name=_('Transaction time'),
        blank=True, null=True,
    )

    eci = models.CharField(
        verbose_name=_('ECI'),
        max_length=2,
    )

    remark = models.TextField(
        verbose_name=_('Remark'),
        max_length=1024,
        blank=True,
    )

    card_issuing_country = models.CharField(
        verbose_name=_('Card issuing country'),
        max_length=3,
    )

    alert_code = models.CharField(
        verbose_name=_('Alert code'),
        max_length=50,
        blank=True,
        help_text=_('e.g. R14 - IP Country not match with Issuing Country'),
    )

    merchant_id = models.BigIntegerField(
        verbose_name=_('Merchant ID'),
        blank=True, null=True,
    )

    exp_month = models.PositiveIntegerField(
        verbose_name=_('Expiration month of card'),
        blank=True, null=True,
    )

    exp_year = models.PositiveIntegerField(
        verbose_name=_('Expiration year of card'),
        blank=True, null=True,
    )

    source_ip = models.IPAddressField(
        verbose_name=_('Source IP'),
    )

    pan_first_4 = models.CharField(
        verbose_name=_('First four digits of card'),
        max_length=4,
        blank=True,
    )

    pan_first_6 = models.CharField(
        verbose_name=_('First six digits of card'),
        max_length=6,
        blank=True,
    )

    pan_last_4 = models.CharField(
        verbose_name=_('Last four digits of card'),
        max_length=4,
        blank=True,
    )

    class Meta:
        ordering = ('-transaction_time', )

    def translate_success_code(self):
        if self.success_code == '0':
            return _('Succeeded')
        if self.success_code == '1':
            return _('Failure')
        return _('Error')

    @property
    def is_successful(self):
        return self.prc == '0'

    def __unicode__(self):
        return self.order_number
