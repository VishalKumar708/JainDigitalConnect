from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from .serializer import *
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from utils.get_id_by_token import get_user_id_from_token_view
from jdcApi.models import Saint, MstSect
from accounts.pagination import CustomPagination
import logging
error_logger = logging.getLogger('error')
info_logger = logging.getLogger('info')


class GETAllSectSaint(ListAPIView):
    """ Count 'Saint' by 'Sect' """
    serializer_class = GETAllSectWithCountForSaintSerializer

    def get_queryset(self):
        query_set = MstSect.objects.all()
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


class POSTNewSaint(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        """ Create New Saint Record."""
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
            response_data = {
                'status': 500,
                'statusCode': 'error',
                'data': {'message': "Internal Server error."}
            }
            return Response(response_data, status=500)


class PUTSaintById(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, id, *args, **kwargs):
        """ Update existing record by 'id'."""
        try:
            saint_obj = Saint.objects.get(id=id)
            get_user_id = get_user_id_from_token_view(request)
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
        except Saint.DoesNotExist or ValueError:
            response_data = {
                'status': 404,
                'statusCode': 'failed',
                'data': {'message': 'Invalid Id'}
            }
            error_logger.error(f'Invalid Saint Id. While updating record.')
            return Response(response_data, status=404)
        except ValueError:
            response_data = {
                'status': 404,
                'statusCode': 'failed',
                'data': {'message': f"'id' excepted a number but got '{id}'."}
            }
            error_logger.error(f'Invalid Saint Id. While updating record.')
            return Response(response_data, status=404)
        except Exception as e:
            error_logger.error(f'An Exception occured while updating new saint {e}')
            response_data = {
                'status': 500,
                'statusCode': 'error',
                'data': {'message': "Internal Server error."}
            }
            return Response(response_data, status=500)


# for search
class GETAllSaintsBySearchParam(APIView):
    pagination_class = CustomPagination

    def get(self, request, sectId, *args, **kwargs):
        """ Search saint in specific sect by 'saintName' param"""

        try:
            MstSect.objects.get(id=sectId)
            search_param = request.GET.get('saintName')
            if search_param:
                queryset = Saint.objects.filter(isVerified=True, sectId=sectId, name__icontains=search_param.strip()).order_by('name')
            else:
                response_data = {
                    'status': 400,
                    'statusCode': 'failed',
                    'data': {'message': "Please pass value inside search param 'saintName' to search saint."}
                }
                return Response(response_data, status=400)

            if len(queryset) < 1:
                response_data = {
                    'status': 200,
                    'statusCode': 'success',
                    'data': {'message': 'No Record Found!'}
                }
                return Response(response_data)

            serializer = GETAllSaintSerializer(queryset, many=True)
            response_data = {
                    'status': 200,
                    'statusCode': 'success',
                    'data': serializer.data
                }
            return Response(response_data)
        except MstSect.DoesNotExist:
            response_data = {
                'status': 404,
                'statusCode': 'failed',
                'data': {'message': 'Invalid SectId.'}
            }

            return Response(response_data, status=404)
        except ValueError:
            response_data = {
                'status': 404,
                'statusCode': 'failed',
                'data': {'message': f"'id' expected a number but got '{sectId}'. "}
            }
            return Response(response_data, status=404)
        except Exception as e:
            error_logger.error(f'An Exception occured while searching saint by name {e}')
            response_data = {
                'status': 500,
                'statusCode': 'error',
                'data': {'error': "Internal Server error."}
            }
            return Response(response_data, status=500)


class GETAllActiveSaintBySectId(APIView):
    pagination_class = CustomPagination

    def get(self, request, sectId, *args, **kwargs):
        """Get all active records by sectId in 'Saint' model."""
        search_param = request.GET.get('gender')
        pagination_data = {}
        try:
            MstSect.objects.get(id=sectId)
            if search_param:
                queryset = Saint.objects.filter(sectId=sectId, gender=search_param.strip().capitalize(), isVerified=True).order_by('name')
            else:
                queryset = Saint.objects.filter(sectId=sectId, isVerified=True).order_by('name')
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
                pagination_data = paginator.get_paginated_response(serializer.data)
            #
            # serializer = GETAllSaintBySectIdSerializer(queryset, many=True)

            response_data = {**{
                'status': 200,
                'statusCode': 'success',
                # 'data': serializer.data
            }, ** pagination_data}
            return Response(response_data)

        except MstSect.DoesNotExist:
            response_data = {
                'status': 404,
                'statusCode': 'failed',
                'data': {'message': 'invalid sectId'}
            }
            return Response(response_data, status=404)
        except ValueError:
            response_data = {
                'status': 404,
                'statusCode': 'failed',
                'data': {'message': f" 'saintId' excepted a number but got '{sectId}'."}
            }
            return Response(response_data, status=404)
        except Exception as e:
            error_logger.error(f'An Exception occured while searching saint by gender {e}')
            response_data = {
                'status': 500,
                'statusCode': 'error',
                'data': {'message': "Internal Server error."}
            }
            return Response(response_data, status=500)


class GETAllAddAndApprovedSaint(APIView):
    pagination_class = CustomPagination

    def get(self, request, *args, **kwargs):
        """ show all active and inactive saint by a query param 'status' """
        try:
            search_param = request.GET.get('status')
            # queryset = None
            if search_param:
                pagination_data = {}
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
                    pagination_data = paginator.get_paginated_response(serializer.data)

                # if pagination is disable
                # serializer = GETAllSaintForAdminSerializer(queryset, many=True)

                response_data = {**{
                    'status': 200,
                    'statusCode': 'success',
                    # 'data': serializer.data
                }, **pagination_data}
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
            response_data = {
                'status': 500,
                'statusCode': 'error',
                'data': {'message': "Internal Server error."}
            }
            return Response(response_data, status=500)


class GETSaintDetailById(APIView):

    def get(self, request, saintId, *args, **kwargs):
        """ show all details by 'saintId'."""
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
                'status': 404,
                'statusCode': 'failed',
                'data': {'message': f" saintId excepted a number but got '{saintId}'."}
            }
            return Response(response_data, status=404)
        except Exception as e:
            error_logger.error(f'An Exception occured while fetching individual saint record. {e}')
            response_data = {
                'status': 500,
                'statusCode': 'error',
                'data': {'message': "Internal Server error."}
            }
            return Response(response_data, status=500)
