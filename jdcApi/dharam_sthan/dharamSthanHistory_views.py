from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .dharamSthanHistory_serializer import *
from utils.get_id_by_token import get_user_id_from_token_view
from accounts.pagination import CustomPagination
from rest_framework.response import Response
from jdcApi.models import DharamSthanHistory
from django.utils import timezone


class POSTNewDharamSthanHistory(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        # try:
            get_user_id = get_user_id_from_token_view(request)
            serializer = CREATEDharamSthanHistorySerializer(data=request.data, context={'user_id_by_token': get_user_id})
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
        # except Exception as e:
        #     response_data = {
        #         'statusCode': 500,
        #         'status': 'error',
        #         'data': {'message': "Internal Server Error"},
        #     }
        #     return Response(response_data, status=500)


class PUTDharamSthanHistoryById(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, dharamSthanHistoryId, *args, **kwargs):
        try:
            get_user_id = get_user_id_from_token_view(request)
            instance = DharamSthanHistory.objects.get(id=dharamSthanHistoryId)
            serializer = UPDATEDharamSthanHistorySerializer(instance, data=request.data, partial=True, context={'user_id_by_token': get_user_id})
            if serializer.is_valid():
                serializer.save()
                response_data = {
                    'statusCode': 200,
                    'status': 'Success',
                    'data': {'message': 'Record Updated Successfully.'}
                }
                return Response(response_data)
            response_data = {
                'statusCode': 400,
                'status': 'failed',
                'data': serializer.errors
            }
            return Response(response_data, status=400)
        except DharamSthanHistory.DoesNotExist:
            response_data = {
                'statusCode': 404,
                'status': 'failed',
                'data': {'message': "Invalid DharamSthanHistory Id."},
            }
            return Response(response_data, status=404)
        except ValueError:
            response_data = {
                'statusCode': 404,
                'status': 'failed',
                'data': {'message': f"'DharamSthanHistory id' excepted a number but got '{dharamSthanHistoryId}'"},
            }
            return Response(response_data, status=404)


class GETDharamSthanHistoryDetailsById(APIView):

    def get(self, request, dharamSthanHistoryId, *args, **kwargs):
        try:
            instance = DharamSthanHistory.objects.get(id=dharamSthanHistoryId)
            serializer = GETDharamSthanHistoryDetialsSerializer(instance)
            response_data = {
                'statusCode': 200,
                'status': 'success',
                'data': serializer.data
            }
            return Response(response_data)

        except DharamSthanHistory.DoesNotExist:
            response_data = {
                'statusCode': 404,
                'status': 'failed',
                'data': {'message': "Invalid dharamSthanHistory id."}
            }
            return Response(response_data, status=404)
        except ValueError:
            response_data = {
                'statusCode': 404,
                'status': 'failed',
                'data': {'message': f"excepted a number but you got '{dharamSthanHistoryId}'."}
            }
            return Response(response_data, status=404)
        except Exception as e:
            response_data = {
                'statusCode': 500,
                'status': 'error',
                'data': {'message': 'Internal Server Error.'}
            }
            return Response(response_data, status=500)


class GETAllActiveDharamSthanHistoryBydharamSthanId(APIView):

    def get(self, request, dharamSthanId, *args, **kwargs):
        try:
            current_year = timezone.now().year
            queryset = DharamSthanHistory.objects.filter(dharamSthanId=dharamSthanId, isActive=True, year=current_year)
            if len(queryset) < 1:
                response_data = {
                    'statusCode': 200,
                    'status': 'success',
                    'data': {"message": "No Record Found."}
                }
                return Response(response_data)

            serializer = GETAllDharamSthanHistorySerializer(queryset, many=True)
            response_data = {
                'statusCode': 200,
                'status': 'success',
                'data': serializer.data
            }
            return Response(response_data)
        except ValueError:
            response_data = {
                'statusCode': 404,
                'status': 'failed',
                'data': {'message': f"excepted a number but you got '{dharamSthanId}'."}
            }
            return Response(response_data, status=404)


class GETAllDharamSthanHistoryBydharamSthanIdForAdmin(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, dharamSthanId, *args, **kwargs):
        try:
            queryset = DharamSthanHistory.objects.filter(dharamSthanId=dharamSthanId)
            if len(queryset) < 1:
                response_data = {
                    'statusCode': 200,
                    'status': 'success',
                    'data': {"message": "No Record Found."}
                }
                return Response(response_data)

            serializer = GETAllDharamSthanHistorySerializer(queryset, many=True)
            response_data = {
                'statusCode': 200,
                'status': 'success',
                'data': serializer.data
            }
            return Response(response_data)
        except ValueError:
            response_data = {
                'statusCode': 404,
                'status': 'failed',
                'data': {'message': f"excepted a number but you got '{dharamSthanId}'."}
            }
            return Response(response_data, status=404)
