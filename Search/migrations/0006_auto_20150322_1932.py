# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Search', '0005_searchitem_owner'),
    ]

    operations = [
        migrations.AlterField(
            model_name='searchitem',
            name='view_count',
            field=models.IntegerField(default=1),
            preserve_default=True,
        ),
    ]
