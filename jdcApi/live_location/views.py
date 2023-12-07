from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .serializer import *
from utils.get_id_by_token import get_user_id_from_token_view
from accounts.pagination import CustomPagination
from rest_framework.response import Response
from jdcApi.models import DharamSthanHistory, MstSect, DharamSthan, LiveLocation
from django.utils import timezone


class GETAllSectDharamSthanHistory(APIView):
    """ Count 'DharamSthanHistory' by 'Sect' """

    def get(self, request, *args, **kwargs):
        queryset = MstSect.objects.filter(isActive=True)
        # print(queryset)
        if len(queryset) < 1:
            response_data = {
                'status': 200,
                'statusCode': 'success',
                'data': {'message': 'No Record Found!'}
            }
            return Response(response_data)
        serializer = GETAllSectWithCountForDharamSthanHistorySerializer(queryset, many=True)
        response_data = {
            'status': 200,
            'statusCode': 'success',
            'data': serializer.data
        }
        return Response(response_data)


class GETAllDharamSthanHistoryBySectId(APIView):

    def get(self, request, sectId, *args, **kwargs):
        try:
            current_year = timezone.now().year
            queryset = DharamSthanHistory.objects.filter(
                isActive=True,
                dharamSthanId__isActive=True,
                dharamSthanId__isVerified=True,
                dharamSthanId__sectId=sectId,
                year=current_year
            )
            # print('query ==> ', queryset.query)
            # print("queryset==> ", queryset)
            if len(queryset) < 1:
                response_data = {
                    'status': 200,
                    'statusCode': 'success',
                    'data': {'message': 'No Record Found!'}
                }
                return Response(response_data)
            serializer = GETAllDharamSthanHistorySerializer(queryset, many=True)
            response_data = {
                'status': 200,
                'statusCode': 'success',
                'data': serializer.data
            }
            return Response(response_data)
        except ValueError:
            response_data = {
                'status': 404,
                'statusCode': 'failed',
                'data': {"message": f"'sectId' excepted a number but got '{sectId}'."}
            }
            return Response(response_data, status=404)


class GETDharamSthanDetailsByDharamSthanIdForLiveLocation(APIView):

    def get(self, request, dharamSthanId, *args, **kwargs):
        try:
            instance = DharamSthan.objects.get(id=dharamSthanId)
            serializer = GETDharamSthanDetailsSerializer(instance=instance)
            response_data = {
                'status': 200,
                'statusCode': 'success',
                'data': serializer.data
            }
            return Response(response_data)

        except DharamSthan.DoesNotExist:
            response_data = {
                'status': 404,
                'statusCode': 'failed',
                'data': {'message': "Invalid DharamSthan Id."}
            }
            return Response(response_data, status=404)
        except ValueError:
            response_data = {
                'status': 404,
                'statusCode': 'failed',
                'data': {'message': f"'DharamSthan Id' excepted a number but got '{dharamSthanId}'."}
            }
            return Response(response_data, status=404)


class POSTNewLiveLocation(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        try:
            get_user_id = get_user_id_from_token_view(request)
            serializer = CREATENewLiveLocationSerializer(data=request.data, context={'user_id_by_token': get_user_id})
            if serializer.is_valid():
                serializer.save()
                response_data = {
                    'statusCode': 200,
                    'status': 'Success',
                    'data': {'message': 'Record Added successfully.'}
                }
                return Response(response_data)
            response_data = {
                'statusCode': 400,
                'status': 'failed',
                'data': serializer.errors
            }
            return Response(response_data, status=400)
        except Exception as e:
            response_data = {
                'statusCode': 500,
                'status': 'error',
                'data': {'message': "Internal Server Error"},
            }
            return Response(response_data, status=500)


class PUTLiveLocationById(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, liveLocationId, *args, **kwargs):
        try:
            get_user_id = get_user_id_from_token_view(request)
            instance = LiveLocation.objects.get(id=liveLocationId)
            serializer = UPDATELiveLocationSerializer(instance, data=request.data, partial=True, context={'user_id_by_token': get_user_id})
            if serializer.is_valid():
                serializer.save()
                response_data = {
                    'statusCode': 200,
                    'status': 'Success',
                    'data': {'message': 'Record Updated Successfully.'}
                }
                return Response(response_data)
            response_data = {
                'statusCode': 400,
                'status': 'failed',
                'data': serializer.errors
            }
            return Response(response_data, status=400)
        except LiveLocation.DoesNotExist:
            response_data = {
                'statusCode': 404,
                'status': 'failed',
                'data': {'message': "Invalid liveLocation Id."},
            }
            return Response(response_data, status=404)
        except ValueError:
            response_data = {
                'statusCode': 404,
                'status': 'failed',
                'data': {'message': f"'liveLocation id' excepted a number but got '{liveLocationId}'"},
            }
            return Response(response_data, status=404)


class GETLiveLocationDetailsById(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, liveLocationId, *args, **kwargs):
        try:
            instance = LiveLocation.objects.get(id=liveLocationId)
            serializer = GETLiveLocationDetailByIdSerializer(instance)
            response_data = {
                'statusCode': 200,
                'status': 'success',
                'data': serializer.data
            }
            return Response(response_data)
        except LiveLocation.DoesNotExist:
            response_data = {
                'statusCode': 404,
                'status': 'failed',
                'data': {'message': "Invalid liveLocation Id."},
            }
            return Response(response_data, status=404)
        except ValueError:
            response_data = {
                'statusCode': 404,
                'status': 'failed',
                'data': {'message': f"'liveLocation id' excepted a number but got '{liveLocationId}'"},
            }
            return Response(response_data, status=404)


class GETAllLiveLocationByUserId(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, userId, *args, **kwargs):
        try:
            queryset = LiveLocation.objects.filter(createdBy=userId)
            if len(queryset) < 1:
                response_data = {
                    'statusCode': 200,
                    'status': 'success',
                    'data': {"message": "No Record Found."}
                }
                return Response(response_data)
            serializer = GETAllLiveLocationByUserIdSerializer(queryset, many=True)
            response_data = {
                'statusCode': 200,
                'status': 'success',
                'data': serializer.data
            }
            return Response(response_data)
        except ValueError:
            response_data = {
                'statusCode': 404,
                'status': 'failed',
                'data': {'message': f"'user id' excepted a number but got '{userId}'"},
            }
            return Response(response_data, status=404)