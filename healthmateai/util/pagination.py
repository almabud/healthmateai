from collections import OrderedDict

from rest_framework.pagination import (
    PageNumberPagination as RestPageNumberPagination,
    CursorPagination as RestCursorPagination
)
from rest_framework.response import Response


class PageNumberPagination(RestPageNumberPagination):
    page_size = 15
    page_size_query_param = 'page_size'
    max_page_size = 250

    def get_paginated_response(self, data):
        response = OrderedDict([
            ('count', self.page.paginator.count),
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('results', data)
        ])

        return Response(
            OrderedDict([('status', 'success'), ('data', response)])
        )


class CursorPagination(RestCursorPagination):
    page_size = 15
    page_size_query_param = 'page_size'
    max_page_size = 250

    def get_paginated_response(self, data):
        response = OrderedDict([
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('results', data)
        ])

        return Response(response)
