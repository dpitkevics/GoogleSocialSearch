# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Search', '0002_auto_20150321_2214'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='searchitemclick',
            name='click_count',
        ),
        migrations.RemoveField(
            model_name='searchitemview',
            name='view_count',
        ),
    ]
