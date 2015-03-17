# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CseImage',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('src', models.CharField(max_length=512)),
            ],
            options={
                'db_table': 'cse_images',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CseThumbnail',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('width', models.FloatField(default=0)),
                ('height', models.FloatField(default=0)),
                ('src', models.CharField(max_length=512)),
            ],
            options={
                'db_table': 'cse_thumbnails',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('kind', models.CharField(max_length=256)),
                ('title', models.CharField(max_length=256)),
                ('html_title', models.CharField(max_length=256)),
                ('link', models.CharField(max_length=256)),
                ('display_link', models.CharField(max_length=256)),
                ('snippet', models.CharField(max_length=512)),
                ('html_snippet', models.CharField(max_length=1024)),
                ('cache_id', models.CharField(max_length=256)),
                ('formatted_url', models.CharField(max_length=256)),
                ('html_formatted_url', models.CharField(max_length=256)),
            ],
            options={
                'db_table': 'items',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Metatag',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('referrer', models.CharField(max_length=256)),
                ('site_name', models.CharField(max_length=256)),
                ('url', models.URLField(max_length=512)),
                ('image', models.CharField(max_length=512)),
                ('locale', models.CharField(max_length=256)),
                ('locale_alternate', models.CharField(max_length=256)),
            ],
            options={
                'db_table': 'metatags',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='NextPage',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('title', models.CharField(max_length=256)),
                ('total_results', models.IntegerField(default=0)),
                ('search_terms', models.CharField(max_length=512)),
                ('count', models.IntegerField(default=0)),
                ('start_index', models.IntegerField(default=1)),
                ('input_encoding', models.CharField(default='utf8', max_length=8)),
                ('output_encoding', models.CharField(default='utf8', max_length=8)),
                ('safe', models.CharField(default='off', max_length=8)),
                ('cx', models.CharField(max_length=256)),
            ],
            options={
                'db_table': 'next_pages',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Pagemap',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('cse_image', models.ForeignKey(to='Search.CseImage', null=True)),
                ('cse_thumbnail', models.ForeignKey(to='Search.CseThumbnail', null=True)),
                ('metatag', models.ForeignKey(to='Search.Metatag', null=True)),
            ],
            options={
                'db_table': 'pagemaps',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Request',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('title', models.CharField(max_length=256)),
                ('total_results', models.IntegerField(default=0)),
                ('search_terms', models.CharField(max_length=512)),
                ('count', models.IntegerField(default=0)),
                ('start_index', models.IntegerField(default=1)),
                ('input_encoding', models.CharField(default='utf8', max_length=8)),
                ('output_encoding', models.CharField(default='utf8', max_length=8)),
                ('safe', models.CharField(default='off', max_length=8)),
                ('cx', models.CharField(max_length=256)),
                ('request_count', models.IntegerField(default=1)),
            ],
            options={
                'db_table': 'requests',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SearchInformation',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('search_time', models.FloatField(default=0)),
                ('formatted_search_time', models.FloatField(default=0)),
                ('total_results', models.BigIntegerField(default=0)),
                ('formatted_total_results', models.BigIntegerField(default=0)),
            ],
            options={
                'db_table': 'search_informations',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SearchResult',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('next_page', models.OneToOneField(to='Search.NextPage', null=True)),
                ('request', models.OneToOneField(to='Search.Request')),
                ('search_information', models.OneToOneField(to='Search.SearchInformation')),
            ],
            options={
                'db_table': 'search_results',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='item',
            name='pagemap',
            field=models.ForeignKey(to='Search.Pagemap'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='item',
            name='search_result',
            field=models.ForeignKey(to='Search.SearchResult', related_name='items'),
            preserve_default=True,
        ),
    ]
