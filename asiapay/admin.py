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
    readonly_fields = [
        'payment_method',
        'auth_id',
        'pan_last_4',
        'ip_country',
        'account_holder',
        'transaction_time',
        'eci',
        'pan_first_6',
        'exp_month',
        'exp_year',
        'source_ip',
        'pan_first_4',
    ]


admin.site.register(models.AsiaPayTransaction, AsiaPayTransactionAdmin)
