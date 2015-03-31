# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('User', '0006_auto_20150328_1935'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userexperiencelevel',
            name='experience_from',
            field=models.FloatField(db_index=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='userexperiencelevel',
            name='experience_till',
            field=models.FloatField(db_index=True),
            preserve_default=True,
        ),
    ]
