from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework import status


class CustomPagination(PageNumberPagination):
    page_size_query_param = 'page_size'  # Change the page size query parameter if needed
    max_page_size = 100  # Set your maximum page size if needed
    page_query_param = 'page'
    page_size = 5
    # last_page_strings = 'end_page'

    def get_paginated_response(self, data):
        if self.page.paginator.count == 0:
            return Response({
                'status_code': status.HTTP_204_NO_CONTENT,
                'status': 'success',
                'data': {
                    'count': self.page.paginator.count,
                    'next': self.get_next_link(),
                    'previous': self.get_previous_link(),
                    'results': "No Active Record found.",
                }
            }, status=204)
        return Response({
            'status_code': 200,
            'status': 'success',
            'data': {
                'count': self.page.paginator.count,
                'next': self.get_next_link(),
                'previous': self.get_previous_link(),
                'results': data,
            }
        })
