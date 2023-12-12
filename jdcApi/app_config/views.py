
from rest_framework.views import APIView

from .serializer import *
from rest_framework import status
from rest_framework.response import Response
from jdcApi.models import AppConfigurations
from rest_framework.permissions import IsAuthenticated
from utils.get_id_by_token import get_user_id_from_token_view
# from django.db.models import Q
# from accounts.pagination import CustomPagination


class POSTNewAppConfiguration(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        try:
            get_user_id = get_user_id_from_token_view(request)
            serializer = CREATEAppConfigurationSerializer(data=request.data, context={'user_id_by_token': get_user_id})
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
                'data': {'error': str(e)},
            }
            return Response(response_data, status=500)


class PUTAppConfigurationById(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, appConfigurationId, *args, **kwargs):
        try:
            get_user_id = get_user_id_from_token_view(request)
            instance = AppConfigurations.objects.get(id=appConfigurationId)
            serializer = UPDATEAppConfigurationSerializer(instance, data=request.data, partial=True, context={'user_id_by_token': get_user_id, 'id': appConfigurationId})
            if serializer.is_valid():
                serializer.save()
                response_data = {
                    'statusCode': status.HTTP_200_OK,
                    'status': 'Success',
                    'data': {'message': 'Record Updated Successfully.'}
                }
                return Response(response_data)
            response_data = {
                'statusCode': status.HTTP_400_BAD_REQUEST,
                'status': 'failed',
                'data': serializer.errors
            }
            return Response(response_data, status=400)
        except AppConfigurations.DoesNotExist:
            response_data = {
                'statusCode': status.HTTP_404_NOT_FOUND,
                'status': 'failed',
                'data': {'message': "Invalid AppConfiguration Id."},
            }
            return Response(response_data, status=404)
        except ValueError:
            response_data = {
                'statusCode': 404,
                'status': 'failed',
                'data': {'message': f"'app configuration id' excepted a number but got '{appConfigurationId}'"},
            }
            return Response(response_data, status=404)
        except Exception as e:
            response_data = {
                'statusCode': status.HTTP_500_INTERNAL_SERVER_ERROR,
                'status': 'error',
                'data': {'error': str(e)},
            }
            return Response(response_data, status=500)


class GETAppConfigurationDetailsById(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, appConfigurationId, *args, **kwargs):
        try:
            instance = AppConfigurations.objects.get(id=appConfigurationId)
            serializer = GETAppConfigurationByIdSerializer(instance)

            response_data = {
                'statusCode':200,
                'status': 'Success',
                'data': serializer.data
            }
            return Response(response_data, status=400)
        except AppConfigurations.DoesNotExist:
            response_data = {
                'statusCode': status.HTTP_404_NOT_FOUND,
                'status': 'failed',
                'data': {'message': "Invalid AppConfiguration Id."},
            }
            return Response(response_data, status=404)
        except ValueError:
            response_data = {
                'statusCode': 404,
                'status': 'failed',
                'data': {'message': f"'app configuration id' excepted a number but got '{appConfigurationId}'"},
            }
            return Response(response_data, status=404)


class GETAllAppConfigurationsForAdmin(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        queryset = AppConfigurations.objects.all()
        if len(queryset) < 1:
            response_data = {
                'statusCode': 200,
                'status': 'Success',
                'data': {"message": "No Record Found."}
            }
            return Response(response_data)
        serializer = GETAllAppConfigurationSerializer(queryset, many=True)

        response_data = {
            'statusCode': 200,
            'status': 'Success',
            'data': serializer.data
        }
        return Response(response_data, status=400)

