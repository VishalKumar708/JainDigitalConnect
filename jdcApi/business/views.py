
from rest_framework.views import APIView

from .serializer import GETCityCountForBusinessSerializer, GETCitySerializer, CREATEBusinessSerializer, PUTBusinessSerializer, GETBusinessSerializer, GETBusinessByIdSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from utils.get_id_by_token import get_user_id_from_token_view
from jdcApi.models import Business, City
from accounts.models import User
from django.db.models import Q, Count
from accounts.pagination import CustomPagination


class GETAllBusinessByUserId(APIView):
    def get(self, request, userId, *args, **kwargs):
        try:
            User.objects.get(id=userId)
            queryset = Business.objects.filter(userId=userId)
            if len(queryset) < 1:
                response_data = {
                    'statusCode': status.HTTP_200_OK,
                    'status': 'Success',
                    'data': {"message": "No Record found."},
                }
                return Response(response_data)

            serializer = GETBusinessSerializer(queryset, many=True)
            response_data = {
                'statusCode': 200,
                'status': 'Success',
                'data': serializer.data,
            }
            return Response(response_data, status=200)

        except User.DoesNotExist:
            response_data = {
                'statusCode': 404,
                'status': 'Success',
                'data': {"message": "Invalid User Id."},
            }
            return Response(response_data, status=404)
        except ValueError:
            response_data = {
                'statusCode': 404,
                'status': 'Success',
                'data': {"message": f"'userId' excepted a number but got '{userId}'."},
            }
            return Response(response_data, status=404)


class GetAllApprovedCityAndSearchCityNameForBusiness(APIView):
    """ show all approved city and search 'cityName' by user. for 'business' screen"""

    def get(self, request, *args, **kwargs):
        # try:
        queryset = City.objects.filter(isActive=True, isVerified=True).annotate(
            count=Count('GetAllBusinessByCityId', filter=Q(GetAllBusinessByCityId__isActive=True, GetAllBusinessByCityId__isVerified=True))
        ).values('cityId', 'cityName', 'count').order_by('cityName')
        # Customize the response data as needed
        if len(queryset) < 0:
            response_data = {
                'statusCode': status.HTTP_200_OK,
                'status': 'Success',
                'data': {"message": "No Record found."},
            }
            return Response(response_data)

        #  for search city Name
        cityName = request.GET.get('cityName')
        if cityName is None:
            serializer = GETCityCountForBusinessSerializer(queryset, many=True)
            response_data = {
                'status_code': status.HTTP_200_OK,
                'status': 'Success',
                'data': serializer.data,
            }
            return Response(response_data)
        else:
            filtered_queryset = queryset.filter(cityName__icontains=cityName.strip())

            #  if search not found
            if len(filtered_queryset) < 1:
                response_data = {
                    'statusCode': status.HTTP_200_OK,
                    'status': 'Success',
                    'data': {"message": "No Results found !"},
                }
                return Response(response_data)

            # if search found.
            serializer = GETCitySerializer(filtered_queryset, many=True)
            response_data = {
                'status_code': status.HTTP_200_OK,
                'status': 'Success',
                'data': serializer.data,
            }
            return Response(response_data)


class GetAllApprovedBusinessByCityId(APIView):  # correct
    pagination_class = CustomPagination

    def get(self, request,cityId, *args, **kwargs):
        try:
            business_name = request.GET.get('businessName')
            if business_name:
                queryset = Business.objects.filter(isActive=True, isVerified=True, cityId=cityId, businessName__icontains=business_name)
                if len(queryset) < 1:
                    response_data = {
                        'statusCode': status.HTTP_200_OK,
                        'status': 'Success',
                        'data': {'message': 'No Record found.'}
                    }

                    return Response(response_data)

                serializer = GETBusinessSerializer(queryset, many=True)
                response_data = {
                    'statusCode': status.HTTP_200_OK,
                    'status': 'Success',
                    'data': serializer.data,
                }

                return Response(response_data)

            queryset = Business.objects.filter(isActive=True, isVerified=True, cityId=cityId).order_by('businessName')
            if len(queryset) < 1:
                response_data = {
                    'statusCode': status.HTTP_200_OK,
                    'status': 'Success',
                    'data': {'message': 'No Record found.'}
                }

                return Response(response_data)
            # pagination
            pagination_data = {}
            paginator = self.pagination_class()
            page = paginator.paginate_queryset(queryset, request)
            if page is not None:
                serializer = GETBusinessSerializer(page, many=True)
                pagination_data = paginator.get_paginated_response(serializer.data)

            response_data = {**{
                'statusCode': 200,
                'status': 'Success'
            }, **pagination_data}

            return Response(response_data)
        except ValueError:
            response_data = {
                'statusCode': 404,
                'status': 'failed',
                'data': {'message': f"'cityId' excepted a number but got '{cityId}'."},
            }
            return Response(response_data, status=404)


class GetAllApprovedAndUnapprovedBusiness(APIView):  # correct
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination

    def get(self, request, *args, **kwargs):
        status = request.GET.get('status')

        if status is None or status.strip().lower() == 'active':
            queryset = Business.objects.filter(isActive=True, isVerified=True).order_by('businessName')
        elif status.strip().lower() == 'inactive':
            queryset = Business.objects.filter(Q(isActive=False) | Q(isVerified=False)).order_by('businessName')
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
                'data': {'message': 'No Record found.'}
            }
            return Response(response_data)
        pagination_data = {}
        paginator = self.pagination_class()
        page = paginator.paginate_queryset(queryset, request)
        if page is not None:
            serializer = GETBusinessSerializer(page, many=True)
            pagination_data = paginator.get_paginated_response(serializer.data)

        response_data = {**{
            'statusCode': 200,
            'status': 'Success'
        }, ** pagination_data}

        return Response(response_data)


class GetBusinessDetailsById(APIView):  # correct
    # permission_classes = [IsAuthenticated]
    def get(self, request, businessId, *args, **kwargs):
        try:
            instance = Business.objects.get(businessId=businessId)
            serializer = GETBusinessByIdSerializer(instance)

            response_data = {
                'statusCode': 200,
                'status': 'success',
                'data': serializer.data
            }
            return Response(response_data)

        except Business.DoesNotExist:
            response_data = {
                'statusCode': 404,
                'status': 'failed',
                'data': {'message': "Invalid BusinessId."}
            }
            return Response(response_data, status=404)
        except ValueError:
            response_data = {
                'statusCode': 404,
                'status': 'failed',
                'data': {'message': f"'BusinessId' excepted a number but got '{businessId}'."}
            }
            return Response(response_data, status=404)


class POSTNewBusiness(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request,  *args, **kwargs):

        get_user_id = get_user_id_from_token_view(request)
        serializer = CREATEBusinessSerializer(data=request.data, context={'user_id_by_token': get_user_id})
        if serializer.is_valid():
            serializer.save()
            response_data = {
                'statusCode': 200,
                'status': 'success',
                'data': {'message': 'Record Added Successfully.'}
            }
            return Response(response_data)
        response_data = {
            'statusCode': status.HTTP_400_BAD_REQUEST,
            'status': 'failed',
            'data': serializer.errors
        }
        return Response(response_data, status=400)


class PUTBusinessById(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, businessId, *args, **kwargs):
        try:

            instance = Business.objects.get(businessId=businessId)
            get_user_id = get_user_id_from_token_view(request)
            serializer = PUTBusinessSerializer(instance, data=request.data, partial=True, context={'user_id_by_token': get_user_id, 'business_id':businessId})

            if serializer.is_valid():
                serializer.save()
                response_data = {
                    'statusCode': status.HTTP_200_OK,
                    'status': 'success',
                    'data': {'message': 'Record updated successfully.'},
                }
                return Response(response_data)

            # Customize the response data if needed
            response_data = {
                'statusCode': status.HTTP_400_BAD_REQUEST,
                'status': 'failed',
                'data': serializer.errors,
            }
            return Response(response_data, status=400)

        except Business.DoesNotExist:
            response_data = {
                'statusCode': status.HTTP_400_BAD_REQUEST,
                'status': 'failed',
                'data': {'message': "Invalid Business Id."},
            }
            return Response(response_data, status=400)
