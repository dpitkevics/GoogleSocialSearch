# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Search', '0004_searchitem_searchrequest'),
    ]

    operations = [
        migrations.AddField(
            model_name='searchitem',
            name='search_request',
            field=models.ManyToManyField(to='Search.SearchRequest'),
            preserve_default=True,
        ),
    ]
