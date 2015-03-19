# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Search', '0012_auto_20150319_2143'),
    ]

    operations = [
        migrations.CreateModel(
            name='SearchItemClick',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('click_count', models.IntegerField(default=0)),
                ('search_item', models.ForeignKey(to='Search.SearchItem')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'search_item_clicks',
            },
            bases=(models.Model,),
        ),
    ]
