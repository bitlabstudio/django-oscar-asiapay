# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AsiaPayTransaction',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('payment_method', models.CharField(max_length=10, verbose_name='Payment method')),
                ('currency_code', models.CharField(max_length=3, verbose_name='Currency', choices=[(b'344', b'HKD'), (b'156', b'CNY (RMB)'), (b'036', b'AUD'), (b'124', b'CAD'), (b'764', b'THB'), (b'410', b'KRW'), (b'784', b'AED'), (b'356', b'INR'), (b'840', b'USD'), (b'392', b'JPY'), (b'978', b'EUR'), (b'446', b'MOP'), (b'458', b'MYR'), (b'682', b'SAR'), (b'096', b'BND'), (b'702', b'SGD'), (b'901', b'TWD'), (b'826', b'GBP'), (b'608', b'PHP'), (b'360', b'IDR'), (b'554', b'NZD'), (b'704', b'VND')])),
                ('prc', models.IntegerField(verbose_name='Primary bank host status')),
                ('src', models.IntegerField(verbose_name='Secondary bank host status')),
                ('auth_id', models.CharField(max_length=128, verbose_name='Auth ID', blank=True)),
                ('success_code', models.SmallIntegerField(verbose_name='Success code')),
                ('payer_auth', models.CharField(max_length=1, verbose_name='Payer auth status', choices=[(b'Y', b'3-D card succeeded'), (b'N', b'3-D card failed'), (b'P', b'3-D secure check pending'), (b'A', b'Card is not 3-D secure enrolled'), (b'U', b'3-D secure check not processed')])),
                ('channel_type', models.CharField(max_length=3, verbose_name='AsiaPay channel type', choices=[(b'SPC', b'Client Post Through Browser'), (b'DPC', b'Direct Client Side Connection'), (b'DPS', b'Server Side Direct Connection'), (b'SCH', b'Schedule Payment'), (b'DPL', b'Direct Payment Link Connection'), (b'MOT', b'Moto Connection'), (b'RTL', b'RetailPay Connection'), (b'BPP', b'Batch Payment Process'), (b'MOB', b'Mobile Payment Connection')])),
                ('order_number', models.CharField(max_length=128, verbose_name='Order number')),
                ('ip_country', models.CharField(max_length=3, verbose_name="Country of payer's IP")),
                ('payment_reference', models.BigIntegerField(verbose_name='Payment Reference')),
                ('bank_reference', models.BigIntegerField(null=True, verbose_name='Bank reference (ORD)', blank=True)),
                ('account_holder', models.CharField(max_length=128, verbose_name='Account holder')),
                ('amount', models.FloatField(verbose_name='Amount')),
                ('transaction_time', models.DateTimeField(null=True, verbose_name='Transaction time', blank=True)),
                ('eci', models.CharField(max_length=2, verbose_name='ECI')),
                ('remark', models.TextField(max_length=1024, verbose_name='Remark', blank=True)),
                ('card_issuing_country', models.CharField(max_length=3, verbose_name='Card issuing country')),
                ('alert_code', models.CharField(help_text='e.g. R14 - IP Country not match with Issuing Country', max_length=50, verbose_name='Alert code', blank=True)),
                ('merchant_id', models.BigIntegerField(null=True, verbose_name='Merchant ID', blank=True)),
                ('exp_month', models.PositiveIntegerField(null=True, verbose_name='Expiration month of card', blank=True)),
                ('exp_year', models.PositiveIntegerField(null=True, verbose_name='Expiration year of card', blank=True)),
                ('source_ip', models.IPAddressField(verbose_name='Source IP')),
                ('pan_first_4', models.CharField(max_length=4, verbose_name='First four digits of card', blank=True)),
                ('pan_first_6', models.CharField(max_length=6, verbose_name='First six digits of card', blank=True)),
                ('pan_last_4', models.CharField(max_length=4, verbose_name='Last four digits of card', blank=True)),
            ],
            options={
                'ordering': ('-transaction_time',),
            },
        ),
    ]
