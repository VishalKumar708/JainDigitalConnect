from rest_framework.views import exception_handler
from rest_framework.response import Response


def custom_jwt_exception_handler(exc, context):
    response = exception_handler(exc, context)

    try:
        status_code = response.status_code
    except AttributeError:
        return response

    if status_code is not None and status_code == 401:

        custom_response = {
            'statusCode': response.status_code,
            'status': 'failed' if response.status_code != 200 else 'success',
            'data': {
                'detail': response.data.get('detail', 'Something went wrong'),
                # 'code': response.data.get('code', 'token_not_valid'),
                'error': response.data.get('messages', []),
            }
        }
        response.data = custom_response
    elif status_code is not None and status_code == 400:
        custom_response = {
            'statusCode': response.status_code,
            'status': 'failed' if response.status_code != 200 else 'success',
            'data': [response.data]
        }
        response.data = custom_response

    return response


# def custom_jwt_exception_handler(exc, context):
#     response = exception_handler(exc, context)
#     status_code = response.status_code
#
#     if response is not None:
#         custom_response = {
#             'statusCode': response.status_code,
#             'status': 'failed' if response.status_code != 200 else 'success',
#             'data': {
#                 'detail': response.data.get('detail', 'Something went wrong'),
#                 # 'code': response.data.get('code', 'token_not_valid'),
#                 'error': response.data.get('messages', []),
#             }
#         }
#         response.data = custom_response
#
#     return response
