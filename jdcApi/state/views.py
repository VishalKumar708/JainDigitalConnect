
from rest_framework.generics import *
from rest_framework.views import APIView

from .serializer import *
from rest_framework import status
from rest_framework.response import Response
from django.db.models import Q
from jdcApi.models import State
from utils.get_id_by_token import get_user_id_from_token_view
# from utils.permission import IsOwnerOrReadOnly
from rest_framework.permissions import IsAuthenticated


class GetAllApprovedState(ListAPIView):
    permission_classes = []
    serializer_class = GETStateSerializer

    def get_queryset(self):
        queryset = State.objects.filter(isActive=True, isVerified=True).order_by('stateName')
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        # Customize the response data as needed
        if len(queryset) < 1:
            response_data = {
                'statusCode': status.HTTP_200_OK,
                'status': 'Success',
                'data': {'message': 'Record Not Found'}
            }
            return Response(response_data)

        serializer = self.get_serializer(queryset, many=True)

        response_data = {
            'statusCode': status.HTTP_200_OK,
            'status': 'Success',
            'data': serializer.data,
        }

        return Response(response_data)


class GetAllUnapprovedState(ListAPIView):
    serializer_class = GETStateSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = State.objects.filter(Q(isActive=False) | Q(isVerified=False)).order_by('stateName')
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        if len(serializer.data) < 1:
            response_data = {
                'status_code': status.HTTP_200_OK,
                'status': 'Success',
                'data': {'message': 'No Record Found'}
            }
            return Response(response_data)
        # Customize the response data as needed
        response_data = {
            'status_code': status.HTTP_200_OK,
            'status': 'Success',
            'data': serializer.data,
        }
        return Response(response_data)


class GetStateById(APIView):
    def get(self, request, stateId):
        try:
            obj = State.objects.get(stateId=stateId)
            serializer = GETStateSerializer(obj)

            response = {
                'statusCode': 200,
                'status': 'success',
                'data': serializer.data
            }
            return Response(response, status=200)
        except State.DoesNotExist:
            response = {
                'statusCode': status.HTTP_404_NOT_FOUND,
                'status': 'failed',
                'data': {'error': 'Invalid State Id.'}
            }
            return Response(response, status=404)
        except Exception as e:
            response = {
                'statusCode': status.HTTP_404_NOT_FOUND,
                'status': 'error',
                'data': {'message': str(e)}
            }
            return Response(response, status=200)


class GetCitiesByStateId(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, stateId, *args, **kwargs):
        try:
            int(stateId)
            instance = State.objects.get(stateId__iexact=stateId)
            serializer = GetAllCitiesByStateSerializer(instance)
            data = serializer.data
            if len(data) < 1:
                response_data = {
                    'status_code': status.HTTP_200_OK,
                    'status': 'success',
                    'data': {'message': "No Record found."}
                }
                return Response(response_data)
            response_data = {
                'status_code': status.HTTP_200_OK,
                'status': 'success',
                'totalCities': len(data['cities']),
                'data': data
            }
            return Response(response_data)
        except State.DoesNotExist:
            response_data = {
                'statusCode': status.HTTP_404_NOT_FOUND,
                'status': 'failed',
                'data': {'message': "Invalid State Id."}
            }
            return Response(response_data, status=404)
        except ValueError:
            response_data = {
                'statusCode': 400,
                'status': 'failed',
                'data': {'message': f"'State Id' excepted a number but got '{stateId}'."}
            }
            return Response(response_data, status=400)
        # except Exception as e:
        #     response_data = {
        #         'status_code': status.HTTP_500_INTERNAL_SERVER_ERROR,
        #         'status': 'error',
        #         'data': {'error': str(e)},
        #     }
        #     return Response(response_data, status=500)


class POSTNewState(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        try:
            # fetch 'user_id' from token payload
            get_user_id = get_user_id_from_token_view(request)
            serializer = CREATEStateSerializer(data=request.data, context={'user_id_by_token': get_user_id})
            if serializer.is_valid():
                serializer.save()
                response_data = {
                    'status_code': status.HTTP_200_OK,
                    'status': 'success',
                    'message': {'message': 'Record Added Successfully.'},
                }
                return Response(response_data, status=200)

            response_data = {
                'status_code': status.HTTP_400_BAD_REQUEST,
                'status': 'failed',
                'message': serializer.errors
            }
            return Response(response_data, status=400)

        except Exception as e:
            # Handle the case when request data is not valid
            response_data = {
                'status_code': status.HTTP_500_INTERNAL_SERVER_ERROR,
                'status': 'error',
                'data': {'error': str(e)},
            }
            return Response(response_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UpdateStateById(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, stateId, *args, **kwargs):
        try:
            instance = State.objects.get(stateId=stateId)

            get_user_id = get_user_id_from_token_view(request)

            serializer = CREATEStateSerializer(instance, data=request.data,  context={'user_id_by_token': get_user_id, 'put_method': True, 'state_id':stateId})

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
                'statusCode': status.HTTP_400_BAD_REQUEST,
                'status': 'failed',
                'data': serializer.errors,
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
        except State.DoesNotExist:
            response_data = {
                'status_code': status.HTTP_400_BAD_REQUEST,
                'status': 'failed',
                'data': {'message': "Invalid State Id."},
            }
            return Response(response_data, status=400)
        except Exception as e:
            response_data = {
                'status_code': status.HTTP_500_INTERNAL_SERVER_ERROR,
                'status': 'error',
                'data': {'error': str(e)},
            }
            return Response(response_data, status=500)

