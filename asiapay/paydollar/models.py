import re

from django.db import models
from asiapay import base


class PaydollarTransaction(base.ResponseModel):

    # The AsiaPay method and version used
    method = models.CharField(max_length=32)
    version = models.CharField(max_length=8)

    # Transaction details used in GetPaydollarCheckout
    amount = models.DecimalField(max_digits=12, decimal_places=2, null=True,
                                 blank=True)
    currency = models.CharField(max_length=8, null=True, blank=True)

    # Response params
    SUCCESS, SUCCESS_WITH_WARNING, FAILURE = 'Success', 'SuccessWithWarning', 'Failure'
    ack = models.CharField(max_length=32)

    correlation_id = models.CharField(max_length=32, null=True, blank=True)
    token = models.CharField(max_length=32, null=True, blank=True)

    error_code = models.CharField(max_length=32, null=True, blank=True)
    error_message = models.CharField(max_length=256, null=True, blank=True)

    class Meta:
        ordering = ('-date_created',)
        app_label = 'asiapay'

    def save(self, *args, **kwargs):
        self.raw_request = re.sub(r'PWD=\d+&', 'PWD=XXXXXX&', self.raw_request)
        return super(PaydollarTransaction, self).save(*args, **kwargs)

    @property
    def is_successful(self):
        return self.ack in (self.SUCCESS, self.SUCCESS_WITH_WARNING)

    def __unicode__(self):
        return u'method: %s: token: %s' % (
            self.method, self.token)

