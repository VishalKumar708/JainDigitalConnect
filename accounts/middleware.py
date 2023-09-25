

import json
from django.http import JsonResponse
from django.urls import resolve
from rest_framework import status
import logging


error_logger = logging.getLogger('error')
info_logger = logging.getLogger('django')


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
            error_logger.error('Invalid URL.')
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
                error_logger.error(f'Unsupported Media Type. Expected application/json but got {content_type}')

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
                    error_logger.error(f'Invalid JSON data.{str(e)}')

                    return JsonResponse(response_data, status=400)
            print('Middleware working fine')
        return self.get_response(request)


