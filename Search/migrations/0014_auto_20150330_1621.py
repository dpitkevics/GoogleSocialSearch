# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Search', '0013_searchitemfavourite'),
    ]

    operations = [
        migrations.AlterField(
            model_name='searchitem',
            name='link',
            field=models.CharField(max_length=255, db_index=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='searchplugin',
            name='query',
            field=models.CharField(max_length=255, db_index=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='searchrequest',
            name='search_terms',
            field=models.CharField(max_length=255, db_index=True),
            preserve_default=True,
        ),
    ]
