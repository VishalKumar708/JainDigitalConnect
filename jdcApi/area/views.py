from rest_framework.generics import *
from rest_framework.views import APIView

from .serializer import *
from rest_framework import status
from rest_framework.response import Response

from django.db.models import Q
from jdcApi.models import Area, City
from utils.get_id_by_token import get_user_id_from_token_view
from rest_framework.permissions import IsAuthenticated


class GetAllApprovedAndUnapprovedAreasForAdmin(ListAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        # try:
        status = request.GET.get('status')
        if status is None:
            response_data = {
                'statusCode': 400,
                'status': 'failed',
                'data': {"message": "Please pass query param 'status' value 'active/inactive' only."},
            }
            return Response(response_data, status=400)

        if status.strip().lower() == 'active':
            queryset = Area.objects.filter(isActive=True, isVerified=True).order_by('areaName')
        elif status.strip().lower() == 'inactive':
            queryset = Area.objects.filter(Q(isActive=False) | Q(isVerified=False)).order_by('areaName')
        else:
            response_data = {
                'statusCode': 400,
                'status': 'failed',
                'data': {"message": "Please enter correct value 'active/inactive' only."},
            }
            return Response(response_data, status=400)

        if len(queryset) < 1:
            response_data = {
                'statusCode': 200,
                'status': 'Success',
                'data': {'message': 'Record Not Found'}
            }
            return Response(response_data)

        serializer = GETAreaForAdminSerializer(queryset, many=True)
        response_data = {
            'statusCode': 200,
            'status': 'Success',
            'data': serializer.data,
        }
        return Response(response_data)


class GetAreaDetailsById(APIView):
    permission_classes = [IsAuthenticated]

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
        except ValueError:
            response_data = {
                'statusCode': 404,
                'status': 'failed',
                'data': {'message': f"'areaId' excepted a number but got '{areaId}'."}
            }
            return Response(response_data, status=404)



class POSTNewArea(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):

        get_user_id = get_user_id_from_token_view(request)
        serializer = CREATEAreaSerializer(data=request.data, context={'user_id_by_token': get_user_id})
        if serializer.is_valid():
            serializer.save()
            response_data = {
                'statusCode': status.HTTP_200_OK,
                'status': 'success',
                'data': {'message': 'Record Added Successfully.'},
            }
            return Response(response_data, status=200)
        response_data = {
            'statusCode': status.HTTP_400_BAD_REQUEST,
            'status': 'failed',
            'data': serializer.errors,
        }
        return Response(response_data, status=400)


class UpdateAreaById(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, areaId, *args, **kwargs):
        try:
            area_instance = Area.objects.get(areaId=areaId)
            # Save the updated state object
            get_user_id = get_user_id_from_token_view(request)
            serializer = UPDATEAreaSerializer(area_instance, data=request.data, partial=True,  context={'user_id_by_token': get_user_id, 'area_id':areaId})
            if serializer.is_valid():
                serializer.save()
                response_data = {
                    'statusCode': status.HTTP_200_OK,
                    'status': 'success',
                    'data': {'message': 'Record Updated Successfully.'},
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
                'statusCode': 404,
                'status': 'failed',
                'data': {'message': "Invalid Area Id."},
            }
            return Response(response_data, status=404)
        except ValueError:
            response_data = {
                'statusCode': 400,
                'status': 'failed',
                'data': {'message': f"'Area Id' excepted a number but got '{areaId}'."},
            }
            return Response(response_data, status=400)
