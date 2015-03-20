# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Comments', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SearchItem',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
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
                ('upvote_count', models.IntegerField(default=0)),
                ('downvote_count', models.IntegerField(default=0)),
            ],
            options={
                'db_table': 'search_items',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SearchItemClick',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('click_count', models.IntegerField(default=0)),
                ('search_item', models.ForeignKey(to='Search.SearchItem')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'search_item_clicks',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SearchItemComments',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('submit_date', models.DateTimeField(auto_now_add=True)),
                ('comment', models.ForeignKey(to='Comments.Comment')),
                ('search_item', models.ForeignKey(to='Search.SearchItem', related_name='comments')),
            ],
            options={
                'db_table': 'search_item_comments',
                'ordering': ('-submit_date',),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SearchItemVoter',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('search_item', models.ForeignKey(to='Search.SearchItem')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'search_item_voters',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SearchRequest',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('search_time', models.FloatField(default=0)),
                ('total_results', models.BigIntegerField(default=0)),
                ('title', models.CharField(max_length=256)),
                ('search_terms', models.CharField(max_length=512)),
                ('start_index', models.IntegerField(default=1)),
                ('input_encoding', models.CharField(max_length=8, default='utf8')),
                ('output_encoding', models.CharField(max_length=8, default='utf8')),
                ('safe', models.CharField(max_length=8, default='off')),
                ('cx', models.CharField(max_length=256)),
                ('country_code', models.CharField(max_length=32, default='en')),
            ],
            options={
                'db_table': 'search_requests',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UserSearchRequest',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('search_count', models.IntegerField(default=1)),
                ('search_request', models.ForeignKey(to='Search.SearchRequest')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'user_search_requests',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='searchitem',
            name='search_request',
            field=models.ManyToManyField(to='Search.SearchRequest'),
            preserve_default=True,
        ),
    ]
