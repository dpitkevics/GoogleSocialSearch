# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Search', '0021_auto_20150409_1759'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='searchitem',
            options={'permissions': (('can_vote', 'Can Vote'), ('can_buy', 'Can Buy'), ('can_sell', 'Can Sell'), ('owner', 'Owner'), ('can_add_basic_html', 'Can Add Basic Html'))},
        ),
        migrations.AlterModelOptions(
            name='searchitemcomments',
            options={'ordering': ('-submit_date',)},
        ),
    ]
