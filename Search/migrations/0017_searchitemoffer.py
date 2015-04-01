# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Search', '0016_searchitem_owner_updated_at'),
    ]

    operations = [
        migrations.CreateModel(
            name='SearchItemOffer',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('offered_amount', models.FloatField()),
                ('offer_date', models.DateTimeField(auto_now_add=True)),
                ('offer_status', models.IntegerField(default=0)),
                ('search_item', models.ForeignKey(to='Search.SearchItem')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'search_item_offers',
            },
            bases=(models.Model,),
        ),
    ]
