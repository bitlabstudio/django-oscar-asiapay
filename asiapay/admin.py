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
        '5005',
        'ip_country',
        'account_holder',
        'transaction_time',
        'eci',
        'pan_first_6',
        'exp_month',
        'exp_year',
        '92.209.35.250',
        'pan_first_4',
    ]


admin.site.register(models.AsiaPayTransaction, AsiaPayTransactionAdmin)
