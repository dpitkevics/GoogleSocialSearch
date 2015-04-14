# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Search', '0022_auto_20150413_1337'),
    ]

    operations = [
        migrations.AddField(
            model_name='searchitem',
            name='price_at_owner_change',
            field=models.FloatField(null=True),
            preserve_default=True,
        ),
    ]
