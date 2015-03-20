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
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('comment', models.TextField(max_length=3000, verbose_name='comment')),
                ('submit_date', models.DateTimeField(default=None, verbose_name='date/time submitted', auto_now_add=True)),
                ('ip_address', models.GenericIPAddressField(blank=True, verbose_name='IP address', unpack_ipv4=True, null=True)),
                ('is_public', models.BooleanField(default=True, verbose_name='is public', help_text='Uncheck this box to make the comment effectively disappear from the site.')),
                ('is_removed', models.BooleanField(default=False, verbose_name='is removed', help_text='Check this box if the comment is inappropriate. A "This comment has been removed" message will be displayed instead.')),
                ('user', models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True, related_name='comment_comments', verbose_name='user')),
            ],
            options={
                'db_table': 'comments',
                'verbose_name_plural': 'comments',
                'verbose_name': 'comment',
                'ordering': ('-submit_date',),
                'permissions': [('can_moderate', 'Can moderate comments')],
            },
            bases=(models.Model,),
        ),
    ]
