# flake8: noqa
# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'AsiaPayTransaction'
        db.create_table(u'asiapay_asiapaytransaction', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('payment_method', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('currency_code', self.gf('django.db.models.fields.CharField')(max_length=3)),
            ('prc', self.gf('django.db.models.fields.IntegerField')()),
            ('src', self.gf('django.db.models.fields.IntegerField')()),
            ('auth_id', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('success_code', self.gf('django.db.models.fields.SmallIntegerField')()),
            ('payer_auth', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('channel_type', self.gf('django.db.models.fields.CharField')(max_length=3)),
            ('order_number', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('ip_country', self.gf('django.db.models.fields.CharField')(max_length=3)),
            ('payment_reference', self.gf('django.db.models.fields.IntegerField')()),
            ('bank_reference', self.gf('django.db.models.fields.IntegerField')()),
            ('account_holder', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('amount', self.gf('django.db.models.fields.FloatField')()),
            ('transaction_time', self.gf('django.db.models.fields.DateTimeField')()),
            ('eci', self.gf('django.db.models.fields.CharField')(max_length=2)),
            ('remark', self.gf('django.db.models.fields.TextField')(max_length=1024, blank=True)),
            ('card_issuing_country', self.gf('django.db.models.fields.CharField')(max_length=3)),
            ('alert_code', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('merchant_id', self.gf('django.db.models.fields.IntegerField')()),
            ('exp_month', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('exp_year', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('source_ip', self.gf('django.db.models.fields.IPAddressField')(max_length=15)),
            ('pan_first_4', self.gf('django.db.models.fields.CharField')(max_length=4)),
            ('pan_first_6', self.gf('django.db.models.fields.CharField')(max_length=6)),
            ('pan_last_4', self.gf('django.db.models.fields.CharField')(max_length=4)),
        ))
        db.send_create_signal(u'asiapay', ['AsiaPayTransaction'])


    def backwards(self, orm):
        # Deleting model 'AsiaPayTransaction'
        db.delete_table(u'asiapay_asiapaytransaction')


    models = {
        u'asiapay.asiapaytransaction': {
            'Meta': {'ordering': "('-transaction_time',)", 'object_name': 'AsiaPayTransaction'},
            'account_holder': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'alert_code': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'amount': ('django.db.models.fields.FloatField', [], {}),
            'auth_id': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'bank_reference': ('django.db.models.fields.IntegerField', [], {}),
            'card_issuing_country': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'channel_type': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'currency_code': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'eci': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'exp_month': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'exp_year': ('django.db.models.fields.PositiveIntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip_country': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'merchant_id': ('django.db.models.fields.IntegerField', [], {}),
            'order_number': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'pan_first_4': ('django.db.models.fields.CharField', [], {'max_length': '4'}),
            'pan_first_6': ('django.db.models.fields.CharField', [], {'max_length': '6'}),
            'pan_last_4': ('django.db.models.fields.CharField', [], {'max_length': '4'}),
            'payer_auth': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'payment_method': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'payment_reference': ('django.db.models.fields.IntegerField', [], {}),
            'prc': ('django.db.models.fields.IntegerField', [], {}),
            'remark': ('django.db.models.fields.TextField', [], {'max_length': '1024', 'blank': 'True'}),
            'source_ip': ('django.db.models.fields.IPAddressField', [], {'max_length': '15'}),
            'src': ('django.db.models.fields.IntegerField', [], {}),
            'success_code': ('django.db.models.fields.SmallIntegerField', [], {}),
            'transaction_time': ('django.db.models.fields.DateTimeField', [], {})
        }
    }

    complete_apps = ['asiapay']