from Search.models import SearchItemView, SearchItemClick, SearchItemVoter


class ItemHelper:
    def __init__(self, search_item):
        self.search_item = search_item

    def get_view_count(self):
        search_item_view_count = SearchItemView.objects.filter(search_item=self.search_item).count()

        return search_item_view_count

    def get_click_count(self):
        search_item_click_count = SearchItemClick.objects.filter(search_item=self.search_item).count()

        return search_item_click_count

    def get_upvote_count(self):
        search_item_upvote_count = SearchItemVoter.objects.filter(search_item=self.search_item,
                                                                  vote_type=SearchItemVoter.VOTE_TYPE_UP).count()

        return search_item_upvote_count

    def get_downvote_count(self):
        search_item_downvote_count = SearchItemVoter.objects.filter(search_item=self.search_item,
                                                                    vote_type=SearchItemVoter.VOTE_TYPE_DOWN).count()

        return search_item_downvote_count