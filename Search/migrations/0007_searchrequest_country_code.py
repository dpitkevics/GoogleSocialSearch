# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Search', '0006_auto_20150316_1703'),
    ]

    operations = [
        migrations.AddField(
            model_name='searchrequest',
            name='country_code',
            field=models.CharField(max_length=32, default='en'),
            preserve_default=True,
        ),
    ]
