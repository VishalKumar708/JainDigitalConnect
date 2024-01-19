from django.db.models import Q
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from .serializer import *
from rest_framework import status
from rest_framework.response import Response
from jdcApi.models import City

from utils.get_id_by_token import get_user_id_from_token_view


class GetAllApprovedAndUnapprovedCityForAdmin(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        status = request.GET.get('status')
        if status is None:
            response_data = {
                'statusCode': 400,
                'status': 'failed',
                'data': {"message": "Please pass query param 'status' value 'active/inactive' only."},
            }
            return Response(response_data, status=400)

        # check query param available or not
        if status.strip().lower() == 'active':
            queryset = City.objects.filter(isActive=True, isVerified=True).order_by('cityName')

        elif status.strip().lower() == 'inactive':
            queryset = City.objects.filter(Q(isActive=False) | Q(isVerified=False)).order_by('cityName')
        else:
            response_data = {
                'statusCode': 400,
                'status': 'failed',
                'data': {"message": "Invalid value of query param 'status'."},
            }
            return Response(response_data, status=400)
        if len(queryset) < 1:
            response_data = {
                'statusCode': 200,
                'status': 'Success',
                'data': {"message": "No Record Found."},
            }
            return Response(response_data)

        serializer = GETCitySerializer(queryset, many=True)
        response_data = {
            'status_code': 200,
            'status': 'Success',
            'data': serializer.data
        }
        return Response(response_data)


class GetCityDetailsById(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, cityId, *args, **kwargs):
        try:
            int(cityId)
            instance = City.objects.get(cityId=cityId)
            if instance.isVerified is False:
                serializer = GETCityByCityIdSerializer(instance, context={'status': True})
            else:
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
        except ValueError:
            response_data = {
                'statusCode': 404,
                'status': 'failed',
                'data': {'message': f"cityId excepted a number but got {cityId} "}
            }
            return Response(response_data, status=404)


class POSTNewCity(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        get_user_id = get_user_id_from_token_view(request)
        serializer = CREATECitySerializer(data=request.data, context={'user_id_by_token': get_user_id})
        if serializer.is_valid():
            serializer.save()
            response_data = {
                'status_code': status.HTTP_200_OK,
                'status': 'success',
                'data': {'message': 'Record added successfully.'},
            }
            return Response(response_data, status=200)
        response_data = {
            'status_code': status.HTTP_200_OK,
            'status': 'failed',
            'data': serializer.errors,
        }
        return Response(response_data, status=400)

class UpdateCityById(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, cityId, *args, **kwargs):
        try:
            int(cityId)
            get_user_id = get_user_id_from_token_view(request)
            instance = City.objects.get(cityId=cityId)
            serializer = UPDATECitySerializer(instance, data=request.data, partial=True, context={'user_id_by_token': get_user_id, 'city_id':cityId})
            if serializer.is_valid():
                serializer.save()
                response_data = {
                    'statusCode': status.HTTP_200_OK,
                    'status': 'success',
                    'data': {'message': 'Record Updated Successfully.'}
                }
                return Response(response_data)

            # Customize the response data if needed
            response_data = {
                'statusCode': 400,
                'status': 'failed',
                'data': serializer.errors,
            }
            return Response(response_data, status=400)
        except City.DoesNotExist:
            response_data ={
                'statusCode': 404,
                'status': 'failed',
                'data': {"message": "Invalid City Id."}
            }
            return Response(response_data, status=404)
        except ValueError:
            response_data ={
                'statusCode': 404,
                'status': 'failed',
                'data': {"message": f"City Id excepted a number but got {cityId}"}
            }
            return Response(response_data, status=404)

