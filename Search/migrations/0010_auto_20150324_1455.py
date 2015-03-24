# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Search', '0009_auto_20150324_1444'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='searchitem',
            options={'permissions': (('can_vote', 'Can Vote'), ('can_buy', 'Can Buy'), ('can_sell', 'Can Sell'), ('can_edit', 'Can Edit'))},
        ),
    ]
