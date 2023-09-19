

# import json
# from django.http import JsonResponse
# from rest_framework import status
# import logging
#
# logger = logging.getLogger(__name__)
# logger_middleware = logging.getLogger('middleware_log')
#
#
# class Json404Middleware:
#     def __init__(self, get_response):
#         self.get_response = get_response
#
#     def __call__(self, request):
#         try:
#             response = self.get_response(request)
#
#             if response.status_code == 404:
#                 response_data = {
#                     'status_code': status.HTTP_404_NOT_FOUND,
#                     'status': 'failed',
#                     'msg': 'Please provide a valid URL',
#                 }
#                 logger_middleware.error('Requested for Invalid URL.')
#
#                 return JsonResponse(response_data, status=404)
#
#             if request.method in ['POST', 'PUT']:
#                 try:
#                     # Attempt to parse the request data as JSON
#                     json.loads(response.body.decode('utf-8'))  # Assumes UTF-8 encoding
#                 except json.JSONDecodeError:
#                     response_data = {
#                         'statusCode': 406,
#                         'status': 'Failed',
#                         'data': {'error': 'Invalid JSON data', }
#                     }
#                     logger_middleware.error('Invalid JSON data.')
#
#                     return JsonResponse(response_data, status=400)
#         except Exception as e:
#             error_message = str(e)
#             status_code = 500
#             error_response = {
#                 'statusCode': status_code,
#                 'status': 'failed',
#                 'error': error_message,
#             }
#             logger_middleware.error(error_message)
#             return JsonResponse(error_response, status=status_code)
#
#         return response  # Return the original response if no exceptions occurred

import json
from django.http import JsonResponse
from django.urls import resolve
from rest_framework import status
import logging

logger = logging.getLogger(__name__)
logger_middleware = logging.getLogger('middleware_log')


class ValidateURLAndJSONMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Check if the URL is valid
        try:
            resolve(request.path_info)
            # print(request.path_info)
        except Exception as e:
            response_data = {
                'status_code': status.HTTP_404_NOT_FOUND,
                'status': 'failed',
                'msg': f'Please provide a valid URL.',
            }
            logger_middleware.info('Invalid URL.')
            return JsonResponse(response_data, status=404)

        if request.method in ['POST', 'PUT']:
            # Check if the request has a valid JSON content type
            content_type = request.content_type
            print('content_type ==> ', content_type)
            # if content_type != 'application/json':
            if content_type not in ('application/x-www-form-urlencoded', 'application/json'):
                response_data = {
                    'statusCode': 415,  # Use 415 Unsupported Media Type for non-JSON data
                    'status': 'Failed',
                    'data': {'error': 'Unsupported Media Type', 'details': f'Expected application/json but got {content_type}'}
                }
                logger_middleware.info(f'Unsupported Media Type. Expected application/json but got {content_type}')

                return JsonResponse(response_data, status=415)

            # Attempt to parse the request data as JSON
            if content_type == 'application/json':
                try:
                    request_data = json.loads(request.body.decode('utf-8'))  # Assumes UTF-8 encoding
                except json.JSONDecodeError as e:
                    response_data = {
                        'statusCode': 400,  # Use 400 Bad Request for invalid JSON
                        'status': 'Failed',
                        'data': {'error': 'Invalid JSON data', 'details': str(e)}
                    }
                    logger_middleware.info(f'Invalid JSON data.{str(e)}')

                    return JsonResponse(response_data, status=400)

        return self.get_response(request)


