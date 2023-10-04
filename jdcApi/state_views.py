
from rest_framework.generics import *
from rest_framework.views import APIView

from .serializers import *
from rest_framework import status
from rest_framework.response import Response
from django.db.models import Q
from .models import State
from utils.get_id_by_token import get_user_id_from_token_view
from utils.permission import IsOwnerOrReadOnly
from rest_framework.permissions import IsAuthenticated


class GetAllApprovedState(ListAPIView):
    permission_classes = [IsOwnerOrReadOnly]
    serializer_class = GETStateSerializer

    def get_queryset(self):
        queryset = State.objects.filter(isActive=True, isVerified=True).order_by('stateName')
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)

        # Customize the response data as needed
        if len(serializer.data) == 0:
            response_data = {
                'statusCode': status.HTTP_200_OK,
                'status': 'Success',
                'data': {'msg': 'No state found.'}
            }
            return Response(response_data)

        # data = serializer.data
        response_data = {
            'statusCode': status.HTTP_200_OK,
            'status': 'Success',
            'data': serializer.data,
        }

        return Response(response_data, status=200)


class GetAllUnapprovedState(ListAPIView):
    serializer_class = GETStateSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = State.objects.filter(Q(isActive=False) | Q(isVerified=False)).order_by('stateName')
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        if len(serializer.data) == 0:
            data = {'msg': 'No Record Found'}
        else:
            data = serializer.data
        # Customize the response data as needed
        response_data = {
            'status_code': status.HTTP_200_OK,
            'status': 'Success',
            'data': data,
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
                'TotalCities': len(data['city_by_state']),
                'data': data
            }
            return Response(response_data)
        except State.DoesNotExist:
            response_data = {
                'status_code': status.HTTP_404_NOT_FOUND,
                'status': 'failed',
                'data': {'message': "Invalid State Id."}
            }
            return Response(response_data, status=404)
        except Exception as e:
            response_data = {
                'status_code': status.HTTP_500_INTERNAL_SERVER_ERROR,
                'status': 'error',
                'data': {'error': str(e)},
            }
            return Response(response_data, status=500)


class CreateNewState(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        try:
            # check city already exist or not
            state_name = request.data.get('stateName')
            matching_state_count = State.objects.filter(stateName__iexact=state_name).count()
            if matching_state_count > 0:
                json_data = {
                    'status_code': status.HTTP_302_FOUND,
                    'status': 'failed',
                    'message': {'msg': f"'{state_name}' is already exists."},
                }
                return Response(json_data, status=302)
            get_user_id = get_user_id_from_token_view(request)
            serializer = CREATEStateSerializer(data=request.data, context={'user_id_by_token': get_user_id})

            if serializer.is_valid():
                serializer.save()
                response_data = {
                    'status_code': status.HTTP_200_OK,
                    'status': 'success',
                    'message': {'message': 'State created successfully.'},
                }
                return Response(response_data, status=200)

            response_data = {
                'status_code': status.HTTP_400_BAD_REQUEST,
                'status': 'failed',
                'message': serializer.errors
            }
            return Response(response_data, status=404)

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
            # check user provide value or not
            if len(request.data) < 1:
                serializer = CREATEStateSerializer(instance, data=request.data)
                serializer.is_valid(raise_exception=True)
                response_data = {
                    'status_code': status.HTTP_204_NO_CONTENT,
                    'status': 'failed',
                    'message': serializer.errors,
                }
                return Response(response_data, status=status.HTTP_204_NO_CONTENT)

            # check updated state is available or not
            state_name = request.data.get('stateName')
            matching_state_counts = State.objects.filter(Q(stateName__iexact=state_name), ~Q(stateId=stateId)).count()
            print('count ==> ', matching_state_counts)
            if matching_state_counts > 0:
                json_data = {
                    'status_code': status.HTTP_302_FOUND,
                    'status': 'failed',
                    'message': {'msg': f"'{state_name}' is already exists."},
                }
                return Response(json_data, status=status.HTTP_302_FOUND)

            get_user_id = get_user_id_from_token_view(request)

            serializer = CREATEStateSerializer(instance, data=request.data, partial=True, context={'user_id_by_token': get_user_id})

            if serializer.is_valid():
                serializer.save()
                response_data = {
                    'statusCode': status.HTTP_200_OK,
                    'status': 'success',
                    'data': {'msg': 'New State Added Successfully.'}
                }
                return Response(response_data)

            # Customize the response data if needed
            response_data = {
                'status_code': status.HTTP_400_BAD_REQUEST,
                'status': 'failed',
                'message': serializer.errors,
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

