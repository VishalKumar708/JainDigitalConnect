from rest_framework.generics import *
from rest_framework.views import APIView

from .serializer import *
from rest_framework import status
from rest_framework.response import Response
from jdcApi.models import Literature, MstSect
from rest_framework.permissions import IsAuthenticated
from utils.get_id_by_token import get_user_id_from_token_view
from django.db.models import Q
from accounts.pagination import CustomPagination

class GETAllSectLiterature(ListAPIView):
    """ Count 'Literature' by 'Sect' """
    serializer_class = GETAllSectWithCountForLiteratureSerializer

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


class GETAllApprovedLiteratureBySectId(APIView):
    pagination_class = CustomPagination

    def get(self, request, sectId, *args, **kwargs):
        try:
            queryset = Literature.objects.filter(sectId=sectId, isActive=True, isVerified=True).order_by('title')
            if len(queryset) < 1:
                response_data = {
                    'statusCode': 200,
                    'status': 'Success',
                    'data': {'message': 'No Record found.'}
                }

                return Response(response_data)
            # pagination
            pagination_data={}
            paginator = self.pagination_class()
            page = paginator.paginate_queryset(queryset, request)
            if page is not None:
                serializer = GETLiteratureSerializer(page, many=True)
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
                'data': {'message': f" 'sectId' excepted a number but got '{sectId}'." },
            }
            return Response(response_data, status=404)
        except Exception as e:
            response_data = {
                'statusCode': 500,
                'status': 'error',
                'data': {'error': str(e)},
            }
            return Response(response_data, status=500)


class GETAllApprovedAndUnapprovedLiterature(APIView):
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination

    def get(self, request, *args, **kwargs):
        try:
            status = request.GET.get('status')
            if status is None or status.strip().lower() == 'active':
                queryset = Literature.objects.filter(isActive=True, isVerified=True).order_by('title')
            elif status.strip().lower() == 'inactive':
                queryset = Literature.objects.filter(Q(isActive=False) | Q(isVerified=False)).order_by('title')
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
                serializer = GETLiteratureForAdminSerializer(page, many=True)
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


class GETLiteratureById(APIView):
    # permission_classes = [IsAuthenticated]

    def get(self, request, literatureId, *args, **kwargs):
        try:
            instance = Literature.objects.get(id=literatureId)
            serializer = GETLiteratureByIdSerializer(instance)
            response_data = {
                'statusCode': 200,
                'status': 'success',
                'data': serializer.data
            }
            return Response(response_data)

        except Literature.DoesNotExist:
            response_data = {
                'statusCode': 404,
                'status': 'failed',
                'data': {'message': "Invalid literature id."}
            }
            return Response(response_data, status=404)
        except ValueError:
            response_data = {
                'statusCode': 404,
                'status': 'failed',
                'data': {'literatureId': [f"excepted a number but you got '{literatureId}'."]}
            }
            return Response(response_data, status=404)
        except Exception as e:
            response_data = {
                'statusCode': 500,
                'status': 'error',
                'data': {'error': str(e)}
            }
            return Response(response_data, status=500)


class POSTNewLiterature(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        try:
            get_user_id = get_user_id_from_token_view(request)
            serializer = CREATELiteratureSerializer(data=request.data, context={'user_id_by_token': get_user_id})
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


class UPDATELiterature(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, literatureId, *args, **kwargs):
        try:
            get_user_id = get_user_id_from_token_view(request)
            instance = Literature.objects.get(id=literatureId)
            serializer = UPDATELiteratureSerializer(instance, data=request.data, partial=True, context={'user_id_by_token': get_user_id, 'literature_id': literatureId})
            if serializer.is_valid():
                serializer.save()
                response_data = {
                    'statusCode': status.HTTP_200_OK,
                    'status': 'Success',
                    'data': {'message': 'Record Updated Successfully.'}
                }
                return Response(response_data)
            response_data = {
                'statusCode': status.HTTP_400_BAD_REQUEST,
                'status': 'failed',
                'data': serializer.errors
            }
            return Response(response_data, status=400)
        except Literature.DoesNotExist:
            response_data = {
                'statusCode': status.HTTP_404_NOT_FOUND,
                'status': 'failed',
                'data': {'message': "Invalid literature id."},
            }
            return Response(response_data, status=404)
        except ValueError:
            response_data = {
                'statusCode': 404,
                'status': 'failed',
                'data': {'message': f"'literature id' excepted a number but got '{literatureId}'"},
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