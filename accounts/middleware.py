import json
import logging

from django.http import JsonResponse
from rest_framework import status
from rest_framework.response import Response


class Json404Middleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            response = self.get_response(request)
            print('response==> ', response)

            if response.status_code == 404:
                response_data = {
                    'status_code': status.HTTP_404_NOT_FOUND,
                    'status': 'failed',
                    'msg': 'Please provide a valid URL',
                }
                return JsonResponse(response_data, status=404)
            elif request.method in ['POST', 'PUT']:
                # Attempt to parse the request data as JSON
                json.loads(request.body.decode('utf-8'))  # Assumes UTF-8 encoding
        except json.JSONDecodeError:
            response_data = {
                'statusCode': 406,
                'status': 'Failed',
                'data': {'error': 'Invalid JSON data',}
            }
            return JsonResponse(response_data, status=400)
        except Exception as e:
            print("##################exception occur**************", e)
            response = self.process_exception(request, e)
            return response

    # def process_view(self, request, view_func, view_args, view_kwargs):
    #     """ call before any view called, but it doesn't return response """
    #     pass

    def process_exception(self, request, exception):
        """ Logic will be executed if an exception/error occur. """
        error_message = str(exception)
        status_code = 500
        error_response = {
            'statusCode': status_code,
            'status': '11failed',
            'error': error_message,
        }
        return JsonResponse(error_response, status=status_code)


