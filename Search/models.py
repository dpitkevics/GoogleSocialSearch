from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.db import connection

from datetime import date, timedelta

from Comments.models import Comment
from Jooglin import settings
from Jooglin.lib.database import dictfetchall


class SearchRequest(models.Model):
    search_time = models.FloatField(default=0)
    total_results = models.BigIntegerField(default=0)
    title = models.CharField(max_length=256)
    search_terms = models.CharField(max_length=255, db_index=True)
    start_index = models.IntegerField(default=1)
    input_encoding = models.CharField(max_length=8, default='utf8')
    output_encoding = models.CharField(max_length=8, default='utf8')
    safe = models.CharField(max_length=8, default='off')
    cx = models.CharField(max_length=256)
    country_code = models.CharField(max_length=32, default='en')

    class Meta:
        db_table = 'search_requests'

    def update_items_views(self, user=None, ip_address=None):
        for search_item in self.searchitem_set.all():
            search_item.add_view()

            search_item_view = SearchItemView()
            search_item_view.search_item = search_item
            search_item_view.user = user
            search_item_view.ip_address = ip_address
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
    link = models.CharField(max_length=512)
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
    owner_comment = models.TextField(null=True)
    owner_updated_at = models.DateTimeField(null=True)

    search_request = models.ManyToManyField(SearchRequest)

    class Meta:
        db_table = 'search_items'
        permissions = (
            ('can_vote', 'Can Vote'),
            ('can_buy', 'Can Buy'),
            ('can_sell', 'Can Sell'),
            ('owner', 'Owner'),
        )

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
        cursor = connection.cursor()

        # Retrieving view count
        sql = "SELECT LEAST(COUNT(*), %s) AS view_count FROM search_item_views AS siv " \
              "JOIN search_items AS si ON siv.search_item_id = si.id " \
              "WHERE siv.created_at >= NOW() - INTERVAL 1 MONTH " \
              "AND siv.search_item_id = %s " \
              "AND si.owner_id != siv.user_id " \
              "GROUP BY siv.ip_address, DATE(siv.created_at)"

        cursor.execute(sql, [settings.MAX_VIEWS_PER_IP_PER_DAY, self.pk])
        rows = dictfetchall(cursor)

        view_count = 0
        for row in rows:
            view_count += row['view_count']

        # Retrieving click count
        sql = "SELECT LEAST(COUNT(*), %s) AS click_count FROM search_item_clicks AS sic " \
              "JOIN search_items AS si ON sic.search_item_id = si.id " \
              "WHERE sic.created_at >= NOW() - INTERVAL 1 MONTH " \
              "AND sic.search_item_id = %s " \
              "AND si.owner_id != sic.user_id " \
              "GROUP BY sic.ip_address, DATE(sic.created_at)"

        cursor.execute(sql, [settings.MAX_CLICKS_PER_IP_PER_DAY, self.pk])
        rows = dictfetchall(cursor)

        click_count = 0
        for row in rows:
            click_count += row['click_count']

        upvotes = SearchItemVoter.objects.filter(created_at__gte=date.today() - timedelta(days=30), search_item=self,
                                                 vote_type=SearchItemVoter.VOTE_TYPE_UP)
        downvotes = SearchItemVoter.objects.filter(created_at__gte=date.today() - timedelta(days=30), search_item=self,
                                                   vote_type=SearchItemVoter.VOTE_TYPE_DOWN)

        votes_count = len(upvotes) - len(downvotes)

        item_price = (view_count * settings.ITEM_VIEW_MULTIPLIER) + (click_count * settings.ITEM_CLICK_MULTIPLIER) + (
            votes_count * settings.ITEM_VOTE_SCORE_MULTIPLIER)
        return item_price

    def is_user_favourite(self, user):
        try:
            self.searchitemfavourite_set.filter(user=user)[0]
            return True
        except IndexError:
            return False

    def is_sell_date_valid(self):
        available_for_sell_date = self.sell_date()
        if timezone.now() < available_for_sell_date:
            return False

        return True

    def sell_date(self):
        available_for_sell_date = self.owner_updated_at + timedelta(days=30)
        return available_for_sell_date


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
    ip_address = models.CharField(max_length=32, null=True)

    class Meta:
        db_table = 'search_item_clicks'


class SearchItemView(models.Model):
    search_item = models.ForeignKey(SearchItem)
    user = models.ForeignKey(User, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    ip_address = models.CharField(max_length=32, null=True)

    class Meta:
        db_table = 'search_item_views'


class SearchPlugin(models.Model):
    query = models.CharField(max_length=255, db_index=True)
    package = models.CharField(max_length=256)
    class_name = models.CharField(max_length=128)

    class Meta:
        db_table = 'search_plugins'

    def __str__(self):
        return self.query


class SearchItemFavourite(models.Model):
    search_item = models.ForeignKey(SearchItem)
    user = models.ForeignKey(User)

    class Meta:
        db_table = 'search_item_favourites'


class SearchItemOffer(models.Model):
    OFFER_STATUS_PENDING = 0
    OFFER_STATUS_ACCEPTED = 1
    OFFER_STATUS_DECLINED = 2

    search_item = models.ForeignKey(SearchItem)
    user = models.ForeignKey(User)
    offered_amount = models.FloatField()
    offer_date = models.DateTimeField(auto_now_add=True)
    offer_status = models.IntegerField(default=OFFER_STATUS_PENDING)

    class Meta:
        db_table = 'search_item_offers'


class SearchItemCommentReport(models.Model):
    search_item_comment = models.ForeignKey(SearchItemComments)
    reported_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'search_item_comment_reports'