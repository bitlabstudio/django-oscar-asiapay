"""Admin models for the ``asiapay`` app."""
from django.contrib import admin

from asiapay import models


class AsiaPayTransactionAdmin(admin.ModelAdmin):
    list_display = [
        'payment_method',
        'currency_code',
        'order_number',
        'ip_country',
        'amount',
        'transaction_time',
    ]


admin.site.register(models.AsiaPayTransaction, AsiaPayTransactionAdmin)
