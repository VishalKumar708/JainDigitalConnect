from django.db.models import Q
from rest_framework.generics import *
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from .serializers import GETCitySerializer, CREATECitySerializer, GetAllAreaByCitySerializer, \
    GetAllBusinessByCitySerializer, GETCityByCityIdSerializer, UPDATECitySerializer
from rest_framework import status
from rest_framework.response import Response
from .models import City, Business

from .models import State
from utils.get_id_by_token import get_user_id_from_token_view
from utils.permission import IsOwnerOrReadOnly


class GetAllApprovedCity(ListAPIView):
    serializer_class = GETCitySerializer


    def get_queryset(self):
        queryset = City.objects.filter(isActive=True, isVerified=True).order_by('cityName')
        return queryset

    def list(self, request, *args, **kwargs):
        try:
            queryset = self.get_queryset()
            serializer = self.get_serializer(queryset, many=True)

            # Customize the response data as needed
            if len(serializer.data) == 0:
                response_data = {
                    'statusCode': status.HTTP_200_OK,
                    'status': 'Success',
                    'data': {"message": "No Record found."},
                }
                return Response(response_data)

            data = serializer.data
            response_data = {
                'status_code': status.HTTP_200_OK,
                'status': 'Success',
                'data': data,
            }

            return Response(response_data)
        except Exception as e:
            response_data = {
                'status_code': status.HTTP_500_INTERNAL_SERVER_ERROR,
                'status': 'error',
                'data': {'error': str(e)},
            }
            return Response(response_data, status=500)


class GetAllUnapprovedCity(ListAPIView):
    serializer_class = GETCitySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = City.objects.filter(Q(isActive=False)| Q(isVerified=False)).order_by('cityName')
        return queryset

    def list(self, request, *args, **kwargs):
        try:
            queryset = self.get_queryset()
            if len(queryset) == 0:
                response_data = {
                    'statusCode': status.HTTP_200_OK,
                    'status': 'Success',
                    'data': {"message": "No Record Found."},
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


class GetCityById(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, cityId, *args, **kwargs):
        try:
            instance = City.objects.get(cityId=cityId)
            serializer = GETCityByCityIdSerializer(instance)

            response_data = {
                'statusCode': status.HTTP_200_OK,
                'status': 'success',
                'data': serializer.data
            }
            return Response(response_data)
        except City.DoesNotExist:
            response_data = {
                'statusCode': status.HTTP_404_NOT_FOUND,
                'status': 'failed',
                'data': {'message': "Invalid CityId."}
            }
            return Response(response_data, status=404)
        except Exception as e:
            response_data = {
                'statusCode': status.HTTP_500_INTERNAL_SERVER_ERROR,
                'status': 'error',
                'data': {'error': str(e)}
            }
            return Response(response_data, status=500)


# Get all areas by cityId
class GetAreaByCityId(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, cityId, *args, **kwargs):
        try:
            instance = City.objects.get(cityId=cityId)
            serializer = GetAllAreaByCitySerializer(instance, context={'cityId': cityId})
            response_data = {
                'status_code': status.HTTP_200_OK,
                'status': 'Success',
                'data': serializer.data,
            }
            return Response(response_data)
        except City.DoesNotExist:
            response_data = {
                'statusCode': status.HTTP_404_NOT_FOUND,
                'status': 'failed',
                'data': {'message': "Invalid CityId."}
            }
            return Response(response_data, status=404)
        except Exception as e:
            response_data = {
                'statusCode': status.HTTP_500_INTERNAL_SERVER_ERROR,
                'status': 'error',
                'data': {'error': str(e)}
            }
            return Response(response_data, status=500)


# get all business by city id
class GetAllBusinessByCityId(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, cityId, *args, **kwargs):
        try:
            instance = City.objects.get(cityId=cityId)
            serializer = GetAllBusinessByCitySerializer(instance, context={'cityId': cityId})
            response_data = {
                'status_code': status.HTTP_200_OK,
                'status': 'Success',
                'data': serializer.data,
            }
            return Response(response_data)
        except City.DoesNotExist:
            response_data = {
                'statusCode': status.HTTP_404_NOT_FOUND,
                'status': 'failed',
                'data': {'message': "Invalid CityId."}
            }
            return Response(response_data, status=404)
        except Exception as e:
            response_data = {
                'statusCode': status.HTTP_500_INTERNAL_SERVER_ERROR,
                'status': 'error',
                'data': {'error': str(e)}
            }
            return Response(response_data, status=500)


class CreateNewCity(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        try:
            # check city already exist or not
            city_name = request.data.get('cityName')
            matching_cities_count = City.objects.filter(cityName__iexact=city_name.strip()).count()
            if matching_cities_count > 0:
                json_data = {
                    'status_code': status.HTTP_302_FOUND,
                    'status': 'failed',
                    'message': {'msg': f"'{city_name.strip()}' already exists."},
                }
                return Response(json_data, status=302)

            # chekc city,state are not None and description is None
            state_id = request.data.get('stateId')
            # Exception occurred if state id is wrong
            State.objects.get(stateId=state_id)

            get_user_id = get_user_id_from_token_view(request)
            serializer = CREATECitySerializer(data=request.data, context={'user_id_by_token': get_user_id})
            if serializer.is_valid():
                serializer.save()
                response_data = {
                    'status_code': status.HTTP_200_OK,
                    'status': 'success',
                    'data': {'message': 'City created successfully.'},
                }
                return Response(response_data, status=200)
            response_data = {
                'status_code': status.HTTP_200_OK,
                'status': 'failed',
                'data': serializer.errors,
            }
            return Response(response_data, status=400)
        except State.DoesNotExist:
            response_data = {
                'status_code': status.HTTP_404_NOT_FOUND,
                'status': 'failed',
                'data': {'message': "Invalid stateId."},
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            # Handle the case when request data is not valid
            response_data = {
                'status_code': status.HTTP_400_BAD_REQUEST,
                'status': 'error',
                'data': {'error': str(e)},
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)


class UpdateCityById(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, cityId, *args, **kwargs):
        try:
            # check user provide value or not
            if len(request.data) < 1:
                serializer = UPDATECitySerializer(data=request.data)
                if not serializer.is_valid():
                    response_data = {
                        'statusCode': status.HTTP_204_NO_CONTENT,
                        'status': 'failed',
                        'message': serializer.errors,
                    }
                    return Response(response_data, status=status.HTTP_204_NO_CONTENT)

            city_name = request.data.get('cityName')
            # check updated state is available or not
            matching_city_counts = City.objects.filter(Q(cityName__iexact=city_name), ~Q(cityId=cityId)).count()
            # print('count ==> ', matching_city_counts)
            if matching_city_counts > 0:
                json_data = {
                    'statuscode': status.HTTP_302_FOUND,
                    'status': 'failed',
                    'message': {'msg': f"'{city_name}' is already exists."},
                }
                return Response(json_data, status=status.HTTP_302_FOUND)

            get_user_id = get_user_id_from_token_view(request)
            instance = City.objects.get(cityId=cityId)
            serializer = UPDATECitySerializer(instance, data=request.data, partial=True, context={'user_id_by_token': get_user_id})
            if serializer.is_valid():
                serializer.save()
                response_data = {
                    'statusCode': status.HTTP_200_OK,
                    'status': 'success',
                    'data': {'msg': 'City Updated Successfully.'}
                }
                return Response(response_data)

            # Customize the response data if needed
            response_data = {
                'statusCode': status.HTTP_400_BAD_REQUEST,
                'status': 'failed',
                'data': serializer.errors,
            }
            return Response(response_data, status=404)
        except City.DoesNotExist:
            response_data = {
                'statusCode': status.HTTP_400_BAD_REQUEST,
                'status': 'failed',
                'data': {'message': "Invalid city Id."},
            }
            return Response(response_data, status=400)
        except Exception as e:
            response_data = {
                'statusCode': status.HTTP_500_INTERNAL_SERVER_ERROR,
                'status': 'error',
                'data': {'error': str(e)},
            }
            return Response(response_data, status=500)
