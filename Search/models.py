from django.db import models


class SearchRequest(models.Model):
    search_time = models.FloatField(default=0)
    total_results = models.BigIntegerField(default=0)
    title = models.CharField(max_length=256)
    search_terms = models.CharField(max_length=512)
    start_index = models.IntegerField(default=1)
    input_encoding = models.CharField(max_length=8, default='utf8')
    output_encoding = models.CharField(max_length=8, default='utf8')
    safe = models.CharField(max_length=8, default='off')
    cx = models.CharField(max_length=256)

    class Meta:
        db_table = 'search_requests'

    def update_items_views(self):
        for search_item in self.searchitem_set.all():
            search_item.add_view()


class SearchItem(models.Model):
    kind = models.CharField(max_length=256)
    title = models.CharField(max_length=256)
    html_title = models.CharField(max_length=256)
    link = models.CharField(max_length=256)
    display_link = models.CharField(max_length=256)
    snippet = models.CharField(max_length=512)
    html_snippet = models.CharField(max_length=1024)
    cache_id = models.CharField(max_length=256)
    formatted_url = models.CharField(max_length=256)
    html_formatted_url = models.CharField(max_length=256)

    view_count = models.IntegerField(default=1)
    click_count = models.IntegerField(default=0)

    search_request = models.ManyToManyField(SearchRequest)

    class Meta:
        db_table = 'search_items'

    def __str__(self):
        return self.title

    def add_view(self):
        self.view_count += 1
        self.save()

    def add_click(self):
        self.click_count += 1
        self.save()