# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Search', '0019_searchitemview_ip_address'),
    ]

    operations = [
        migrations.AddField(
            model_name='searchitemclick',
            name='ip_address',
            field=models.CharField(null=True, max_length=32),
            preserve_default=True,
        ),
    ]
