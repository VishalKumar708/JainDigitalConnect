from rest_framework.generics import ListAPIView
from rest_framework.views import APIView

from .serializers import CREATEBusinessSerializer, UPDATEBusinessSerializer, GETBusinessSerializer, GETBusinessByIdSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from utils.get_id_by_token import get_user_id_from_token_view
from .models import Business, City
from django.db.models import Q


# class GetAllApprovedBusiness(ListAPIView):
#
#     serializer_class = GETBusinessSerializer
#
#     def get_queryset(self):
#         return Business.objects.filter(isActive=True, isVerified=True).order_by('businessName')
#
#     def list(self, request, *args, **kwargs):
#         try:
#             queryset = self.get_queryset()
#
#             if len(queryset) == 0:
#                 response_data = {
#                     'statusCode': status.HTTP_200_OK,
#                     'status': 'Success',
#                     'data': {'message': 'No Record found.'}
#                 }
#
#                 return Response(response_data)
#
#             serializer = self.get_serializer(queryset, many=True)
#             response_data = {
#                 'statusCode': status.HTTP_200_OK,
#                 'status': 'Success',
#                 'data': serializer.data,
#             }
#
#             return Response(response_data)
#         except Exception as e:
#             response_data = {
#                 'statusCode': status.HTTP_500_INTERNAL_SERVER_ERROR,
#                 'status': 'error',
#                 'data': {'error': str(e)},
#             }
#             return Response(response_data, status=500)


class GetAllApprovedBusinessByCityId(APIView):
    # serializer_class = GETBusinessSerializer
    def get_queryset(self):
        return Business.objects.filter(isActive=True, isVerified=True).order_by('businessName')

    def get(self, request,cityId, *args, **kwargs):
        try:
            int(cityId)
            City.objects.get(cityId=cityId)
            business_name = request.GET.get('businessName')
            if business_name:
                queryset = Business.objects.filter(isActive=True, isVerified=True, businessName__icontains=business_name)
            else:
                queryset = Business.objects.filter(isActive=True, isVerified=True).order_by('businessName')
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
        except City.DoesNotExist:
            response_data = {
                'statusCode': 404,
                'status': 'failed',
                'data': {'message': 'Invalid City Id.'},
            }
            return Response(response_data, status=404)
        except ValueError:
            response_data = {
                'statusCode': 400,
                'status': 'failed',
                'data': {'message': f"'cityId' excepted a number but got '{cityId}'."},
            }
            return Response(response_data, status=400)
        except Exception as e:
            response_data = {
                'statusCode': status.HTTP_500_INTERNAL_SERVER_ERROR,
                'status': 'error',
                'data': {'error': str(e)},
            }
            return Response(response_data, status=500)


class GetAllUnapprovedBusiness(ListAPIView):
    serializer_class = GETBusinessSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        return Business.objects.filter(Q(isActive=False) | Q(isVerified=False)).order_by('businessName')

    def list(self, request, *args, **kwargs):
        try:
            queryset = self.get_queryset()

            if len(queryset) == 0:
                response_data = {
                    'statusCode': status.HTTP_200_OK,
                    'status': 'Success',
                    'data': {'message': 'No Record found.'}
                }

                return Response(response_data)

            serializer = self.get_serializer(queryset, many=True)
            response_data = {
                'statusCode': status.HTTP_200_OK,
                'status': 'Success',
                'data': serializer.data,
            }

            return Response(response_data)
        except Exception as e:
            response_data = {
                'statusCode': status.HTTP_500_INTERNAL_SERVER_ERROR,
                'status': 'error',
                'data': {'error': str(e)},
            }
            return Response(response_data, status=500)


class GetBusinessById(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, businessId, *args, **kwargs):
        try:
            if not businessId.isdigit():
                response_data = {
                    'statusCode': status.HTTP_400_BAD_REQUEST,
                    'status': 'success',
                    'data': {'businessId': [f"business Id must be 'int' but you got '{businessId}'."]}
                }
                return Response(response_data, status=400)
            instance = Business.objects.get(businessId=businessId)
            serializer = GETBusinessByIdSerializer(instance)

            response_data = {
                'statusCode': status.HTTP_200_OK,
                'status': 'success',
                'data': serializer.data
            }
            return Response(response_data)

        except Business.DoesNotExist:
            response_data = {
                'statusCode': status.HTTP_404_NOT_FOUND,
                'status': 'failed',
                'data': {'message': "Invalid BusinessId."}
            }
            return Response(response_data, status=404)
        except Exception as e:
            response_data = {
                'statusCode': status.HTTP_500_INTERNAL_SERVER_ERROR,
                'status': 'error',
                'data': {'error': str(e)}
            }
            return Response(response_data, status=500)


class CreateNewBusiness(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        try:
            business_name = request.data.get('businessName')
            user_id = request.data.get('userId')

            # if business_name and user_id is not None
            if business_name and user_id:
                matching_business_count = Business.objects.filter(businessName__iexact=business_name, userId=user_id).count()
                if matching_business_count > 0:
                    response_data = {
                        'statusCode': status.HTTP_302_FOUND,
                        'status': 'failed',
                        'data': {'message': 'You had already added this business.'}
                    }
                    return Response(response_data, status=302)

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

