# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Search', '0003_auto_20150316_1531'),
    ]

    operations = [
        migrations.CreateModel(
            name='SearchItem',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('kind', models.CharField(max_length=256)),
                ('title', models.CharField(max_length=256)),
                ('html_title', models.CharField(max_length=256)),
                ('link', models.CharField(max_length=256)),
                ('display_link', models.CharField(max_length=256)),
                ('snippet', models.CharField(max_length=512)),
                ('html_snippet', models.CharField(max_length=1024)),
                ('cache_id', models.CharField(max_length=256)),
                ('formatted_url', models.CharField(max_length=256)),
                ('html_formatted_url', models.CharField(max_length=256)),
                ('view_count', models.IntegerField(default=1)),
                ('click_count', models.IntegerField(default=0)),
            ],
            options={
                'db_table': 'search_items',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SearchRequest',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('search_time', models.FloatField(default=0)),
                ('total_results', models.BigIntegerField(default=0)),
                ('title', models.CharField(max_length=256)),
                ('search_terms', models.CharField(max_length=512)),
                ('start_index', models.IntegerField(default=1)),
                ('input_encoding', models.CharField(max_length=8, default='utf8')),
                ('output_encoding', models.CharField(max_length=8, default='utf8')),
                ('safe', models.CharField(max_length=8, default='off')),
                ('cx', models.CharField(max_length=256)),
            ],
            options={
                'db_table': 'search_requests',
            },
            bases=(models.Model,),
        ),
    ]
