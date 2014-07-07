"""Models for the ``asiapay`` app."""
import re

from django.db import models
from django.utils.translation import ugettext_lazy as _


class PaydollarTransaction(models.Model):

    # Debug information
    raw_request = models.TextField(max_length=512)
    raw_response = models.TextField(max_length=512)

    response_time = models.FloatField(
        help_text=_("Response time in milliseconds"))

    date_created = models.DateTimeField(auto_now_add=True)

    # The AsiaPay method and version used
    method = models.CharField(max_length=32)
    version = models.CharField(max_length=8)

    # Transaction details used in GetPaydollarCheckout
    amount = models.DecimalField(max_digits=12, decimal_places=2, null=True,
                                 blank=True)
    currency = models.CharField(max_length=8, null=True, blank=True)

    # Response params
    ack = models.CharField(max_length=32)

    correlation_id = models.CharField(max_length=32, null=True, blank=True)
    token = models.CharField(max_length=32, null=True, blank=True)

    error_code = models.CharField(max_length=32, null=True, blank=True)
    error_message = models.CharField(max_length=256, null=True, blank=True)

    class Meta:
        ordering = ('-date_created',)
        app_label = 'asiapay'

    def response(self):
        return self._as_dl(self.context)
    response.allow_tags = True

    def _as_table(self, params):
        rows = []
        for k, v in sorted(params.items()):
            rows.append(
                '<tbody><tr><th>%s</th><td>%s</td></tr></tbody>' % (k, v[0]))
        return '<table>%s</table>' % ''.join(rows)

    def _as_dl(self, params):
        rows = []
        for k, v in sorted(params.items()):
            rows.append('<dt>%s</dt><dd>%s</dd>' % (k, v[0]))
        return '<dl>%s</dl>' % ''.join(rows)

    def value(self, key, default=None):
        ctx = self.context
        return ctx[key][0].decode('utf8') if key in ctx else default

    def save(self, *args, **kwargs):
        self.raw_request = re.sub(r'PWD=\d+&', 'PWD=XXXXXX&', self.raw_request)
        return super(PaydollarTransaction, self).save(*args, **kwargs)

    @property
    def is_successful(self):
        return self.ack in (self.SUCCESS, self.SUCCESS_WITH_WARNING)

    def __unicode__(self):
        return u'method: %s: token: %s' % (
            self.method, self.token)
