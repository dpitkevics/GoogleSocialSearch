# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('User', '0003_userprofile_experience_level'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='UserExperienceLevels',
            new_name='UserExperienceLevel',
        ),
    ]
