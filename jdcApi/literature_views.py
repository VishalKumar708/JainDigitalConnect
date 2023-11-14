from rest_framework.generics import *
from rest_framework.views import APIView

from .serializers import GETLiteratureSerializer, GETLiteratureByIdSerializer, CREATELiteratureSerializer, UPDATELiteratureSerializer
from rest_framework import status
from rest_framework.response import Response
from .models import Literature
from rest_framework.permissions import IsAuthenticated
from utils.get_id_by_token import get_user_id_from_token_view
from django.db.models import Q
from rest_framework.exceptions import ValidationError
from django.http import Http404

class GetAllApprovedLiterature(ListAPIView):

    serializer_class = GETLiteratureSerializer

    def get_queryset(self):
        return Literature.objects.filter(isActive=True, isVerified=True).order_by('title')

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


class GetAllUnapprovedLiterature(ListAPIView):
    serializer_class = GETLiteratureSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Literature.objects.filter(Q(isActive=False) | Q(isVerified=False)).order_by('title')

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


class GetLiteratureById(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, literatureId, *args, **kwargs):
        try:
            if not literatureId.isdigit():
                response_data = {
                    'statusCode': status.HTTP_400_BAD_REQUEST,
                    'status': 'failed',
                    'data': {'literatureId': [f"business Id must be 'int' but you got '{literatureId}'."]}
                }
                return Response(response_data, status=400)

            instance = Literature.objects.get(literatureId=literatureId)
            serializer = GETLiteratureByIdSerializer(instance)

            response_data = {
                'statusCode': status.HTTP_200_OK,
                'status': 'success',
                'data': serializer.data
            }
            return Response(response_data)

        except Literature.DoesNotExist:
            response_data = {
                'statusCode': status.HTTP_404_NOT_FOUND,
                'status': 'failed',
                'data': {'message': "Invalid literature id."}
            }
            return Response(response_data, status=404)
        except Exception as e:
            response_data = {
                'statusCode': status.HTTP_500_INTERNAL_SERVER_ERROR,
                'status': 'error',
                'data': {'error': str(e)}
            }
            return Response(response_data, status=500)


class CreateNewLiterature(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        try:
            if request.data.get('title'):
                matching_literature_count = Literature.objects.filter(title__iexact=request.data.get('title')).count()
                if matching_literature_count > 0:
                    response_data = {
                        'statusCode': status.HTTP_302_FOUND,
                        'status': 'failed',
                        'data': {'message': 'This literature is already exist.'}
                    }
                    return Response(response_data, status=302)

            get_user_id = get_user_id_from_token_view(request)
            serializer = CREATELiteratureSerializer(data=request.data, context={'user_id_by_token': get_user_id})
            if serializer.is_valid():
                serializer.save()
                response_data = {
                    'statusCode': status.HTTP_200_OK,
                    'status': 'Success',
                    'data': {'message': 'New literature added successfully.'}
                }
                return Response(response_data)
            response_data = {
                'statusCode': status.HTTP_400_BAD_REQUEST,
                'status': 'failed',
                'data': serializer.errors
            }
            return Response(response_data, status=400)
        except Exception as e:
            response_data = {
                'statusCode': status.HTTP_500_INTERNAL_SERVER_ERROR,
                'status': 'error',
                'data': {'error': str(e)},
            }
            return Response(response_data, status=500)


class UPDATELiterature(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, literatureId, *args, **kwargs):
        try:

            instance = Literature.objects.get(literatureId=literatureId)
            if len(request.data) == 0:
                serializer = UPDATELiteratureSerializer(data=request.data)
                if not serializer.is_valid():
                    response_data = {
                        'statusCode': status.HTTP_400_BAD_REQUEST,
                        'status': 'failed',
                        'data': serializer.errors
                    }
                    return Response(response_data, status=400)

            literatureName = request.data.get('title')
            get_literature_name = literatureName.strip() if literatureName else literatureName
            matching_literature_counts = Literature.objects.filter(Q(title__iexact=get_literature_name), ~Q(literatureId=literatureId),).count()

            if matching_literature_counts > 0:
                json_data = {
                    'statuscode': status.HTTP_302_FOUND,
                    'status': 'failed',
                    'message': {'msg': f"'{literatureName}' is already exists."},
                }
                return Response(json_data, status=status.HTTP_302_FOUND)

            get_user_id = get_user_id_from_token_view(request)
            serializer = UPDATELiteratureSerializer(instance, data=request.data, partial=True, context={'user_id_by_token': get_user_id})
            if serializer.is_valid():
                serializer.save()
                response_data = {
                    'statusCode': status.HTTP_200_OK,
                    'status': 'Success',
                    'data': {'message': 'literature updated successfully.'}
                }
                return Response(response_data)
            response_data = {
                'statusCode': status.HTTP_400_BAD_REQUEST,
                'status': 'failed',
                'data': serializer.errors
            }
            return Response(response_data, status=404)
        except Literature.DoesNotExist:
            response_data = {
                'statusCode': status.HTTP_404_NOT_FOUND,
                'status': 'failed',
                'data': {'message': "Invalid literature id."},
            }
            return Response(response_data, status=404)
        # except Exception as e:
        #     response_data = {
        #         'statusCode': status.HTTP_500_INTERNAL_SERVER_ERROR,
        #         'status': 'error',
        #         'data': {'error': str(e)},
        #     }
        #     return Response(response_data, status=500)

#