from django.db import models
from django.contrib.auth.models import User

from datetime import date, timedelta

from Comments.models import Comment
from GoogleSocialSearch import settings


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
    country_code = models.CharField(max_length=32, default='en')

    class Meta:
        db_table = 'search_requests'

    def update_items_views(self, user=None):
        for search_item in self.searchitem_set.all():
            search_item.add_view()

            search_item_view = SearchItemView()
            search_item_view.search_item = search_item
            search_item_view.user = user
            search_item_view.save()


class UserSearchRequest(models.Model):
    search_request = models.ForeignKey(SearchRequest)
    user = models.ForeignKey(User)
    search_count = models.IntegerField(default=1)

    class Meta:
        db_table = 'user_search_requests'

    def add_search(self):
        self.search_count += 1
        self.save()


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

    view_count = models.IntegerField(default=0)
    click_count = models.IntegerField(default=0)
    upvote_count = models.IntegerField(default=0)
    downvote_count = models.IntegerField(default=0)
    owner = models.ForeignKey(User, null=True)

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

    def add_upvote(self):
        self.upvote_count += 1
        self.save()

    def add_downvote(self):
        self.downvote_count += 1
        self.save()

    def get_vote_score(self):
        return self.upvote_count - self.downvote_count

    def get_score(self):
        return self.get_vote_score() + self.click_count + self.view_count

    def get_price(self):
        views = SearchItemView.objects.filter(created_at__gte=date.today() - timedelta(days=30), search_item=self)
        clicks = SearchItemClick.objects.filter(created_at__gte=date.today() - timedelta(days=30), search_item=self)
        upvotes = SearchItemVoter.objects.filter(created_at__gte=date.today() - timedelta(days=30), search_item=self,
                                                 vote_type=SearchItemVoter.VOTE_TYPE_UP)
        downvotes = SearchItemVoter.objects.filter(created_at__gte=date.today() - timedelta(days=30), search_item=self,
                                                   vote_type=SearchItemVoter.VOTE_TYPE_DOWN)

        votes_count = len(upvotes) - len(downvotes)

        item_price = (len(views) * settings.ITEM_VIEW_MULTIPLIER) + (len(clicks) * settings.ITEM_CLICK_MULTIPLIER) + (votes_count * settings.ITEM_VOTE_SCORE_MULTIPLIER)
        return item_price


class SearchItemVoter(models.Model):
    VOTE_TYPE_UNKNOWN = 0
    VOTE_TYPE_UP = 1
    VOTE_TYPE_DOWN = 2

    search_item = models.ForeignKey(SearchItem)
    user = models.ForeignKey(User)
    vote_type = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'search_item_voters'


class SearchItemComments(models.Model):
    search_item = models.ForeignKey(SearchItem, related_name='comments')
    comment = models.ForeignKey(Comment)
    submit_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'search_item_comments'
        ordering = ('-submit_date',)


class SearchItemClick(models.Model):
    search_item = models.ForeignKey(SearchItem)
    user = models.ForeignKey(User, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'search_item_clicks'


class SearchItemView(models.Model):
    search_item = models.ForeignKey(SearchItem)
    user = models.ForeignKey(User, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'search_item_views'