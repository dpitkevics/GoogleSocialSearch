# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('User', '0004_auto_20150327_1006'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='experience',
        ),
        migrations.AddField(
            model_name='userprofile',
            name='_experience',
            field=models.FloatField(default=0, db_column='experience'),
            preserve_default=True,
        ),
    ]
