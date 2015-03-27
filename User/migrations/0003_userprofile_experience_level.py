# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('User', '0002_userexperiencelevels'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='experience_level',
            field=models.ForeignKey(default=1, to='User.UserExperienceLevels'),
            preserve_default=False,
        ),
    ]
