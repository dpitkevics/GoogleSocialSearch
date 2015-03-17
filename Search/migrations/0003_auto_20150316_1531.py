# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Search', '0002_auto_20150316_1530'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='view_count',
            field=models.IntegerField(default=1),
            preserve_default=True,
        ),
    ]
