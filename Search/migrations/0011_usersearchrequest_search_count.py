# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Search', '0010_remove_searchrequest_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='usersearchrequest',
            name='search_count',
            field=models.IntegerField(default=1),
            preserve_default=True,
        ),
    ]
