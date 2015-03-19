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
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('comment', models.TextField(max_length=3000, verbose_name='comment')),
                ('submit_date', models.DateTimeField(default=None, verbose_name='date/time submitted', auto_now_add=True)),
                ('ip_address', models.GenericIPAddressField(unpack_ipv4=True, null=True, verbose_name='IP address', blank=True)),
                ('is_public', models.BooleanField(help_text='Uncheck this box to make the comment effectively disappear from the site.', default=True, verbose_name='is public')),
                ('is_removed', models.BooleanField(help_text='Check this box if the comment is inappropriate. A "This comment has been removed" message will be displayed instead.', default=False, verbose_name='is removed')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, verbose_name='user', related_name='comment_comments', null=True, blank=True)),
            ],
            options={
                'permissions': [('can_moderate', 'Can moderate comments')],
                'ordering': ('-submit_date',),
                'verbose_name': 'comment',
                'verbose_name_plural': 'comments',
                'db_table': 'comments',
            },
            bases=(models.Model,),
        ),
    ]
