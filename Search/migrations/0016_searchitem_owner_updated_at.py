# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Search', '0015_auto_20150331_1431'),
    ]

    operations = [
        migrations.AddField(
            model_name='searchitem',
            name='owner_updated_at',
            field=models.DateTimeField(null=True),
            preserve_default=True,
        ),
    ]
