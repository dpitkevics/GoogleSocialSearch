# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Search', '0020_searchitemclick_ip_address'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='searchitemcomments',
            options={'ordering': ('-submit_date',), 'permissions': (('can_add_basic_html', 'Can Add Basic Html'),)},
        ),
    ]
