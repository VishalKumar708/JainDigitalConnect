
from rest_framework.views import APIView

from .literatureDocument_serializer import *
from rest_framework.response import Response
from jdcApi.models import LiteratureDocument, MstSect
from rest_framework.permissions import IsAuthenticated
from utils.get_id_by_token import get_user_id_from_token_view
from django.db.models import Q
from accounts.pagination import CustomPagination


class POSTNewLiteratureDocument(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        try:
            get_user_id = get_user_id_from_token_view(request)
            serializer = CREATENewLiteratureDocumentSerializer(data=request.data, context={'user_id_by_token': get_user_id})
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
                'data': {'error': str(e)},
            }
            return Response(response_data, status=500)


class PUTLiteratureDocumentById(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, literatureDocumentId, *args, **kwargs):
        try:
            get_user_id = get_user_id_from_token_view(request)
            instance = LiteratureDocument.objects.get(id=literatureDocumentId)
            serializer = UPDATELiteratureDocumentByIdSerializer(instance, data=request.data, partial=True, context={'user_id_by_token': get_user_id})
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
        except LiteratureDocument.DoesNotExist:
            response_data = {
                'statusCode': 404,
                'status': 'failed',
                'data': {'message': "Invalid literatureDocument id."},
            }
            return Response(response_data, status=404)
        except ValueError:
            response_data = {
                'statusCode': 404,
                'status': 'failed',
                'data': {'message': f"'literatureDocument id' excepted a number but got '{literatureDocumentId}'"},
            }
            return Response(response_data, status=404)


class GETLiteratureDocumentDetailsById(APIView):
    # permission_classes = [IsAuthenticated]

    def get(self, request, literatureDocumentId, *args, **kwargs):
        try:
            instance = LiteratureDocument.objects.get(id=literatureDocumentId)
            serializer = GETLiteratureDocumentDetailsSerializer(instance)
            response_data = {
                'statusCode': 200,
                'status': 'failed',
                'data': serializer.data
            }
            return Response(response_data)
        except LiteratureDocument.DoesNotExist:
            response_data = {
                'statusCode': 404,
                'status': 'failed',
                'data': {'message': "Invalid literatureDocument id."},
            }
            return Response(response_data, status=404)
        except ValueError:
            response_data = {
                'statusCode': 404,
                'status': 'failed',
                'data': {'message': f"'literatureDocument id' excepted a number but got '{literatureDocumentId}'"},
            }
            return Response(response_data, status=404)


class GETAllSectLiteratureDocument(APIView):
    """ Count 'LiteratureDocument' by 'Sect' """

    def get(self, request, *args, **kwargs):
        queryset = MstSect.objects.filter(isActive=True)
        if len(queryset) < 1:
            response_data = {
                'status': 200,
                'statusCode': 'success',
                'data': {'message': 'No Record Found!'}
            }
            return Response(response_data)
        serializer = GETAllSectWithCountForLiteratureDocumentSerializer(queryset, many=True)

        response_data = {
            'status': 200,
            'statusCode': 'success',
            'data': serializer.data
        }
        return Response(response_data)


class GETAllLiteratureDocumentForAdmin(APIView):
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination

    def get(self, request, *args, **kwargs):
        try:
            status = request.GET.get('status')
            if status is None or status.strip().lower() == 'active':
                queryset = LiteratureDocument.objects.filter(isActive=True, isVerified=True).order_by('title')
            elif status.strip().lower() == 'inactive':
                queryset = LiteratureDocument.objects.filter(Q(isActive=False) | Q(isVerified=False)).order_by('title')
            else:
                response_data = {
                    'status': 400,
                    'statusCode': 'failed',
                    'data': {'message': f"'status' expected 'active' or 'inactive' value, but got '{status}'."}
                }
                return Response(response_data, status=400)

            # queryset = self.get_queryset()
            if len(queryset) < 1:
                response_data = {
                    'statusCode': 200,
                    'status': 'Success',
                    'data': {'message': 'No Record found.'}
                }

                return Response(response_data)
            # pagination
            pagination_data = {}
            paginator = self.pagination_class()
            page = paginator.paginate_queryset(queryset, request)
            if page is not None:
                serializer = GETAllActiveLiteratureDocumentSerializer(page, many=True)
                pagination_data = paginator.get_paginated_response(serializer.data)
            # serializer = self.get_serializer(queryset, many=True)
            response_data = {**{
                'statusCode': 200,
                'status': 'Success'
            }, **pagination_data}

            return Response(response_data)
        except Exception as e:
            response_data = {
                'statusCode': 500,
                'status': 'error',
                'data': {'error': str(e)},
            }
            return Response(response_data, status=500)


class GETAllApprovedLiteratureDocument(APIView):
    pagination_class = CustomPagination

    def get(self, request, *args, **kwargs):
        try:
            queryset = LiteratureDocument.objects.filter(isActive=True, isVerified=True).order_by('title')
            # queryset = self.get_queryset()
            if len(queryset) < 1:
                response_data = {
                    'statusCode': 200,
                    'status': 'Success',
                    'data': {'message': 'No Record found.'}
                }

                return Response(response_data)
            # pagination
            pagination_data = {}
            paginator = self.pagination_class()
            page = paginator.paginate_queryset(queryset, request)
            if page is not None:
                serializer = GETAllActiveLiteratureDocumentSerializer(page, many=True)
                pagination_data = paginator.get_paginated_response(serializer.data)
            # serializer = self.get_serializer(queryset, many=True)
            response_data = {**{
                'statusCode': 200,
                'status': 'Success'
            }, **pagination_data}

            return Response(response_data)
        except Exception as e:
            response_data = {
                'statusCode': 500,
                'status': 'error',
                'data': {'error': str(e)},
            }
            return Response(response_data, status=500)