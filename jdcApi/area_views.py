from rest_framework.generics import *
from rest_framework.views import APIView

from .serializers import *
from rest_framework import status
from rest_framework.response import Response

from django.db.models import Q
from rest_framework.exceptions import ValidationError
from django.http import Http404
from .models import Area
from utils.get_id_by_token import get_user_id_from_token_view
from rest_framework.permissions import IsAuthenticated

class GetAllApprovedAreas(ListAPIView):
    queryset = Area.objects.all().order_by('areaName')
    serializer_class = GETAreaSerializer

    def get_queryset(self):
        queryset = Area.objects.filter(isActive=True, isVerified=True).order_by('areaName')
        return queryset

    def list(self, request, *args, **kwargs):
        try:
            queryset = self.get_queryset()

            # Customize the response data as needed
            if len(queryset) == 0:
                response_data = {
                    'statusCode': status.HTTP_200_OK,
                    'status': 'Success',
                    'data': {'message': 'Record Not Found'}
                }
                return Response(response_data)

            serializer = self.get_serializer(queryset, many=True)
            response_data = {
                'status_code': status.HTTP_200_OK,
                'status': 'Success',
                'data': serializer.data,
            }
            return Response(response_data)
        except Exception as e:
            response_data = {
                'status_code': status.HTTP_500_INTERNAL_SERVER_ERROR,
                'status': 'error',
                'data': {'error': str(e)},
            }
            return Response(response_data, status=500)
#
#

class GetAllUnapprovedAreas(ListAPIView):
    serializer_class = GETAreaSerializer

    def get_queryset(self):
        queryset = Area.objects.filter(Q(isActive=False) | Q(isVerified=False)).order_by('areaName')
        return queryset

    def list(self, request, *args, **kwargs):
        try:
            queryset = self.get_queryset()

            # Customize the response data as needed
            if len(queryset) == 0:
                response_data = {
                    'statusCode': status.HTTP_200_OK,
                    'status': 'Success',
                    'data': {'message': 'Record Not Found'}
                }
                return Response(response_data)

            serializer = self.get_serializer(queryset, many=True)
            response_data = {
                'status_code': status.HTTP_200_OK,
                'status': 'Success',
                'data': serializer.data,
            }
            return Response(response_data)
        except Exception as e:
            response_data = {
                'status_code': status.HTTP_500_INTERNAL_SERVER_ERROR,
                'status': 'error',
                'data': {'error': str(e)},
            }
            return Response(response_data, status=500)


class GetAreaById(APIView):
    def get(self, request, areaId, *args, **kwargs):
        try:
            instance = Area.objects.get(areaId=areaId)
            serializer = GETAreaByAreaIdSerializer(instance)

            response_data = {
                'statusCode': status.HTTP_200_OK,
                'status': 'success',
                'data': serializer.data
            }
            return Response(response_data)
        except Area.DoesNotExist:
            response_data = {
                'statusCode': status.HTTP_404_NOT_FOUND,
                'status': 'failed',
                'data': {'message': "Invalid AreaId."}
            }
            return Response(response_data, status=404)
        except Exception as e:
            response_data = {
                'statusCode': status.HTTP_500_INTERNAL_SERVER_ERROR,
                'status': 'error',
                'data': {'error': str(e)}
            }
            return Response(response_data, status=500)


class CreateNewArea(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        try:
            # check city already exist or not
            area = request.data.get('areaName')
            area_name = area.strip() if area else area
            print('area name ===> ', area_name)
            city_id = request.data.get('cityId')
            matching_cities_count = Area.objects.filter(Q(cityId=city_id) & Q(areaName__iexact=area_name)).count()

            if matching_cities_count > 0:
                json_data = {
                    'status_code': status.HTTP_302_FOUND,
                    'status': 'failed',
                    'message': {'msg': f"'{area_name}' already exists."},
                }
                return Response(json_data, status=302)

            get_user_id = get_user_id_from_token_view(request)
            serializer = CREATEAreaSerializer(data=request.data, context={'user_id_by_token': get_user_id})
            if serializer.is_valid():
                serializer.save()
                response_data = {
                    'statusCode': status.HTTP_200_OK,
                    'status': 'success',
                    'data': {'message': 'Area created successfully.'},
                }
                return Response(response_data, status=200)
            response_data = {
                'statusCode': status.HTTP_400_BAD_REQUEST,
                'status': 'failed',
                'data': serializer.errors,
            }
            return Response(response_data, status=400)
        except Exception as e:
            # Handle the case when request data is not valid
            response_data = {
                'statusCode': status.HTTP_500_INTERNAL_SERVER_ERROR,
                'status': 'error',
                'data': {'error': str(e)},
            }
            return Response(response_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UpdateAreaById(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, areaId, *args, **kwargs):
        try:
            # check user provide value or not
            if len(request.data) < 2:
                serializer = UPDATEAreaSerializer(data=request.data)
                if not serializer.is_valid():
                    response_data = {
                        'statusCode': status.HTTP_204_NO_CONTENT,
                        'status': 'failed',
                        'message': serializer.errors,
                    }
                    return Response(response_data, status=status.HTTP_204_NO_CONTENT)

            # check updated area is available or not
            area = request.data.get('areaName')
            area_name = area.strip() if area else area
            city_id = request.data.get('cityId')
            matching_area_counts = Area.objects.filter(Q(areaName__iexact=area_name), ~Q(areaId=areaId), ~Q(cityId=city_id)).count()
            print('area matching count ==> ', matching_area_counts)
            if matching_area_counts > 0:
                json_data = {
                    'statuscode': status.HTTP_302_FOUND,
                    'status': 'failed',
                    'message': {'msg': f"'{area_name}' is already exists."},
                }
                return Response(json_data, status=status.HTTP_302_FOUND)

            area_instance = Area.objects.get(areaId=areaId)

            # Save the updated state object
            get_user_id = get_user_id_from_token_view(request)
            serializer = UPDATEAreaSerializer(area_instance, data=request.data, partial=True,  context={'user_id_by_token': get_user_id})
            if serializer.is_valid():
                serializer.save()
                response_data = {
                    'statusCode': status.HTTP_200_OK,
                    'status': 'success',
                    'data': {'message': 'Area updated successfully.'},
                }
                return Response(response_data, status=200)
            response_data = {
                'statusCode': status.HTTP_400_BAD_REQUEST,
                'status': 'failed',
                'data': serializer.errors,
            }
            return Response(response_data, status=400)
        except Area.DoesNotExist:
            response_data = {
                'statusCode': status.HTTP_400_BAD_REQUEST,
                'status': 'failed',
                'data': {'message': "Invalid Area Id."},
            }
            return Response(response_data, status=400)
        except Exception as e:
            response_data = {
                'statusCode': status.HTTP_500_INTERNAL_SERVER_ERROR,
                'status': 'error',
                'data': {'error': str(e)},
            }
            return Response(response_data, status=500)



