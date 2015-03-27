# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0001_initial'),
        ('User', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserExperienceLevels',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('experience_from', models.FloatField()),
                ('experience_till', models.FloatField()),
                ('title', models.CharField(max_length=64)),
                ('user_group', models.ForeignKey(to='auth.Group')),
            ],
            options={
                'db_table': 'user_experience_levels',
            },
            bases=(models.Model,),
        ),
    ]
