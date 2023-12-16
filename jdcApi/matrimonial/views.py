from rest_framework.views import APIView

from .serializer import *
from rest_framework.response import Response
from jdcApi.models import City
from accounts.models import User

from rest_framework.permissions import IsAuthenticated
from accounts.pagination import CustomPagination

from django.db.models import Q
from django.db.models import Case, F, IntegerField, When
from django.utils import timezone
from datetime import datetime, timedelta
from django.conf import settings

# Default age limits
DEFAULT_BOY_MIN_AGE = 18
DEFAULT_GIRL_MIN_AGE = 18


BOY_MIN_AGE = getattr(settings, 'BOY_MIN_AGE', DEFAULT_BOY_MIN_AGE)
GIRL_MIN_AGE = getattr(settings, 'GIRL_MIN_AGE', DEFAULT_GIRL_MIN_AGE)


class GETAllApprovedCityMatrimonial(APIView):
    permission_classes = [IsAuthenticated]
    """ show all approved city and search 'cityName' by user."""

    def get(self, request, *args, **kwargs):
        try:
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

            # queryset = City.objects.filter(isActive=True, isVerified=True).order_by(
            #     'cityName')
            queryset = City.objects.raw(
                """
                select jdcapi_city.cityId, jdcapi_city.cityName, count(accounts_user.id) as count from jdcapi_city
                left join accounts_user on accounts_user.cityId = jdcapi_city.cityId
                where jdcapi_city.isVerified=true and jdcapi_city.isActive=True
                group by jdcapi_city.cityId;
                """)
            print('queryset', queryset)
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
                'data': serializer.data

            }
            return Response(response_data)
        except Exception as e:
            response_data = {
                'status_code': 500,
                'status': 'error',
                'data': {'message': str(e)},
            }
            return Response(response_data, status=500)


class GETAllResidentsByCityIdForMatrimonial(APIView):
    pagination_class = CustomPagination
    permission_classes = [IsAuthenticated]


    def get(self, request, cityId, *args, **kwargs):
        try:
            search_param = request.GET.get('gender')

            # search gender to get 'male' or 'female' record
            if search_param is None or search_param.strip().lower() == 'male':
                min_age = BOY_MIN_AGE
                search_param = 'male'
            elif search_param and search_param.strip().lower() == 'female':
                min_age = GIRL_MIN_AGE
            else:
                response_data = {
                    'status': 400,
                    'statusCode': 'failed',
                    'data': {
                        'message': f"'status' expected 'male' or 'female' value, but got '{search_param}'."}
                }
                return Response(response_data, status=400)
            queryset = User.objects.filter(
                            Q(cityId=cityId),
                            Q(lookingForMatch=True),
                            Q(gender=search_param),
                            ~Q(dob=None),
                            Q(dob__lte=datetime.now() - timedelta(365 * min_age)),
                        ).annotate(
                            age=Case(
                                When(
                                    dob__year__lt=timezone.now().year,
                                    then=timezone.now().year - F('dob__year') -
                                         Case(
                                             When(
                                                 dob__month__gt=timezone.now().month,
                                                 then=1
                                             ),
                                             When(
                                                 dob__month=timezone.now().month,
                                                 dob__day__gt=timezone.now().day,
                                                 then=1
                                             ),
                                             default=0,
                                             output_field=IntegerField()  # Specify the output field for this Case
                                         )
                                ),
                                default=None,  # Set default age to None if conditions aren't met
                                output_field=IntegerField()
                            )
                        ).order_by('name')

            # print('queryset==> ', queryset)
            if len(queryset) < 1:
                response_data = {
                    'statusCode': 200,
                    'status': 'Success',
                    'data': {'message': 'Record Not Found'}
                }
                return Response(response_data)

            # apply pagination
            pagination_data = {}
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
        except ValueError:
            response_data = {
                'statusCode': 404,
                'status': 'failed',
                'data': {'message': f"'cityId' excepted a number but got '{cityId}'"},
            }
            return Response(response_data, status=404)
        except Exception as e:
            response_data = {
                'statusCode': 500,
                'status': 'error',
                'data': {'message': str(e)},
            }
            return Response(response_data, status=500)


class GETAllResidentsForMatrimonial(APIView):
    pagination_class = CustomPagination
    permission_classes = [IsAuthenticated]


    def get(self, request, *args, **kwargs):
        try:
            search_param = request.GET.get('gender')

            # search gender to get 'male' or 'female' record
            if search_param is None or search_param.strip().lower() == 'male':
                min_age = BOY_MIN_AGE
                search_param = 'male'
            elif search_param and search_param.strip().lower() == 'female':
                min_age = GIRL_MIN_AGE
            else:
                response_data = {
                    'status': 400,
                    'statusCode': 'failed',
                    'data': {
                        'message': f"'status' expected 'male' or 'female' value, but got '{search_param}'."}
                }
                return Response(response_data, status=400)
            queryset = User.objects.filter(
                        Q(lookingForMatch=True),
                        Q(gender=search_param),
                        ~Q(dob=None),
                        Q(dob__lte=datetime.now() - timedelta(365 * min_age)),
                    ).annotate(
                        age=Case(
                            When(
                                dob__year__lt=timezone.now().year,
                                then=timezone.now().year - F('dob__year') -
                                     Case(
                                         When(
                                             dob__month__gt=timezone.now().month,
                                             then=1
                                         ),
                                         When(
                                             dob__month=timezone.now().month,
                                             dob__day__gt=timezone.now().day,
                                             then=1
                                         ),
                                         default=0,
                                         output_field=IntegerField()  # Specify the output field for this Case
                                     )
                            ),
                            default=None,  # Set default age to None if conditions aren't met
                            output_field=IntegerField()
                        )
                    ).order_by('name')

            if len(queryset) < 1:
                response_data = {
                    'statusCode': 200,
                    'status': 'Success',
                    'data': {'message': 'Record Not Found'}
                }
                return Response(response_data)

            # apply pagination
            pagination_data = {}
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

