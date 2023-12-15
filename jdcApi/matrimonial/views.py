from rest_framework.views import APIView

from .serializer import *
from rest_framework.response import Response
from jdcApi.models import City
from accounts.models import User

from rest_framework.permissions import IsAuthenticated
from utils.get_id_by_token import get_user_id_from_token_view
from django.db.models import Q
from accounts.pagination import CustomPagination
from django.db.models import Count, F


class GETAllApprovedCityMatrimonial(APIView):
    """ show all approved city and search 'cityName' by user."""
    def get(self, request, *args, **kwargs):
        # try:
            #  for search city Name
            cityName = request.GET.get('cityName')
            if cityName:
                queryset = City.objects.filter(isActive=True, isVerified=True, cityName__icontains=cityName.strip()).order_by('cityName')
                if len(queryset) < 1:
                    response_data = {
                        'statusCode': 200,
                        'status': 'Success',
                        'data': {"message": "No Results found !"},
                    }
                    return Response(response_data)

                serializer = GETCityWithCountSerializer(queryset, many=True)
                response_data = {
                    'statusCode': 200,
                    'status': 'Success',
                    'data': serializer.data,
                }
                return Response(response_data)

            queryset = City.objects.filter(isActive=True, isVerified=True).order_by(
                'cityName')
            if len(queryset) < 1:
                response_data = {
                    'statusCode': 200,
                    'status': 'Success',
                    'data': {"message": "No Results found !"},
                }
                return Response(response_data)

            # Customize the response data as needed
            if len(queryset) < 1:
                response_data = {
                    'statusCode': 200,
                    'status': 'Success',
                    'data': {"message": "No Record found."},
                }
                return Response(response_data)

            serializer = GETCityWithCountSerializer(queryset, many=True)
            response_data = {
                'status_code': 200,
                'status': 'Success',
                'data': serializer.data,
            }
            return Response(response_data)
        # except Exception as e:
        #     response_data = {
        #         'status_code': 500,
        #         'status': 'error',
        #         'data': {'message': str(e)},
        #     }
        #     return Response(response_data, status=500)


class GETAllResidentsByCityIdForMatrimonial(APIView):
    pagination_class = CustomPagination

    def get(self, request, cityId, *args, **kwargs):
        try:

            search_param = request.GET.get('gender')
            # queryset = None

            pagination_data = {}
            if search_param is None or search_param.strip().lower() == 'male':
                queryset = User.objects.filter(cityId=cityId, lookingForMatch=True, gender='male').order_by('name')
            elif search_param and search_param.strip().lower() == 'female':
                queryset = User.objects.filter(cityId=cityId, lookingForMatch=True, gender='female').order_by('name')
            else:
                response_data = {
                    'status': 400,
                    'statusCode': 'failed',
                    'data': {
                        'message': f"'status' expected 'male' or 'female' value, but got '{search_param}'."}
                }
                return Response(response_data, status=400)

            if len(queryset) < 1:
                response_data = {
                    'statusCode': 200,
                    'status': 'Success',
                    'memberCount': User.objects.filter(cityId=cityId).count(),
                    'familyCount': User.objects.filter(cityId=cityId, headId=None).count(),
                    'data': {'message': 'Record Not Found'}
                }
                return Response(response_data)

            # apply pagination
            paginator = self.pagination_class()
            page = paginator.paginate_queryset(queryset, request)
            if page is not None:
                serializer = GETAllResidentsForMatrimonialSerializer(page, many=True)
                pagination_data = paginator.get_paginated_response(serializer.data)

            response_data = {**{
                'status': 200,
                'statusCode': 'success',
                # 'data': serializer.data
            }, **pagination_data}
            return Response(response_data)

        # exceptions
        except ValueError:
            response_data = {
                'statusCode': 404,
                'status': 'failed',
                'data': {'message': f"'City Id' excepted a number but got '{cityId}'."},
            }
            return Response(response_data, status=404)
        except Exception as e:
            response_data = {
                'status_code': 500,
                'status': 'error',
                'data': {'message': str(e)},
            }
            return Response(response_data, status=500)


class GETAllResidentsForMatrimonial(APIView):
    pagination_class = CustomPagination

    def get(self, request, *args, **kwargs):
        try:

            search_param = request.GET.get('gender')
            # queryset = None

            pagination_data = {}
            if search_param is None or search_param.strip().lower() == 'male':
                queryset = User.objects.filter(lookingForMatch=True, gender='male').order_by('name')
            elif search_param and search_param.strip().lower() == 'female':
                queryset = User.objects.filter(lookingForMatch=True, gender='female').order_by('name')
            else:
                response_data = {
                    'status': 400,
                    'statusCode': 'failed',
                    'data': {
                        'message': f"'status' expected 'male' or 'female' value, but got '{search_param}'."}
                }
                return Response(response_data, status=400)

            if len(queryset) < 1:
                response_data = {
                    'statusCode': 200,
                    'status': 'Success',
                    'data': {'message': 'Record Not Found'}
                }
                return Response(response_data)

            # apply pagination
            paginator = self.pagination_class()
            page = paginator.paginate_queryset(queryset, request)
            if page is not None:
                serializer = GETAllResidentsForMatrimonialSerializer(page, many=True)
                pagination_data = paginator.get_paginated_response(serializer.data)

            response_data = {**{
                'status': 200,
                'statusCode': 'success',
                # 'data': serializer.data
            }, **pagination_data}
            return Response(response_data)
        except Exception as e:
            response_data = {
                'status_code': 500,
                'status': 'error',
                'data': {'message': str(e)},
            }
            return Response(response_data, status=500)