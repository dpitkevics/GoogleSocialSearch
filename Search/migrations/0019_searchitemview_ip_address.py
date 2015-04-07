# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Search', '0018_searchitemcommentreport'),
    ]

    operations = [
        migrations.AddField(
            model_name='searchitemview',
            name='ip_address',
            field=models.CharField(null=True, max_length=32),
            preserve_default=True,
        ),
    ]
