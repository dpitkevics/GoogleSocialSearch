# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Search', '0007_auto_20150322_1944'),
    ]

    operations = [
        migrations.CreateModel(
            name='SearchPlugin',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('query', models.CharField(max_length=512)),
                ('package', models.CharField(max_length=256)),
                ('class_name', models.CharField(max_length=128)),
            ],
            options={
                'db_table': 'search_plugins',
            },
            bases=(models.Model,),
        ),
    ]
