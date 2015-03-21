# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.utils.timezone import utc
from django.conf import settings
import datetime


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Search', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SearchItemView',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('view_count', models.IntegerField(default=1)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('search_item', models.ForeignKey(to='Search.SearchItem')),
                ('user', models.ForeignKey(null=True, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'search_item_views',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='searchitemclick',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2015, 3, 21, 20, 14, 34, 355558, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='searchitemvoter',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2015, 3, 21, 20, 14, 40, 598556, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='searchitemvoter',
            name='vote_type',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='searchitemclick',
            name='click_count',
            field=models.IntegerField(default=1),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='searchitemclick',
            name='user',
            field=models.ForeignKey(null=True, to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
