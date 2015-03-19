# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('Comments', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Search', '0011_usersearchrequest_search_count'),
    ]

    operations = [
        migrations.CreateModel(
            name='SearchItemComments',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('submit_date', models.DateTimeField(auto_now_add=True)),
                ('comment', models.ForeignKey(to='Comments.Comment')),
                ('search_item', models.ForeignKey(related_name='comments', to='Search.SearchItem')),
            ],
            options={
                'ordering': ('-submit_date',),
                'db_table': 'search_item_comments',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SearchItemVoter',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('search_item', models.ForeignKey(to='Search.SearchItem')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'search_item_voters',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='searchitem',
            name='downvote_count',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='searchitem',
            name='upvote_count',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
    ]
