# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Search', '0011_auto_20150324_1457'),
    ]

    operations = [
        migrations.AddField(
            model_name='searchitem',
            name='owner_comment',
            field=models.TextField(null=True),
            preserve_default=True,
        ),
    ]
