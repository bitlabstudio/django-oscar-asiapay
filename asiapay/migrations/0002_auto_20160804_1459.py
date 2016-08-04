# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('asiapay', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='asiapaytransaction',
            name='source_ip',
            field=models.GenericIPAddressField(verbose_name='Source IP'),
        ),
    ]
