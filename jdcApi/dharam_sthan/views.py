from rest_framework.generics import *
from rest_framework.views import APIView

from .serializer import *
from rest_framework import status
from rest_framework.response import Response
from jdcApi.models import DharamSthan, City
from rest_framework.permissions import IsAuthenticated
from utils.get_id_by_token import get_user_id_from_token_view
from django.db.models import Q, Count
from accounts.pagination import CustomPagination
from masterApi.models import MstSect


class GETAllSectDharamSthan(ListAPIView):
    """ Count 'DharamSthan' by 'Sect' """
    serializer_class = GETAllSectWithCountForDharamSthanSerializer

    def get_queryset(self):
        # query_set = MstSect.objects.filter(isActive=True)
        query_set = MstSect.objects.filter(isActive=True).annotate(
            count=Count('dharamsthan', filter=Q(dharamsthan__isActive=True, dharamsthan__isVerified=True))
        ).values('id', 'sectName', 'count')
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


class GETAllCityBySectIdDharamSthan(APIView):
    pagination_class = CustomPagination

    def get(self, request, sectId, *args, **kwargs):
        try:
            city_name = request.GET.get('cityName')
            if city_name:
                queryset = City.objects.filter(isActive=True, isVerified=True, cityName__icontains=city_name)
                serializer = SearchCitySerializer(queryset, many=True)
                if len(queryset) < 1:
                    response_data = {
                        'statusCode': 200,
                        'status': 'Success',
                        'data': {'message': 'No Record found.'}
                    }

                    return Response(response_data)
                response_data = {
                    'statusCode': 200,
                    'status': 'Success',
                    'data': serializer.data
                }
                return Response(response_data)
            queryset = City.objects.filter(isActive=True, isVerified=True).annotate(
        count=Count('dharamsthan', filter=Q(dharamsthan__isActive=True, dharamsthan__isVerified=True))
        ).values('cityId', 'cityName', 'count').order_by('cityName')
            if len(queryset) < 1:
                response_data = {
                    'statusCode': 200,
                    'status': 'Success',
                    'data': {'message': 'No Record found.'}
                }

                return Response(response_data)

            serializer = GETAllCityWithCountForDharamSthanSerializer(queryset, many=True)

            response_data = {
                'statusCode': 200,
                'status': 'Success',
                'data': serializer.data
            }
            return Response(response_data)
        except ValueError:
            response_data = {
                'statusCode': 400,
                'status': 'failed',
                'data': {'message': f" 'sectId' excepted a number but got '{sectId}'."},
            }
            return Response(response_data, status=400)


class GETAllApprovedDharamSthanBySectId(APIView):
    pagination_class = CustomPagination

    def get(self, request, sectId, cityId,  *args, **kwargs):
        try:
            dharam_sthan_name = request.GET.get('dharamSthanName')
            if dharam_sthan_name:
                queryset = DharamSthan.objects.filter(cityId=cityId, sectId=sectId, isActive=True, isVerified=True, name__icontains=dharam_sthan_name.strip())
                if len(queryset) < 1:
                    response_data = {
                        'statusCode': 200,
                        'status': 'Success',
                        'data': {'message': 'No Record found.'}
                    }

                    return Response(response_data)
                serializer = SearchDharamSthanSerializer(queryset, many=True)
                response_data = {
                        'statusCode': 200,
                        'status': 'Success',
                        'data': serializer.data
                    }
                return Response(response_data)
            queryset = DharamSthan.objects.filter(cityId=cityId, sectId=sectId, isActive=True, isVerified=True).order_by('name')
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
                serializer = GETAllDharamSthanSerializer(page, many=True)
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
                'data': {'message': f" 'cityId' excepted a number but got '{cityId}'." },
            }
            return Response(response_data, status=404)
        # except Exception as e:
        #     response_data = {
        #         'statusCode': 500,
        #         'status': 'error',
        #         'data': {'message': "Internal Server Error."},
        #     }
        #     return Response(response_data, status=500)


class GETDharamSthanDetailsById(APIView):
    # permission_classes = [IsAuthenticated]

    def get(self, request, dharamSthanId, *args, **kwargs):
        try:
            instance = DharamSthan.objects.get(id=dharamSthanId)
            serializer = GETDharamSthanDetailsSerializer(instance)
            response_data = {
                'statusCode': 200,
                'status': 'success',
                'data': serializer.data
            }
            return Response(response_data)

        except DharamSthan.DoesNotExist:
            response_data = {
                'statusCode': 404,
                'status': 'failed',
                'data': {'message': "Invalid DharamSthan id."}
            }
            return Response(response_data, status=404)
        except ValueError:
            response_data = {
                'statusCode': 404,
                'status': 'failed',
                'data': {'message': f"excepted a number but you got '{dharamSthanId}'."}
            }
            return Response(response_data, status=404)



class POSTNewDharamSthan(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        # try:
            get_user_id = get_user_id_from_token_view(request)
            serializer = CREATEDharamSthanSerializer(data=request.data, context={'user_id_by_token': get_user_id})
            if serializer.is_valid():
                obj = serializer.save()
                response_data = {
                    'statusCode': 200,
                    'status': 'Success',
                    'data': {'message': 'Record Added successfully.', 'id': obj.id}
                }
                return Response(response_data)
            response_data = {
                'statusCode': 400,
                'status': 'failed',
                'data': serializer.errors
            }
            return Response(response_data, status=400)


class PUTDharamSthanById(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, dharamSthanId, *args, **kwargs):
        try:
            get_user_id = get_user_id_from_token_view(request)
            instance = DharamSthan.objects.get(id=dharamSthanId)
            serializer = UPDATEDharamSthanSerializer(instance, data=request.data, partial=True, context={'user_id_by_token': get_user_id, 'dharam_sthan_id': dharamSthanId})
            if serializer.is_valid():
                serializer.save()
                response_data = {
                    'statusCode': 200,
                    'status': 'Success',
                    'data': {'message': 'Record Updated Successfully.'}
                }
                return Response(response_data)
            response_data = {
                'statusCode': status.HTTP_400_BAD_REQUEST,
                'status': 'failed',
                'data': serializer.errors
            }
            return Response(response_data, status=404)
        except DharamSthan.DoesNotExist:
            response_data = {
                'statusCode': status.HTTP_404_NOT_FOUND,
                'status': 'failed',
                'data': {'message': "Invalid DharamSthan Id."},
            }
            return Response(response_data, status=404)
        except ValueError:
            response_data = {
                'statusCode': 404,
                'status': 'failed',
                'data': {'message': f"'DharamSthan id' excepted a number but got '{dharamSthanId}'"},
            }
            return Response(response_data, status=404)

#

#   ***************************************************    Admin Panel *************************************


class GETAllCityDharamSthanForAdmin(APIView):
    pagination_class = CustomPagination

    def get(self, request, *args, **kwargs):
        city_name = request.GET.get('cityName')
        if city_name:
            queryset = City.objects.filter(isActive=True, isVerified=True, cityName__icontains=city_name)
            serializer = SearchCitySerializer(queryset, many=True)
            if len(queryset) < 1:
                response_data = {
                    'statusCode': 200,
                    'status': 'Success',
                    'data': {'message': 'No Record found.'}
                }

                return Response(response_data)
            response_data = {
                'statusCode': 200,
                'status': 'Success',
                'data': serializer.data
            }
            return Response(response_data)
        queryset = City.objects.filter(isActive=True, isVerified=True).annotate(
            count=Count('dharamsthan')
        ).values('cityId', 'cityName', 'count').order_by('cityName')
        if len(queryset) < 1:
            response_data = {
                'statusCode': 200,
                'status': 'Success',
                'data': {'message': 'No Record found.'}
            }

            return Response(response_data)

        serializer = GETAllCityWithCountForDharamSthanForAdminSerializer(queryset, many=True)

        response_data = {
            'statusCode': 200,
            'status': 'Success',
            'data': serializer.data
        }
        return Response(response_data)


class GETAllApprovedAndUnapprovedDharamSthanByCityIdForAdmin(APIView):
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination

    def get(self, request, cityId, *args, **kwargs):
        status = request.GET.get('status')
        if status is None or status.strip().lower() == 'active':
            queryset = DharamSthan.objects.filter(cityId=cityId, isActive=True, isVerified=True).order_by('name')
        elif status.strip().lower() == 'inactive':
            queryset = DharamSthan.objects.filter(Q(cityId=cityId), Q(Q(isActive=False) | Q(isVerified=False))).order_by('name')
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
            serializer = GETAllDharamSthanForAdminSerializer(page, many=True)
            pagination_data = paginator.get_paginated_response(serializer.data)
        # serializer = self.get_serializer(queryset, many=True)
        response_data = {**{
            'statusCode': 200,
            'status': 'Success'
        }, **pagination_data}

        return Response(response_data)

