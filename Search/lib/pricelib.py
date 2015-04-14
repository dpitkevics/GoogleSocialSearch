from django.db import connection
from django.utils.timezone import datetime

from datetime import timedelta

from Jooglin import settings
from Jooglin.lib.database import dictfetchall


class Price:
    def __init__(self, search_item, search_item_voter):
        self.search_item = search_item
        self.search_item_voter = search_item_voter

    def get_current_price(self):
        return self.get_price(datetime.now())

    def get_price_for_date(self, date_for_price):
        return self.get_price(date_for_price)

    def get_price(self, date_for_price):
        cursor = connection.cursor()

        # Retrieving view count
        sql = "SELECT LEAST(COUNT(*), %s) AS view_count FROM search_item_views AS siv " \
              "JOIN search_items AS si ON siv.search_item_id = si.id " \
              "WHERE siv.created_at >= %s - INTERVAL 1 MONTH " \
              "AND siv.search_item_id = %s " \
              "GROUP BY siv.ip_address, DATE(siv.created_at)"

        cursor.execute(sql, [settings.MAX_VIEWS_PER_IP_PER_DAY,
                             date_for_price.strftime('%Y-%m-%d %H:%M:%S'),
                             self.search_item.pk])
        rows = dictfetchall(cursor)

        view_count = 0
        for row in rows:
            view_count += row['view_count']

        # Retrieving click count
        sql = "SELECT LEAST(COUNT(*), %s) AS click_count FROM search_item_clicks AS sic " \
              "JOIN search_items AS si ON sic.search_item_id = si.id " \
              "WHERE sic.created_at >= %s - INTERVAL 1 MONTH " \
              "AND sic.search_item_id = %s " \
              "GROUP BY sic.ip_address, DATE(sic.created_at)"

        cursor.execute(sql, [settings.MAX_CLICKS_PER_IP_PER_DAY,
                             date_for_price.strftime('%Y-%m-%d %H:%M:%S'),
                             self.search_item.pk])
        rows = dictfetchall(cursor)

        click_count = 0
        for row in rows:
            click_count += row['click_count']

        upvotes = self.search_item_voter.objects.filter(created_at__gte=date_for_price - timedelta(days=30),
                                                        search_item=self.search_item,
                                                        vote_type=self.search_item_voter.VOTE_TYPE_UP)
        downvotes = self.search_item_voter.objects.filter(created_at__gte=date_for_price - timedelta(days=30),
                                                          search_item=self.search_item,
                                                          vote_type=self.search_item_voter.VOTE_TYPE_DOWN)

        votes_count = len(upvotes) - len(downvotes)

        item_price = (view_count * settings.ITEM_VIEW_MULTIPLIER) + (click_count * settings.ITEM_CLICK_MULTIPLIER) + (
            votes_count * settings.ITEM_VOTE_SCORE_MULTIPLIER)

        return max(item_price, 0)