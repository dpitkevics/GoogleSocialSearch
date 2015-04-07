# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Search', '0017_searchitemoffer'),
    ]

    operations = [
        migrations.CreateModel(
            name='SearchItemCommentReport',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('reported_at', models.DateTimeField(auto_now_add=True)),
                ('search_item_comment', models.ForeignKey(to='Search.SearchItemComments')),
            ],
            options={
                'db_table': 'search_item_comment_reports',
            },
            bases=(models.Model,),
        ),
    ]
