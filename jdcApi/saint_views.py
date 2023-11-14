from rest_framework.views import APIView
from .serializers import CREATESaintSerializer, UPDATESaintSerializer, GETAllSaintSerializer, GETSaintByIdSerializer, GETAllSaintBySectIdSerializer, GETAllSaintForAdminSerializer
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from utils.get_id_by_token import get_user_id_from_token_view
from .models import Saint, Sect
from accounts.pagination import CustomPagination
import logging
error_logger = logging.getLogger('error')
info_logger = logging.getLogger('info')


class POSTNewSaint(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        try:
            get_user_id = get_user_id_from_token_view(request)
            serializer = CREATESaintSerializer(data=request.data, context={'user_id_by_token': get_user_id})
            if serializer.is_valid():
                serializer.save()
                response_data = {
                    'status': 200,
                    'statusCode': 'success',
                    'data': {'message': 'Record Added Successfully.'}
                }
                info_logger.info('Saint Created Successfully.')
                return Response(response_data)
            response_data = {
                'status': 400,
                'statusCode': 'failed',
                'data': serializer.errors
            }
            return Response(response_data, status=400)
        except Exception as e:
            error_logger.error(f'An Exception occured while creating new saint {e}')


class PUTSaintById(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, id, *args, **kwargs):
        try:
            saint_obj = Saint.objects.get(id=id)
            get_user_id = get_user_id_from_token_view(request)
            # print('get_user_id==> ', get_user_id)
            serializer = UPDATESaintSerializer(data=request.data, instance=saint_obj, partial=True, context={'user_id_by_token': get_user_id})
            if serializer.is_valid():
                serializer.save()
                response_data = {
                    'status': 200,
                    'statusCode': 'success',
                    'data': {'message': 'Record Updated Successfully.'}
                }
                info_logger.info('Saint Updated Successfully.')
                return Response(response_data)
            response_data = {
                'status': 400,
                'statusCode': 'failed',
                'data': serializer.errors
            }
            return Response(response_data, status=400)
        except Saint.DoesNotExist:
            response_data = {
                'status': 404,
                'statusCode': 'failed',
                'data': {'message': 'Invalid Id'}
            }
            error_logger.error(f'Invalid Saint Id. While updating record.')
            return Response(response_data, status=404)
        except Exception as e:
            error_logger.error(f'An Exception occured while updating new saint {e}')


# for search
class GETAllSaintsBySearchParam(APIView):
    pagination_class = CustomPagination

    def get(self, request, sectId, *args, **kwargs):
        """ Search saint in specific sect by 'search' param"""

        try:
            Sect.objects.get(id=sectId)
            search_param = request.GET.get('search')
            if search_param:
                queryset = Saint.objects.filter(isVerified=True, selectSect=sectId, name__icontains=search_param.strip()).order_by('name')
            else:
                queryset = Saint.objects.filter(isVerified=True, selectSect=sectId).order_by('name')

            if len(queryset) < 1:
                response_data = {
                    'status': 200,
                    'statusCode': 'success',
                    'data': {'message': 'No Record Found!'}
                }
                return Response(response_data)
            paginator = self.pagination_class()
            page = paginator.paginate_queryset(queryset, request)
            if page is not None:
                serializer = GETAllSaintSerializer(page, many=True)
                return paginator.get_paginated_response(serializer.data)

            serializer = GETAllSaintSerializer(queryset, many=True)
            response_data = {
                    'status': 200,
                    'statusCode': 'success',
                    'data': serializer.data
                }
            return Response(response_data)
        except Sect.DoesNotExist:
            response_data = {
                'status': 404,
                'statusCode': 'failed',
                'data': {'message': 'Invalid SectId.'}
            }

            return Response(response_data, status=404)
        except ValueError:
            response_data = {
                'status': 400,
                'statusCode': 'failed',
                'data': {'message': f"'id' expected a number but got '{sectId}'. "}
            }
            return Response(response_data, status=400)
        except Exception as e:
            error_logger.error(f'An Exception occured while searching saint by name {e}')


class GETAllActiveSaintBySectIdUsingSearchParam(APIView):
    pagination_class = CustomPagination

    def get(self, request, sectId, *args, **kwargs):
        search_param = request.GET.get('gender')
        try:
            Sect.objects.get(id=sectId)
            if search_param:
                queryset = Saint.objects.filter(selectSect=sectId, gender=search_param.strip().capitalize(), isVerified=True).order_by('name')
            else:
                queryset = Saint.objects.filter(selectSect=sectId, isVerified=True).order_by('name')
            if len(queryset) < 1:
                response_data = {
                    'status': 200,
                    'statusCode': 'success',
                    'data': {'message': 'Record Not found'}
                }
                return Response(response_data)
            paginator = self.pagination_class()
            page = paginator.paginate_queryset(queryset, request)
            if page is not None:
                serializer = GETAllSaintBySectIdSerializer(page, many=True)
                return paginator.get_paginated_response(serializer.data)
            else:
                serializer = GETAllSaintBySectIdSerializer(queryset, many=True)

            response_data = {
                'status': 200,
                'statusCode': 'success',
                'data': serializer.data
            }
            return Response(response_data)

        except Sect.DoesNotExist:
            response_data = {
                'status': 404,
                'statusCode': 'failed',
                'data': {'message': 'invalid sectId'}
            }
            return Response(response_data, status=404)
        except ValueError:
            response_data = {
                'status': 400,
                'statusCode': 'failed',
                'data': {'message': f" 'saintId' excepted a number but got '{sectId}'."}
            }
            return Response(response_data,status=404)
        except Exception as e:
            error_logger.error(f'An Exception occured while searching saint by gender {e}')


class GETAllAddAndApprovedSaint(APIView):
    pagination_class = CustomPagination

    def get(self, request, *args, **kwargs):
        try:
            search_param = request.GET.get('status')
            # queryset = None
            if search_param:
                if search_param.strip().lower() == 'active':
                    queryset = Saint.objects.filter(isVerified=True).order_by('name')
                elif search_param.strip().lower() == 'inactive':
                    queryset = Saint.objects.filter(isVerified=False).order_by('name')
                else:
                    response_data = {
                        'status': 400,
                        'statusCode': 'failed',
                        'data': {'message': f"'status' expected 'active' or 'inactive' value, but got '{search_param}'."}
                    }
                    return Response(response_data, status=400)

                if len(queryset) < 1:
                    response_data = {
                        'status': 200,
                        'statusCode': 'success',
                        'data': {'message': 'Record Not found'}
                    }
                    return Response(response_data)

                # apply pagination
                paginator = self.pagination_class()
                page = paginator.paginate_queryset(queryset, request)
                if page is not None:
                    serializer = GETAllSaintForAdminSerializer(page, many=True)
                    return paginator.get_paginated_response(serializer.data)

                # if pagination is disable
                serializer = GETAllSaintForAdminSerializer(queryset, many=True)

                response_data = {
                    'status': 200,
                    'statusCode': 'success',
                    'data': serializer.data
                }
                return Response(response_data)
            else:
                response_data = {
                    'status': 400,
                    'statusCode': 'failed',
                    'data': {'message': f"'status' expected 'active' or 'inactive' value, but got '{search_param}'."}
                }
                return Response(response_data, status=400)
        except Exception as e:
            error_logger.error(f'An Exception occured while fetching data in "GETAllAddAndApprovedSaint" api view. {e}')


class GETSaintDetailById(APIView):

    def get(self, request, saintId, *args, **kwargs):
        try:
            saint_obj = Saint.objects.get(id=saintId)
            # print(saint_obj.dob)
            serializer = GETSaintByIdSerializer(saint_obj)
            response_data = {
                'status': 200,
                'statusCode': 'success',
                'data': serializer.data
            }
            return Response(response_data)

        except Saint.DoesNotExist:
            response_data = {
                'status': 404,
                'statusCode': 'failed',
                'data': {'message': 'invalid saintId'}
            }
            return Response(response_data, status=404)
        except ValueError:
            response_data = {
                'status': 400,
                'statusCode': 'failed',
                'data': {'message': f" saintId excepted a number but got '{saintId}'."}
            }
            return Response(response_data, status=404)
        except Exception as e:
            error_logger.error(f'An Exception occured while fetching individual saint record. {e}')


