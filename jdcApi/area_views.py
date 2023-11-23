from rest_framework.generics import *
from rest_framework.views import APIView

from .serializers import *
from rest_framework import status
from rest_framework.response import Response

from django.db.models import Q
from .models import Area
from utils.get_id_by_token import get_user_id_from_token_view
from rest_framework.permissions import IsAuthenticated


class GetAllApprovedAreasByCityId(APIView):

    def get(self, request, cityId, *args, **kwargs):
        try:
            City.objects.get(cityId=cityId)
            area_name = request.GET.get('areaName')

            # if query param is not empty
            if area_name:
                queryset = Area.objects.filter(isActive=True, isVerified=True, areaName__icontains=area_name.strip())
                if len(queryset) < 1:
                    response_data = {
                        'statusCode': status.HTTP_200_OK,
                        'status': 'Success',
                        'data': {'message': 'Record Not Found'}
                    }
                    return Response(response_data)
                serializer = GETAreaSerializer(queryset, many=True)
                response_data = {
                    'status_code': status.HTTP_200_OK,
                    'status': 'Success',
                    'data': serializer.data,
                }
                return Response(response_data)
            else:
                queryset = Area.objects.filter(isActive=True, isVerified=True).order_by('areaName')
                if len(queryset) < 1:
                    response_data = {
                        'statusCode': status.HTTP_200_OK,
                        'status': 'Success',
                        'data': {'message': 'Record Not Found'}
                    }
                    return Response(response_data)

                serializer = GETAreaWithCountSerializer(queryset, many=True)
                response_data = {
                    'status_code': status.HTTP_200_OK,
                    'status': 'Success',
                    'data': serializer.data,
                }
                return Response(response_data)
        # exceptions
        except City.DoesNotExist:
            response_data = {
                'statusCode': status.HTTP_400_BAD_REQUEST,
                'status': 'failed',
                'data': {'message': "Invalid City Id."},
            }
            return Response(response_data, status=400)
        except ValueError:
            response_data = {
                'statusCode': 400,
                'status': 'failed',
                'data': {'message': f"'City Id' excepted a number but got '{cityId}'."},
            }
            return Response(response_data, status=400)
        except Exception as e:
            response_data = {
                'status_code': status.HTTP_500_INTERNAL_SERVER_ERROR,
                'status': 'error',
                'data': {'error': str(e)},
            }
            return Response(response_data, status=500)
#


class GetAllApprovedAndUnapprovedAreasForAdmin(ListAPIView):

    def get(self, request, *args, **kwargs):
        try:
            status = request.GET.get('status')
            if status is None:
                response_data = {
                    'statusCode': 400,
                    'status': 'failed',
                    'data': {"message": "Please pass query param 'status' value 'active/inactive' only."},
                }
                return Response(response_data, status=400)

            if status.strip().lower() == 'active':
                queryset = Area.objects.filter(isActive=True, isVerified=True).order_by('areaName')
            elif status.strip().lower() == 'inactive':
                queryset = Area.objects.filter(Q(isActive=False) | Q(isVerified=False)).order_by('areaName')
            else:
                response_data = {
                    'statusCode': 400,
                    'status': 'failed',
                    'data': {"message": "Please enter correct value 'active/inactive' only."},
                }
                return Response(response_data, status=400)

            if len(queryset) < 1:
                response_data = {
                    'statusCode': 200,
                    'status': 'Success',
                    'data': {'message': 'Record Not Found'}
                }
                return Response(response_data)

            serializer = GETAreaForAdminSerializer(queryset, many=True)
            response_data = {
                'statusCode': 200,
                'status': 'Success',
                'data': serializer.data,
            }
            return Response(response_data)
        except Exception as e:
            response_data = {
                'status_code': 500,
                'status': 'error',
                'data': {'error': str(e)},
            }
            return Response(response_data, status=500)


class GetAreaDetailsById(APIView):
    def get(self, request, areaId, *args, **kwargs):
        try:
            instance = Area.objects.get(areaId=areaId)
            serializer = GETAreaByAreaIdSerializer(instance)

            response_data = {
                'statusCode': status.HTTP_200_OK,
                'status': 'success',
                'data': serializer.data
            }
            return Response(response_data)
        except Area.DoesNotExist:
            response_data = {
                'statusCode': status.HTTP_404_NOT_FOUND,
                'status': 'failed',
                'data': {'message': "Invalid AreaId."}
            }
            return Response(response_data, status=404)
        except ValueError:
            response_data = {
                'statusCode': 400,
                'status': 'failed',
                'data': {'message': f"'areaId' excepted a number but got '{areaId}'."}
            }
            return Response(response_data, status=400)
        except Exception as e:
            response_data = {
                'statusCode': status.HTTP_500_INTERNAL_SERVER_ERROR,
                'status': 'error',
                'data': {'error': str(e)}
            }
            return Response(response_data, status=500)


class POSTNewArea(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        try:
            get_user_id = get_user_id_from_token_view(request)
            serializer = CREATEAreaSerializer(data=request.data, context={'user_id_by_token': get_user_id})
            if serializer.is_valid():
                serializer.save()
                response_data = {
                    'statusCode': status.HTTP_200_OK,
                    'status': 'success',
                    'data': {'message': 'Record Added Successfully.'},
                }
                return Response(response_data, status=200)
            response_data = {
                'statusCode': status.HTTP_400_BAD_REQUEST,
                'status': 'failed',
                'data': serializer.errors,
            }
            return Response(response_data, status=400)
        except Exception as e:
            # Handle the case when request data is not valid
            response_data = {
                'statusCode': status.HTTP_500_INTERNAL_SERVER_ERROR,
                'status': 'error',
                'data': {'error': str(e)},
            }
            return Response(response_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UpdateAreaById(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, areaId, *args, **kwargs):
        try:
            area_instance = Area.objects.get(areaId=areaId)
            # Save the updated state object
            get_user_id = get_user_id_from_token_view(request)
            serializer = UPDATEAreaSerializer(area_instance, data=request.data, partial=True,  context={'user_id_by_token': get_user_id, 'area_id':areaId})
            if serializer.is_valid():
                serializer.save()
                response_data = {
                    'statusCode': status.HTTP_200_OK,
                    'status': 'success',
                    'data': {'message': 'Record Updated Successfully.'},
                }
                return Response(response_data, status=200)
            response_data = {
                'statusCode': status.HTTP_400_BAD_REQUEST,
                'status': 'failed',
                'data': serializer.errors,
            }
            return Response(response_data, status=400)
        except Area.DoesNotExist:
            response_data = {
                'statusCode': status.HTTP_400_BAD_REQUEST,
                'status': 'failed',
                'data': {'message': "Invalid Area Id."},
            }
            return Response(response_data, status=400)
        except ValueError:
            response_data = {
                'statusCode': 400,
                'status': 'failed',
                'data': {'message': f"'Area Id' excepted a number but got '{areaId}'."},
            }
            return Response(response_data, status=400)
        # except Exception as e:
        #     response_data = {
        #         'statusCode': status.HTTP_500_INTERNAL_SERVER_ERROR,
        #         'status': 'error',
        #         'data': {'error': str(e)},
        #     }
        #     return Response(response_data, status=500)

from accounts.serializers import GETAllMemberByAreaIdSerializer, GETAllFamilyByAreaIdSerializer, SearchResidentsInAreaSerializer
from accounts.pagination import CustomPagination
class GETAllResidentsByAreaId(APIView):
    pagination_class = CustomPagination

    def get(self, request, areaId, *args, **kwargs):
        try:
            Area.objects.get(areaId=areaId)
            resident_type = request.GET.get('residentType')
            search_resident_name = request.GET.get('residentName')
            data = {}
            #  for searching
            if search_resident_name:
                search_result = User.objects.filter(areaId=areaId, name__icontains=search_resident_name.strip())
                if len(search_result) < 1:
                    response_data = {
                        'statusCode': 200,
                        'status': 'success',
                        'data': {'message': 'No Record Found.'},
                    }
                    return Response(response_data, status=200)
                serializer = SearchResidentsInAreaSerializer(search_result, many=True)
                response_data = {
                    'statusCode': 200,
                    'status': 'success',
                    'data': serializer.data,
                }
                return Response(response_data, status=200)

            #  for getting members/family
            if resident_type is None or resident_type.strip().lower() == 'family':
                family_queryset = User.objects.filter(areaId=areaId, headId=None).order_by('name')
                total_family = len(family_queryset)
                total_member = User.objects.filter(areaId=areaId).count()
                if total_family < 1:
                    response_data = {
                        'statusCode': 200,
                        'status': 'success',
                        'data': {'message': 'No Record Found.'},
                    }
                    return Response(response_data, status=200)
                # apply pagination
                paginator = self.pagination_class()
                page = paginator.paginate_queryset(family_queryset, request)
                if page is not None:
                    serializer = GETAllFamilyByAreaIdSerializer(page, many=True)
                    data = paginator.get_paginated_response(serializer.data)

                # if pagination is disable
                # serializer = GETAllFamilyByAreaIdSerializer(family_queryset, many=True)

            elif resident_type.strip().lower() == 'member':
                members_queryset = User.objects.filter(areaId=areaId).order_by('name')
                total_member = len(members_queryset)
                print('total_member ==> ', total_member)
                total_family = User.objects.filter(areaId=areaId, headId=None).count()
                if total_member < 1:
                    response_data = {
                        'statusCode': 200,
                        'status': 'success',
                        'data': {'message': 'No Record Found.'},
                    }
                    return Response(response_data, status=200)
                # apply pagination
                paginator = self.pagination_class()
                page = paginator.paginate_queryset(members_queryset, request)
                if page is not None:
                    serializer = GETAllMemberByAreaIdSerializer(members_queryset, many=True)
                    data = paginator.get_paginated_response(serializer.data)

                # if pagination is disable
                # serializer = GETAllMemberByAreaIdSerializer(members_queryset, many=True)
            else:
                response_data = {
                    'statusCode': status.HTTP_400_BAD_REQUEST,
                    'status': 'failed',
                    'data': {'message': f"'residentType' query param value must be 'family/member'."},
                }
                return Response(response_data, status=400)

            response_data = {**{
                'statusCode': 200,
                'status': 'failed',
                'memberCount': total_member,
                'familyCount': total_family,
            }, **data}
            return Response(response_data, status=200)
        except Area.DoesNotExist:
            response_data = {
                'statusCode': 404,
                'status': 'failed',
                'data': {'message': "Invalid Area Id."},
            }
            return Response(response_data, status=404)
        except ValueError:
            response_data = {
                'statusCode': 400,
                'status': 'failed',
                'data': {'message': f"'Area Id' excepted a number but got '{areaId}'."},
            }
            return Response(response_data, status=400)
