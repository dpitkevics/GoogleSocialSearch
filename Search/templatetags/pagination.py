from django.template import Library

register = Library()


@register.filter(name='build_uri')
def build_uri(pagination, page_number):
    return pagination.build_uri(page_number)


@register.filter(name='retrieve_page_array')
def retrieve_page_array(pagination):
    return pagination.retrieve_page_array().items()