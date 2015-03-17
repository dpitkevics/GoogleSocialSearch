# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Search', '0008_searchrequest_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserSearchRequest',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('search_request', models.ForeignKey(to='Search.SearchRequest')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'user_search_requests',
            },
            bases=(models.Model,),
        ),
    ]
