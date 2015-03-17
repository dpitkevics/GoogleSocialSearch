# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Search', '0005_searchitem_search_request'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='item',
            name='pagemap',
        ),
        migrations.RemoveField(
            model_name='item',
            name='search_result',
        ),
        migrations.DeleteModel(
            name='Item',
        ),
        migrations.RemoveField(
            model_name='pagemap',
            name='cse_image',
        ),
        migrations.DeleteModel(
            name='CseImage',
        ),
        migrations.RemoveField(
            model_name='pagemap',
            name='cse_thumbnail',
        ),
        migrations.DeleteModel(
            name='CseThumbnail',
        ),
        migrations.RemoveField(
            model_name='pagemap',
            name='metatag',
        ),
        migrations.DeleteModel(
            name='Metatag',
        ),
        migrations.DeleteModel(
            name='Pagemap',
        ),
        migrations.RemoveField(
            model_name='searchresult',
            name='next_page',
        ),
        migrations.DeleteModel(
            name='NextPage',
        ),
        migrations.RemoveField(
            model_name='searchresult',
            name='request',
        ),
        migrations.DeleteModel(
            name='Request',
        ),
        migrations.RemoveField(
            model_name='searchresult',
            name='search_information',
        ),
        migrations.DeleteModel(
            name='SearchInformation',
        ),
        migrations.DeleteModel(
            name='SearchResult',
        ),
    ]
