from django.db import models


class SearchInformation(models.Model):
    search_time = models.FloatField(default=0)
    formatted_search_time = models.FloatField(default=0)
    total_results = models.BigIntegerField(default=0)
    formatted_total_results = models.BigIntegerField(default=0)

    class Meta:
        db_table = 'search_informations'


class Request(models.Model):
    title = models.CharField(max_length=256)
    total_results = models.IntegerField(default=0)
    search_terms = models.CharField(max_length=512)
    count = models.IntegerField(default=0)
    start_index = models.IntegerField(default=1)
    input_encoding = models.CharField(max_length=8, default='utf8')
    output_encoding = models.CharField(max_length=8, default='utf8')
    safe = models.CharField(max_length=8, default='off')
    cx = models.CharField(max_length=256)

    class Meta:
        db_table = 'requests'


class NextPage(models.Model):
    title = models.CharField(max_length=256)
    total_results = models.IntegerField(default=0)
    search_terms = models.CharField(max_length=512)
    count = models.IntegerField(default=0)
    start_index = models.IntegerField(default=1)
    input_encoding = models.CharField(max_length=8, default='utf8')
    output_encoding = models.CharField(max_length=8, default='utf8')
    safe = models.CharField(max_length=8, default='off')
    cx = models.CharField(max_length=256)

    class Meta:
        db_table = 'next_pages'


class SearchResult(models.Model):
    search_information = models.ForeignKey(SearchInformation)
    request = models.ForeignKey(Request)
    next_page = models.ForeignKey(NextPage)

    class Meta:
        db_table = 'search_results'


class CseImage(models.Model):
    src = models.CharField(max_length=512)

    class Meta:
        db_table = 'cse_images'


class CseThumbnail(models.Model):
    width = models.FloatField(default=0)
    height = models.FloatField(default=0)
    src = models.CharField(max_length=512)

    class Meta:
        db_table = 'cse_thumbnails'


class Metatag(models.Model):
    referrer = models.CharField(max_length=256)
    site_name = models.CharField(max_length=256)
    url = models.URLField(max_length=512)
    image = models.CharField(max_length=512)
    locale = models.CharField(max_length=256)
    locale_alternate = models.CharField(max_length=256)

    class Meta:
        db_table = 'metatags'


class Pagemap(models.Model):
    cse_image = models.ForeignKey(CseImage, null=True)
    cse_thumbnail = models.ForeignKey(CseThumbnail, null=True)
    metatag = models.ForeignKey(Metatag, null=True)

    class Meta:
        db_table = 'pagemaps'


class Item(models.Model):
    search_result = models.ForeignKey(SearchResult, related_name='items')

    kind = models.CharField(max_length=256)
    title = models.CharField(max_length=256)
    html_title = models.CharField(max_length=256)
    link = models.CharField(max_length=256)
    display_link = models.CharField(max_length=256)
    snippet = models.CharField(max_length=256)
    html_snippet = models.CharField(max_length=256)
    cache_id = models.CharField(max_length=256)
    formatted_url = models.CharField(max_length=256)
    html_formatted_url = models.CharField(max_length=256)
    pagemap = models.ForeignKey(Pagemap)

    class Meta:
        db_table = 'items'
