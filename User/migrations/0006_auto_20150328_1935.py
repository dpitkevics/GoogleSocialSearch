# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('User', '0005_auto_20150327_1518'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='experience_level',
            field=models.ForeignKey(null=True, to='User.UserExperienceLevel'),
            preserve_default=True,
        ),
    ]
