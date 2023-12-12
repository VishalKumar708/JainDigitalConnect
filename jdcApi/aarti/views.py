from rest_framework.generics import *
from rest_framework.views import APIView

from .serializer import *
from rest_framework import status
from rest_framework.response import Response
from jdcApi.models import Aarti, MstSect
from rest_framework.permissions import IsAuthenticated
from utils.get_id_by_token import get_user_id_from_token_view
from django.db.models import Q
from accounts.pagination import CustomPagination


class GETAllSectAarti(ListAPIView):
    """ Count 'Literature' by 'Sect' """
    serializer_class = GETAllSectWithCountForAartiSerializer

    def get_queryset(self):
        query_set = MstSect.objects.filter(isActive=True)
        return query_set

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        # print(queryset)
        if len(queryset) < 1:
            response_data = {
                'status': 200,
                'statusCode': 'success',
                'data': {'message': 'No Record Found!'}
            }
            return Response(response_data)
        serializer = self.get_serializer(queryset, many=True)

        response_data = {
            'status': 200,
            'statusCode': 'success',
            'data': serializer.data
        }
        return Response(response_data)


class GETAllApprovedAartiBySectId(APIView):
    pagination_class = CustomPagination

    def get(self, request, sectId, *args, **kwargs):
        try:
            queryset = Aarti.objects.filter(sectId=sectId, isActive=True, isVerified=True).order_by('aartiName')
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
                serializer = GETAartiSerializer(page, many=True)
                pagination_data = paginator.get_paginated_response(serializer.data)

            response_data = {**{
                'statusCode': 200,
                'status': 'Success'
            }, **pagination_data}
            return Response(response_data)
        except ValueError:
            response_data = {
                'statusCode': 400,
                'status': 'failed',
                'data': {'message': f" 'sectId' excepted a number but got '{sectId}'." },
            }
            return Response(response_data, status=400)
        except Exception as e:
            response_data = {
                'statusCode': 500,
                'status': 'error',
                'data': {'message': "Internal Server Error."},
            }
            return Response(response_data, status=500)


class GETAllApprovedAndUnapprovedAartiForAdmin(APIView):
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination

    def get(self, request, *args, **kwargs):
        try:
            status = request.GET.get('status')
            if status is None or status.strip().lower() == 'active':
                queryset = Aarti.objects.filter(isActive=True, isVerified=True).order_by('aartiName')
            elif status.strip().lower() == 'inactive':
                queryset = Aarti.objects.filter(Q(isActive=False) | Q(isVerified=False)).order_by('aartiName')
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
                serializer = GETAartiForAdminSerializer(page, many=True)
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
                'data': {'error':'Internal Server Error.'},
            }
            return Response(response_data, status=500)


class GETAartiDetailsById(APIView):
    # permission_classes = [IsAuthenticated]

    def get(self, request, aartiId, *args, **kwargs):
        try:
            instance = Aarti.objects.get(id=aartiId)
            serializer = GETAartiByIdSerializer(instance)
            response_data = {
                'statusCode': 200,
                'status': 'success',
                'data': serializer.data
            }
            return Response(response_data)

        except Aarti.DoesNotExist:
            response_data = {
                'statusCode': 404,
                'status': 'failed',
                'data': {'message': "Invalid Aarti Id."}
            }
            return Response(response_data, status=404)
        except ValueError:
            response_data = {
                'statusCode': 404,
                'status': 'failed',
                'data': {'message': f"excepted a number but you got '{aartiId}'."}
            }
            return Response(response_data, status=404)
        except Exception as e:
            response_data = {
                'statusCode': 500,
                'status': 'error',
                'data': {'message': 'Internal Server Error.'}
            }
            return Response(response_data, status=500)


class POSTNewAarti(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        try:
            get_user_id = get_user_id_from_token_view(request)
            serializer = CREATEAartiSerializer(data=request.data, context={'user_id_by_token': get_user_id})
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


class UPDATEAarti(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, aartiId, *args, **kwargs):
        try:
            get_user_id = get_user_id_from_token_view(request)
            instance = Aarti.objects.get(id=aartiId)
            serializer = UPDATEAartiSerializer(instance, data=request.data, partial=True, context={'user_id_by_token': get_user_id, 'aarti_id': aartiId})
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
        except Aarti.DoesNotExist:
            response_data = {
                'statusCode': 404,
                'status': 'failed',
                'data': {'message': "Invalid literature id."},
            }
            return Response(response_data, status=404)
        except ValueError:
            response_data = {
                'statusCode': 404,
                'status': 'failed',
                'data': {'message': f"'aarti id' excepted a number but got '{aartiId}'"},
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