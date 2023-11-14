from django.conf import settings
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework import status
# from collections import OrderedDict


class CustomPagination(PageNumberPagination):
    page_size_query_param = 'page_size'  # Change the page size query parameter if needed
    max_page_size = 30  # Set your maximum page size if needed
    page_query_param = 'page'
    # page_size = getattr(settings,  3)
    rest_framework_settings = getattr(settings, 'REST_FRAMEWORK', {})
    page_size = rest_framework_settings.get('PAGE_SIZE', 10)
    # page_size = rest_framework_settings.get('PAGE_SIZE')

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

# from rest_framework.pagination import LimitOffsetPagination
# from rest_framework.response import Response
# from rest_framework import status
#
#
# class CustomPagination(LimitOffsetPagination):
#     default_limit = 3  # Set your default limit (page size) if needed
#     max_limit = 100  # Set your maximum limit (page size) if needed
#
#     def get_paginated_response(self, data):
#         if self.count == 0:
#             return Response({
#                 'status_code': status.HTTP_204_NO_CONTENT,
#                 'status': 'success',
#                 'data': {
#                     'count': self.count,
#                     'next': self.get_next_link(),
#                     'previous': self.get_previous_link(),
#                     'results': "No Active Record found.",
#                 }
#             }, status=204)
#
#         return Response({
#             'status_code': 200,
#             'status': 'success',
#             'data': {
#                 'count': self.count,
#                 'next': self.get_next_link(),
#                 'previous': self.get_previous_link(),
#                 'results': data,
#             }
#         })
