from django.db.models.functions import Concat
from jdcApi.models import City, Area, MstSect
from rest_framework.response import Response
from .serializer import *
from rest_framework.views import APIView
from accounts.serializers import GETAllMemberByAreaIdSerializer, GETAllFamilyByAreaIdSerializer, SearchResidentsInAreaSerializer
from accounts.pagination import CustomPagination
from rest_framework.permissions import IsAuthenticated
from django.db.models import Count, Q, Case, When, Value, F, CharField, Func


class GETAllApprovedCityAndSearchCityName(APIView):
    """ show all approved city and search 'cityName' by user."""
    def get(self, request, *args, **kwargs):
        # try:
        #  for search city Name

        cityName = request.GET.get('cityName')
        if cityName:
            queryset = City.objects.filter(isActive=True, isVerified=True, isActiveForResidents=True, cityName__icontains=cityName.strip()).order_by('cityName')
            if len(queryset) < 1:
                response_data = {
                    'statusCode': 200,
                    'status': 'Success',
                    'data': {"message": "No Results found !"},
                }
                return Response(response_data)

            serializer = GETCitySerializer(queryset, many=True)
            response_data = {
                'statusCode': 200,
                'status': 'Success',
                'data': serializer.data,
            }
            return Response(response_data)

        queryset = City.objects.filter(isActive=True, isVerified=True, isActiveForResidents=True).annotate(
            count=Count('user', filter=Q(user__isActive=True, user__isVerified=True))).values('cityId', 'cityName', 'count').order_by('cityName')
        if len(queryset) < 1:
            response_data = {
                'statusCode': 200,
                'status': 'Success',
                'data': {"message": "No Results found !"},
            }
            return Response(response_data)

        serializer = GETCityWithCountSerializer(queryset, many=True)
        response_data = {
            'status_code': 200,
            'status': 'Success',
            'data': serializer.data,
        }
        return Response(response_data)


class GetAllApprovedAreasByCityId(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, cityId, *args, **kwargs):
        try:
            # City.objects.get(cityId=cityId)
            area_name = request.GET.get('areaName')
            search_resident_name = request.GET.get('residentName')

            # search areaName
            if area_name:
                queryset = Area.objects.filter(isActive=True, isVerified=True,cityId=cityId, areaName__icontains=area_name.strip())
                if len(queryset) < 1:
                    response_data = {
                        'statusCode': 200,
                        'status': 'Success',
                        'data': {'message': 'Record Not Found'}
                    }
                    return Response(response_data)
                serializer = GETAreaSerializer(queryset, many=True)
                response_data = {
                    'status_code': 200,
                    'status': 'Success',
                    'data': serializer.data,
                }
                return Response(response_data)
            # search 'residents' in a 'city'
            if search_resident_name:
                queryset = User.objects.filter(cityId=cityId, name__icontains=search_resident_name.strip())
                if len(queryset) < 1:
                    response_data = {
                        'statusCode': 200,
                        'status': 'success',
                        'data': {'message': 'No Record Found.'},
                    }
                    return Response(response_data, status=200)
                serializer = SearchResidentByCityIdSerializer(queryset, many=True)
                response_data = {
                    'statusCode': 200,
                    'status': 'success',
                    'data': serializer.data,
                }
                return Response(response_data, status=200)
            # return all the areas
            queryset = Area.objects.filter(
                isActive=True, isVerified=True, cityId=cityId
                ).annotate(
                count=Count('user', filter=Q(user__isActive=True, user__isVerified=True, user__sectId=cityId)),
                memberCount=Count('user', filter=Q(user__isActive=True, user__isVerified=True)),
                familyCount=Count('user', filter=Q(user__isActive=True, user__isVerified=True, user__headId=None))
            ).order_by('areaName')
            print('queryset==> ', queryset)
            if len(queryset) < 1:
                response_data = {
                    'statusCode': 200,
                    'status': 'Success',
                    # 'memberCount': User.objects.filter(cityId=cityId).count(),
                    # 'familyCount': User.objects.filter(cityId=cityId, headId=None).count(),
                    'data': {'message': 'Record Not Found'}
                }
                return Response(response_data)

            serializer = GETAreaWithCountSerializer(queryset, many=True)
            response_data = {
                'status_code': 200,
                'status': 'Success',
                # 'memberCount': User.objects.filter(cityId=cityId).count(),
                # 'familyCount': User.objects.filter(cityId=cityId, headId=None).count(),
                'data': serializer.data,
            }
            return Response(response_data)
        # exceptions
        except ValueError:
            response_data = {
                'statusCode': 404,
                'status': 'failed',
                'data': {'message': f"'City Id' excepted a number but got '{cityId}'."},
            }
            return Response(response_data, status=404)


from utils.models.custom_queries import calculate_age_expression
from django.utils import timezone


class GETAllResidentsByAreaId(APIView):
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination

    def get_all_members(self, request, areaId):
        members_queryset = User.objects.filter(areaId=areaId).annotate(
            age=calculate_age_expression('dob', User)
        ).order_by('name')

        if len(members_queryset) < 1:
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

            return Response({**{
                'statusCode': 200,
                'status': 'success',
            }, **data}, status=200)

    def get_all_head_users(self, request, areaId):
        family_queryset = User.objects.filter(areaId=areaId, headId=None). \
            annotate(age=calculate_age_expression('dob', User)).order_by('name')

        if len(family_queryset) < 1:
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
            return Response({**{
                'statusCode': 200,
                'status': 'success',
            }, **data}, status=200)

    def get(self, request, areaId, *args, **kwargs):
        try:
            # Area.objects.get(areaId=areaId)
            resident_type = request.GET.get('residentType')
            search_resident_name = request.GET.get('residentName')
            data = {}
            #  for searching resident
            if search_resident_name:
                search_result = User.objects.filter(areaId=areaId, name__icontains=search_resident_name.strip()
                                                    ).annotate(age=calculate_age_expression('dob', User))
                if len(search_result) < 1:
                    response_data = {
                        'statusCode': 200,
                        'status': 'success',
                        'data': {'message': 'No Record Found.'},
                    }
                    return Response(response_data, status=200)
                serializer = SearchResidentByCityIdSerializer(search_result, many=True)
                response_data = {
                    'statusCode': 200,
                    'status': 'success',
                    'data': serializer.data,
                }
                return Response(response_data, status=200)

            #  for getting members/family records
            if resident_type is None or resident_type.strip().lower() == 'family':
                return self.get_all_head_users(request=request, areaId=areaId)

            elif resident_type.strip().lower() == 'member':
                return self.get_all_members(request=request, areaId=areaId)

            else:
                response_data = {
                    'statusCode': 400,
                    'status': 'success',
                    'data': {'message': f"'residentType' query param value must be 'family/member'."},
                }
                return Response(response_data, status=400)

        except Area.DoesNotExist:
            response_data = {
                'statusCode': 404,
                'status': 'failed',
                'data': {'message': "Invalid Area Id."},
            }
            return Response(response_data, status=404)
        except ValueError:
            response_data = {
                'statusCode': 404,
                'status': 'failed',
                'data': {'message': f"'Area Id' excepted a number but got '{areaId}'."},
            }
            return Response(response_data, status=404)

#  **********************************************      Show Residents SectWise   *****************************


class GETAllSectResident(APIView):
    """ show all approved city and search 'cityName' by user."""
    def get(self, request, *args, **kwargs):
        try:
            queryset = MstSect.objects.filter(isActive=True).annotate(
            count=Count('user', filter=Q(user__isActive=True, user__isVerified=True))).values('id', 'sectName', 'count').order_by('order')
            # print(queryset)
            if len(queryset) < 1:
                response_data = {
                    'statusCode': 200,
                    'status': 'Success',
                    'data': {"message": "No Record found."},
                }
                return Response(response_data)

            serializer = GETSectWithCountSerializer(queryset, many=True)
            response_data = {
                'status_code': 200,
                'status': 'Success',
                'data': serializer.data,
            }
            return Response(response_data)
        except Exception as e:
            response_data = {
                'status_code': 500,
                'status': 'error',
                'data': {'message': str(e)},
            }
            return Response(response_data, status=500)


class GETAllApprovedCityBySectId(APIView):
    """ show all approved city and search 'cityName' by user."""
    def get(self, request,sectId, *args, **kwargs):
        try:
            #  for search city Name
            MstSect.objects.get(id=sectId)
            cityName = request.GET.get('cityName')
            if cityName:
                queryset = City.objects.filter(isActive=True, isVerified=True, isActiveForResidents=True, cityName__icontains=cityName.strip()).order_by('cityName')
                if len(queryset) < 1:
                    response_data = {
                        'statusCode': 200,
                        'status': 'Success',
                        'data': {"message": "No Results found !"},
                    }
                    return Response(response_data)

                serializer = GETCitySerializer(queryset, many=True)
                response_data = {
                    'statusCode': 200,
                    'status': 'Success',
                    'data': serializer.data,
                }
                return Response(response_data)

            queryset = City.objects.filter(isActive=True, isVerified=True, isActiveForResidents=True).annotate(
            count=Count('user', filter=Q(user__isActive=True, user__isVerified=True))).values('cityId', 'cityName', 'count').order_by(
                'cityName')
            if len(queryset) < 1:
                response_data = {
                    'statusCode': 200,
                    'status': 'Success',
                    'data': {"message": "No Results found !"},
                }
                return Response(response_data)

            # Customize the response data as needed
            if len(queryset) < 1:
                response_data = {
                    'statusCode': 200,
                    'status': 'Success',
                    'data': {"message": "No Record found."},
                }
                return Response(response_data)

            serializer = GETCityWithCountSerializer(queryset, many=True)
            response_data = {
                'status_code': 200,
                'status': 'Success',
                'data': serializer.data,
            }
            return Response(response_data)
        except MstSect.DoesNotExist:
            response_data = {
                'statusCode': 404,
                'status': 'failed',
                'data': {'message': "Invalid Sect Id."},
            }
            return Response(response_data, status=404)
        except ValueError:
            response_data = {
                'statusCode': 404,
                'status': 'failed',
                'data': {'message': f"'sectId' excepted a number but got '{sectId}'."},
            }
            return Response(response_data, status=404)


class GETAllApprovedAreasBySectIdAndCityId(APIView):

    def get_all_areas(self, sectId, cityId):
        queryset = Area.objects.filter(isActive=True, isVerified=True, cityId=cityId).annotate(
            count=Count('user',
                        filter=Q(user__isActive=True, user__isVerified=True, user__sectId=sectId, user__cityId=cityId)),
            memberCount=Count('user', filter=Q(user__isActive=True, user__isVerified=True, user__sectId=sectId,
                                               user__cityId=cityId)),
            familyCount=Count('user', filter=Q(user__isActive=True, user__isVerified=True, user__headId=None,
                                               user__sectId=sectId, user__cityId=cityId))
        ).order_by('areaName')
        print('queryset==> ', queryset)
        if len(queryset) < 1:
            response_data = {
                'statusCode': 200,
                'status': 'Success',
                'memberCount': User.objects.filter(sectId=sectId, cityId=cityId).count(),
                'familyCount': User.objects.filter(sectId=sectId, cityId=cityId, headId=None).count(),
                'data': {'message': 'Record Not Found'}
            }
            return Response(response_data)

        serializer = GETAreaWithCountSerializer(queryset, many=True, context={'sect_wise': True, 'sect_id': sectId})
        response_data = {
            'status_code': 200,
            'status': 'Success',
            'memberCount': User.objects.filter(sectId=sectId, cityId=cityId).count(),
            'familyCount': User.objects.filter(sectId=sectId, cityId=cityId, headId=None).count(),
            'data': serializer.data,
        }
        return Response(response_data)

    def get(self, request, sectId, cityId, *args, **kwargs):
        try:
            # City.objects.get(cityId=cityId)
            area_name = request.GET.get('areaName')
            search_resident_name = request.GET.get('residentName')

            # search areaName
            if area_name:
                queryset = Area.objects.filter(isActive=True, isVerified=True, cityId=cityId, areaName__icontains=area_name.strip())
                if len(queryset) < 1:
                    response_data = {
                        'statusCode': 200,
                        'status': 'Success',
                        'data': {'message': 'Record Not Found'}
                    }
                    return Response(response_data)
                serializer = GETAreaSerializer(queryset, many=True)
                response_data = {
                    'status_code': 200,
                    'status': 'Success',
                    'data': serializer.data,
                }
                return Response(response_data)
            # search 'residents' in a 'city'
            if search_resident_name:
                queryset = User.objects.filter(sectId=sectId, cityId=cityId, name__icontains=search_resident_name.strip())
                if len(queryset) < 1:
                    response_data = {
                        'statusCode': 200,
                        'status': 'success',
                        'data': {'message': 'No Record Found.'},
                    }
                    return Response(response_data, status=200)
                serializer = SearchResidentByCityIdSerializer(queryset, many=True)
                response_data = {
                    'statusCode': 200,
                    'status': 'success',
                    'data': serializer.data,
                }
                return Response(response_data, status=200)
            # return all the areas
            return self.get_all_areas(sectId=sectId, cityId=cityId)

        # exceptions
        except ValueError:
            check_sectId = str(sectId).isdigit()
            check_cityId = str(cityId).isdigit()
            message = None
            if not check_cityId and not check_sectId:
                message = f"'sectId' and 'cityId' excepted a number but got '{sectId}' and '{cityId}'."
            elif not check_cityId:
                message = f"'cityId' excepted a number but got '{cityId}'."
            elif not check_sectId:
                message = f"'sectId' excepted a number but got '{sectId}'."

            response_data = {
                'statusCode': 404,
                'status': 'failed',
                # 'data': {'message': f"'City Id' excepted a number but got '{cityId}'."},
                'data': {'message': message}
            }
            return Response(response_data, status=404)


class GETAllResidentsBySectIdAndAreaId(APIView):
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination

    def get_all_members(self, request, sectId, areaId):
        members_queryset = User.objects.filter(sectId=sectId, areaId=areaId).annotate(age=calculate_age_expression('dob', User)).order_by('name')
        # print('members_queryset==> ', members_queryset)
        if len(members_queryset) < 1:
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

            return Response({**{
                'statusCode': 200,
                'status': 'success',
            }, **data}, status=200)

    def get_all_head_users(self, request, sectId, areaId):
        family_queryset = User.objects.filter(sectId=sectId, areaId=areaId, headId=None). \
            annotate(age=calculate_age_expression('dob', User)).order_by('name')

        if len(family_queryset) < 1:
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
            return Response({**{
                'statusCode': 200,
                'status': 'success',
            }, **data}, status=200)

    def get(self, request, sectId, areaId, *args, **kwargs):
        try:
            resident_type = request.GET.get('residentType')
            search_resident_name = request.GET.get('residentName')
            #  for searching resident
            if search_resident_name:
                search_result = User.objects.filter(sectId=sectId, areaId=areaId, name__icontains=search_resident_name.strip()
                                                    ).annotate(age=calculate_age_expression('dob', User))
                if len(search_result) < 1:
                    response_data = {
                        'statusCode': 200,
                        'status': 'success',
                        'data': {'message': 'No Record Found.'},
                    }
                    return Response(response_data, status=200)
                serializer = SearchResidentByCityIdSerializer(search_result, many=True)
                response_data = {
                    'statusCode': 200,
                    'status': 'success',
                    'data': serializer.data,
                }
                return Response(response_data, status=200)

            #  for getting members/family records
            if resident_type is None or resident_type.strip().lower() == 'family':
                return self.get_all_head_users(request=request, sectId=sectId, areaId=areaId)

            elif resident_type.strip().lower() == 'member':
                return self.get_all_members(request=request, sectId=sectId, areaId=areaId)

            else:
                response_data = {
                    'statusCode': 400,
                    'status': 'failed',
                    'data': {'message': f"'residentType' query param value must be 'family/member'."},
                }
                return Response(response_data, status=400)

        except Area.DoesNotExist:
            response_data = {
                'statusCode': 404,
                'status': 'failed',
                'data': {'message': "Invalid Area Id."},
            }
            return Response(response_data, status=404)
        except ValueError:
            check_sectId = str(sectId).isdigit()
            check_areaId = str(areaId).isdigit()
            message = None
            if not check_areaId and not check_sectId:
                message = f"'sectId' and 'areaId' excepted a number but got '{sectId}' and '{areaId}'."
            elif not check_areaId:
                message = f"'areaId' excepted a number but got '{areaId}'."
            elif not check_sectId:
                message = f"'sectId' excepted a number but got '{sectId}'."

            response_data = {
                'statusCode': 404,
                'status': 'failed',
                # 'data': {'message': f"'Area Id' excepted a number but got '{areaId}'."},
                'data': {'message': message}
            }
            return Response(response_data, status=404)