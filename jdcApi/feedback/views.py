
from rest_framework.views import APIView

from .serializer import *

from rest_framework.response import Response
from jdcApi.models import Aarti, MstSect, Feedback
from utils.get_id_by_token import get_user_id_from_token_view
from accounts.pagination import CustomPagination

from utils.permission import IsHeadUser, IsAdminUser


class GETAllFeedbackForAdmin(APIView):
    permission_classes = [IsAdminUser]
    pagination_class = CustomPagination

    def get(self, request, *args, **kwargs):
        try:
            queryset = Feedback.objects.all().order_by('-createdDate')

            # queryset = self.get_queryset()
            if len(queryset) < 1:
                response_data = {
                    'statusCode': 200,
                    'status': 'Success',
                    'data': {'message': 'No Record found.'}
                }

                return Response(response_data)
            # pagination
            pagination_data = {}
            paginator = self.pagination_class()
            page = paginator.paginate_queryset(queryset, request)
            if page is not None:
                serializer = GETAllFeedbackForAdminSerializer(page, many=True)
                pagination_data = paginator.get_paginated_response(serializer.data)
            # serializer = self.get_serializer(queryset, many=True)
            response_data = {**{
                'statusCode': 200,
                'status': 'Success'
            }, **pagination_data}

            return Response(response_data)
        except Exception as e:
            response_data = {
                'statusCode': 500,
                'status': 'error',
                'data': {'message':'Internal Server Error.'},
            }
            return Response(response_data, status=500)


class GETFeedbackDetailsById(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request, feedbackId, *args, **kwargs):
        try:
            instance = Feedback.objects.get(id=feedbackId)
            serializer = GETFeedbackDetailsSerializer(instance)
            response_data = {
                'statusCode': 200,
                'status': 'success',
                'data': serializer.data
            }
            return Response(response_data)

        except Feedback.DoesNotExist:
            response_data = {
                'statusCode': 404,
                'status': 'failed',
                'data': {'message': "Invalid Feedback Id."}
            }
            return Response(response_data, status=404)
        except ValueError:
            response_data = {
                'statusCode': 404,
                'status': 'failed',
                'data': {'message': f"excepted a number but you got '{feedbackId}'."}
            }
            return Response(response_data, status=404)
        except Exception as e:
            response_data = {
                'statusCode': 500,
                'status': 'error',
                'data': {'message': 'Internal Server Error.'}
            }
            return Response(response_data, status=500)


class POSTNewFeedback(APIView):
    # permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        try:
            get_user_id = get_user_id_from_token_view(request)
            serializer = CREATEFeedbackSerializer(data=request.data, context={'user_id_by_token': get_user_id})
            if serializer.is_valid():
                serializer.save()
                response_data = {
                    'statusCode': 200,
                    'status': 'Success',
                    'data': {'message': 'Record Added successfully.'}
                }
                return Response(response_data)
            response_data = {
                'statusCode': 400,
                'status': 'failed',
                'data': serializer.errors
            }
            return Response(response_data, status=400)
        except Exception as e:
            response_data = {
                'statusCode': 500,
                'status': 'error',
                'data': {'message': "Internal Server Error"},
            }
            return Response(response_data, status=500)
