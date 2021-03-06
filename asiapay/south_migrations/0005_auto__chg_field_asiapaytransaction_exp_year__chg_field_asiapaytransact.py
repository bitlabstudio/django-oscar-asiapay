# flake8: noqa
# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'AsiaPayTransaction.exp_year'
        db.alter_column(u'asiapay_asiapaytransaction', 'exp_year', self.gf('django.db.models.fields.PositiveIntegerField')(null=True))

        # Changing field 'AsiaPayTransaction.exp_month'
        db.alter_column(u'asiapay_asiapaytransaction', 'exp_month', self.gf('django.db.models.fields.PositiveIntegerField')(null=True))

    def backwards(self, orm):

        # User chose to not deal with backwards NULL issues for 'AsiaPayTransaction.exp_year'
        raise RuntimeError("Cannot reverse this migration. 'AsiaPayTransaction.exp_year' and its values cannot be restored.")

        # The following code is provided here to aid in writing a correct migration
        # Changing field 'AsiaPayTransaction.exp_year'
        db.alter_column(u'asiapay_asiapaytransaction', 'exp_year', self.gf('django.db.models.fields.PositiveIntegerField')())

        # User chose to not deal with backwards NULL issues for 'AsiaPayTransaction.exp_month'
        raise RuntimeError("Cannot reverse this migration. 'AsiaPayTransaction.exp_month' and its values cannot be restored.")

        # The following code is provided here to aid in writing a correct migration
        # Changing field 'AsiaPayTransaction.exp_month'
        db.alter_column(u'asiapay_asiapaytransaction', 'exp_month', self.gf('django.db.models.fields.PositiveIntegerField')())

    models = {
        u'asiapay.asiapaytransaction': {
            'Meta': {'ordering': "('-transaction_time',)", 'object_name': 'AsiaPayTransaction'},
            'account_holder': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'alert_code': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'amount': ('django.db.models.fields.FloatField', [], {}),
            'auth_id': ('django.db.models.fields.CharField', [], {'max_length': '128', 'blank': 'True'}),
            'bank_reference': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'card_issuing_country': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'channel_type': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'currency_code': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'eci': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'exp_month': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'exp_year': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip_country': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'merchant_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'order_number': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'pan_first_4': ('django.db.models.fields.CharField', [], {'max_length': '4', 'blank': 'True'}),
            'pan_first_6': ('django.db.models.fields.CharField', [], {'max_length': '6', 'blank': 'True'}),
            'pan_last_4': ('django.db.models.fields.CharField', [], {'max_length': '4', 'blank': 'True'}),
            'payer_auth': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'payment_method': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'payment_reference': ('django.db.models.fields.IntegerField', [], {}),
            'prc': ('django.db.models.fields.IntegerField', [], {}),
            'remark': ('django.db.models.fields.TextField', [], {'max_length': '1024', 'blank': 'True'}),
            'source_ip': ('django.db.models.fields.IPAddressField', [], {'max_length': '15'}),
            'src': ('django.db.models.fields.IntegerField', [], {}),
            'success_code': ('django.db.models.fields.SmallIntegerField', [], {}),
            'transaction_time': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['asiapay']