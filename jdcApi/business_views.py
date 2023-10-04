from rest_framework.generics import *
from rest_framework.views import APIView

from .serializers import CREATEBusinessSerializer, UPDATEBusinessSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from utils.get_id_by_token import get_user_id_from_token_view

from .models import Business

from django.db.models import Q
from rest_framework.exceptions import ValidationError
from django.http import Http404


# class GetAllApprovedBusiness(ListAPIView):
#     queryset = Business.objects.all()
#     serializer_class = PartialBusinessSerializer
#
#     def list(self, request, *args, **kwargs):
#         queryset = self.filter_queryset(self.get_queryset().filter(isActive=True, isVerified=True))
#         serializer = self.get_serializer(queryset, many=True)
#
#         # Customize the response data as needed
#         if len(serializer.data) == 0:
#             data = {'msg': 'No Business found.'}
#             status_code = status.HTTP_204_NO_CONTENT
#         else:
#             data = serializer.data
#             status_code = status.HTTP_200_OK
#         response_data = {
#             'status_code': status_code,
#             'status': 'Success',
#             'data': data,
#         }
#
#         return Response(response_data)
#
#
# class GetAllUnapprovedBusiness(ListAPIView):
#     queryset = Business.objects.all()
#     serializer_class = BusinessSerializer
#
#     def list(self, request, *args, **kwargs):
#         queryset = self.filter_queryset(self.get_queryset().filter(isActive=False, isVerified=False)).order_by('businessName')
#         serializer = self.get_serializer(queryset, many=True)
#         if len(serializer.data) == 0:
#             data = {'msg': 'Business Not Found.'}
#             status_code = status.HTTP_204_NO_CONTENT
#         else:
#             data = serializer.data
#             status_code = status.HTTP_200_OK
#         # Customize the response data as needed
#         response_data = {
#             'status_code': status_code,
#             'status': 'Success',
#             'data': data,
#         }
#
#         return Response(response_data)
#
#
# class GetBusinessById(RetrieveAPIView):
#     serializer_class = BusinessSerializer
#     lookup_field = 'businessId'
#
#     def get_queryset(self):
#         return Business.objects.all()
#
#     def retrieve(self, request, *args, **kwargs):
#         try:
#             print(self.get_queryset())
#             instance = self.get_object()
#
#         except (Http404, ValidationError):
#
#             msg = {'msg': 'No match Found.Please input valid BusinessId.'}
#             json_data = {
#                 'status_code': status.HTTP_404_NOT_FOUND,
#                 'status': 'error',
#                 'data': msg
#             }
#             return Response(json_data)
#
#         serializer = self.get_serializer(instance)
#         json_data = {
#             'status_code': status.HTTP_200_OK,
#             'status': 'Success',
#             'data': serializer.data,
#         }
#         return Response(json_data)


class CreateNewBusiness(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        try:
            get_user_id = get_user_id_from_token_view(request)
            serializer = CREATEBusinessSerializer(data=request.data, context={'user_id_by_token': get_user_id})
            if serializer.is_valid():
                serializer.save()
                response_data = {
                    'statusCode': status.HTTP_200_OK,
                    'status': 'success',
                    'data': {'message': 'New Business Added Successfully.'}
                }
                return Response(response_data)
            response_data = {
                'statusCode': status.HTTP_400_BAD_REQUEST,
                'status': 'failed',
                'data': serializer.errors
            }
            return Response(response_data)

        except Exception as e:
            # Handle the case when request data is not valid
            response_data = {
                'statusCode': status.HTTP_500_INTERNAL_SERVER_ERROR,
                'status': 'error',
                'data': {'error': str(e)},
            }
            return Response(response_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UpdateBusinessById(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, businessId, *args, **kwargs):
        try:
            # check user provide value or not
            if len(request.data) < 1:
                serializer = UPDATEBusinessSerializer(data=request.data)
                if not serializer.is_valid():
                    response_data = {
                        'statusCode': status.HTTP_204_NO_CONTENT,
                        'status': 'failed',
                        'data': serializer.errors,
                    }
                    return Response(response_data, status=status.HTTP_204_NO_CONTENT)

            instance = Business.objects.get(businessId=businessId)
            get_user_id = get_user_id_from_token_view(request)
            serializer = UPDATEBusinessSerializer(instance, data=request.data, partial=True, context={'user_id_by_token': get_user_id})

            if serializer.is_valid():
                serializer.save()
                response_data = {
                    'statusCode': status.HTTP_200_OK,
                    'status': 'success',
                    'data': {'message': 'Business updated successfully.'},
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
        # except Exception as e:
        #     response_data = {
        #         'statusCode': status.HTTP_500_INTERNAL_SERVER_ERROR,
        #         'status': 'error',
        #         'data': {'error': str(e)},
        #     }
        #     return Response(response_data, status=500)

