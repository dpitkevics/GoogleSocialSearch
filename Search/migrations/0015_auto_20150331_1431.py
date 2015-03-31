# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Search', '0014_auto_20150330_1621'),
    ]

    operations = [
        migrations.AlterField(
            model_name='searchitem',
            name='link',
            field=models.CharField(max_length=512),
            preserve_default=True,
        ),
    ]
