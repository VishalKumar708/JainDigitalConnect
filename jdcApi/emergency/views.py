from django.db.models import Q
from rest_framework.views import APIView
from .serializer import *
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from utils.get_id_by_token import get_user_id_from_token_view
from jdcApi.models import Emergency, City
from accounts.pagination import CustomPagination

import logging
error_logger = logging.getLogger('error')
info_logger = logging.getLogger('info')


class POSTEmergency(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        """To create add new emergency record."""
        try:
            get_user_id = get_user_id_from_token_view(request)
            serializer = CREATEEmergencySerializer(data=request.data, context={'user_id_by_token': get_user_id})
            if serializer.is_valid():
                serializer.save()
                response_data = {
                    'status': 200,
                    'statusCode': 'success',
                    'data': {'message': 'Record Added Successfully.'}
                }
                info_logger.info('New Emergency Created Successfully.')
                return Response(response_data)
            response_data = {
                'status': 400,
                'statusCode': 'failed',
                'data': serializer.errors
            }
            return Response(response_data, status=400)
        except Exception as e:
            error_logger.error(f'An Exception occured while creating new Sect {e}')
            response_data = {
                'status': 500,
                'statusCode': 'failed',
                'data': str(e)
            }
            return Response(response_data, status=500)


class PUTEmergencyById(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, id, *args, **kwargs):
        try:

            obj = Emergency.objects.get(id=id)
            get_user_id = get_user_id_from_token_view(request)
            serializer = UPDATEEmergencySerializer(data=request.data, instance=obj, partial=True,
                                                    context={'user_id_by_token': get_user_id, 'id': id})
            if serializer.is_valid():
                serializer.save()
                response_data = {
                    'status': 200,
                    'statusCode': 'success',
                    'data': {'message': 'Record Updated Successfully.'}
                }
                info_logger.info('Emergency Updated Successfully.')
                return Response(response_data)
            response_data = {
                'status': 400,
                'statusCode': 'failed',
                'data': serializer.errors
            }
            return Response(response_data, status=400)
        except Emergency.DoesNotExist:
            response_data = {
                'status': 404,
                'statusCode': 'failed',
                'data': {'message': 'Invalid Id'}
            }
            error_logger.error(f'Invalid Emergency Id. While updating record.')
            return Response(response_data, status=404)
        except ValueError:
            response_data = {
                'status': 404,
                'statusCode': 'failed',
                'data': f" 'id' excepted a number but got '{id}'."
            }
            return Response(response_data, status=404)
        except Exception as e:
            error_logger.error(f'An Exception occured while updating "Emergency" Record. {e}')
            response_data = {
                'status': 500,
                'statusCode': 'failed',
                'data': str(e)

            }
            return Response(response_data, status=500)


class GETEmergencyDetailById(APIView):

    def get(self, request, id, *args, **kwargs):
        try:
            emergency_obj = Emergency.objects.get(id=id)
            serializer = GETEmergencyDetailsSerializer(instance=emergency_obj)
            response_data = {
                'status': 200,
                'statusCode': 'success',
                'data': serializer.data
            }
            return Response(response_data)

        except Emergency.DoesNotExist:
            response_data = {
                'status': 404,
                'statusCode': 'failed',
                'data': {'message': 'invalid saintId'}
            }
            return Response(response_data, status=404)
        except ValueError:
            response_data = {
                'status': 404,
                'statusCode': 'failed',
                'data': {'message': f"'id' excepted a number but got '{id}'."}
            }
            return Response(response_data, status=404)


class GETAllCityByEmergency(APIView):
    """ show all approved city and search 'cityName' by user."""
    def get(self, request, *args, **kwargs):
        try:
            cityName = request.GET.get('cityName')

            # search
            if cityName:
                queryset = City.objects.filter(isActive=True, isVerified=True, cityName__icontains=cityName.strip())
                if len(queryset) < 1:
                    response_data = {
                        'statusCode': 200,
                        'status': 'Success',
                        'data': {"message": "No Record found."},
                    }
                    return Response(response_data)

                serializer = GETCitySerializer(queryset, many=True)
                response_data = {
                    'statusCode': 200,
                    'status': 'Success',
                    'data': serializer.data,
                }
                return Response(response_data)

            queryset = City.objects.filter(isActive=True, isVerified=True).order_by('cityName')
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
        except Exception as e:
            response_data = {
                'status_code': 500,
                'status': 'error',
                'data': {'error': str(e)},
            }
            return Response(response_data, status=500)


class GETAllEmergencyByCityId(APIView):

    def get(self,request, cityId, *args, **kwargs):
        try:

            City.objects.get(cityId=cityId)
            department_name = request.GET.get('departmentName')
            if department_name:
                queryset = Emergency.objects.filter(cityId=cityId, departmentName__icontains=department_name.strip())
            else:
                queryset = Emergency.objects.filter(cityId=cityId)
            if len(queryset) < 1:
                response_data = {
                    'statusCode': 200,
                    'status': 'Success',
                    'data': {"message": "No Record found."},
                }
                return Response(response_data)
            serializers = GETAllEmergencySerializer(queryset, many=True)
            response_data = {
                'statusCode': 200,
                'status': 'success',
                'data': serializers.data
            }
            return Response(response_data)
        except City.DoesNotExist:
            response_data = {
                'status_code': 404,
                'status': 'failed',
                'data': {"message":"Invalid cityId."},
            }
            return Response(response_data, status=404)
        except ValueError:
            response_data = {
                'status_code': 404,
                'status': 'failed',
                'data': {"message": f"'cityId' excepted a number but got '{cityId}'."},
            }
            return Response(response_data, status=404)


class GETAllEmergencyForAdmin(APIView):
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination

    def get(self, request, *args, **kwargs):
        """ this api show all 'active' and 'inactive' records based on 'status' query param by default show only
        'active' records."""
        status = request.GET.get('status')
        if status is None or status.strip().lower() == 'active':
            queryset = Emergency.objects.filter(isActive=True, isVerified=True).order_by('departmentName')
        elif status.strip().lower() == 'inactive':
            queryset = Emergency.objects.filter(Q(isActive=False) | Q(isVerified=False)).order_by('departmentName')
        else:
            response_data = {
                'status': 400,
                'statusCode': 'failed',
                'data': {'message': f"'status' expected 'active' or 'inactive' value, but got '{status}'."}
            }
            return Response(response_data, status=400)

        if len(queryset) < 1:
            response_data = {
                'statusCode': 200,
                'status': 'Success',
                'data': {"message": "No Record found."},
            }
            return Response(response_data)

        # pagination
        pagination_data = {}
        paginator = self.pagination_class()
        page = paginator.paginate_queryset(queryset, request)
        if page is not None:
            serializer = GETAllEmergencySerializer(page, many=True)
            pagination_data = paginator.get_paginated_response(serializer.data)
        # serializers = GETAllEmergencySerializer(queryset, many=True)
        response_data = {**{
            'statusCode': 200,
            'status': 'success',
        }, **pagination_data}
        return Response(response_data)
