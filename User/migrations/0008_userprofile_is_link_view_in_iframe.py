# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('User', '0007_auto_20150330_1618'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='is_link_view_in_iframe',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
