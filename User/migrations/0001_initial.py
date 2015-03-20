# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('photo', models.TextField()),
                ('experience', models.FloatField(default=0)),
                ('balance', models.FloatField(default=0)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='profile', unique=True)),
            ],
            options={
                'db_table': 'user_profiles',
            },
            bases=(models.Model,),
        ),
    ]
