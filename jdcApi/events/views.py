
from rest_framework.views import APIView

from .serializer import *
from rest_framework import status
from rest_framework.response import Response
from jdcApi.models import MstSect, City, Event
from rest_framework.permissions import IsAuthenticated
from utils.get_id_by_token import get_user_id_from_token_view
from django.db.models import Q, Count
from accounts.pagination import CustomPagination


class POSTNewEvent(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        # try:
            get_user_id = get_user_id_from_token_view(request)
            serializer = CREATEEventSerializer(data=request.data, context={'user_id_by_token': get_user_id})
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


class PUTEventById(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, eventId, *args, **kwargs):
        try:
            get_user_id = get_user_id_from_token_view(request)
            instance = Event.objects.get(id=eventId)
            serializer = UPDATEEventSerializer(instance, data=request.data, partial=True, context={'user_id_by_token': get_user_id, 'event_id': eventId})
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
            return Response(response_data, status=400)
        except Event.DoesNotExist:
            response_data = {
                'statusCode': status.HTTP_404_NOT_FOUND,
                'status': 'failed',
                'data': {'message': "Invalid Event Id."},
            }
            return Response(response_data, status=404)
        except ValueError:
            response_data = {
                'statusCode': 404,
                'status': 'failed',
                'data': {'message': f"'event id' excepted a number but got '{eventId}'"},
            }
            return Response(response_data, status=404)



class GETEventDetailsById(APIView):
    # permission_classes = [IsAuthenticated]

    def get(self, request, eventId, *args, **kwargs):
        try:
            instance = Event.objects.get(id=eventId)
            print('ecent==> ', instance)
            serializer = GETEventDetailsSerializer(instance=instance)
            response_data = {
                'statusCode': 200,
                'status': 'success',
                'data': serializer.data
            }
            return Response(response_data)
        except Event.DoesNotExist:
            response_data = {
                'statusCode': 404,
                'status': 'failed',
                'data': {'message': "Invalid Event Id."},
            }
            return Response(response_data, status=404)
        except ValueError:
            response_data = {
                'statusCode': 404,
                'status': 'failed',
                'data': {'message': f"'event id' excepted a number but got '{eventId}'"},
            }
            return Response(response_data, status=404)


class GETAllSectEvent(APIView):

    def get(self, request, *args, **kwargs):
        queryset = MstSect.objects.filter(
            isActive=True
        ).annotate(count=Count('event', filter=Q(event__isVerified=True, event__isActive=True, event__endDate__gte=date.today())
        )).values('id', 'sectName', 'count').order_by('order')
        serializer = GETAllSectWithCountForEventSerializer(queryset, many=True)
        response_data = {
            'statusCode': 200,
            'status': 'success',
            'data': serializer.data
        }
        return Response(response_data)


class GETAllCityEventBySectId(APIView):
    pagination_class = CustomPagination

    def get(self, request, sectId, *args, **kwargs):
        try:
            int(sectId)
            city_name = request.GET.get('cityName')
            # if cityName is not None then search city
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
            # get all active cities from City Model
            queryset = City.objects.filter(isActive=True, isVerified=True)\
                .annotate(count=Count('event', filter=Q(event__isVerified=True, event__isActive=True, event__sectId=sectId)))\
                .values('cityId', 'cityName', 'count').order_by('cityName')
            if len(queryset) < 1:
                response_data = {
                    'statusCode': 200,
                    'status': 'Success',
                    'data': {'message': 'No Record found.'}
                }

                return Response(response_data)

            serializer = GETAllCityWithCountForEventSerializer(queryset, many=True, context={"sect_id": sectId})

            response_data = {
                'statusCode': 200,
                'status': 'Success',
                'data': serializer.data
            }
            return Response(response_data)
        except ValueError:
            response_data = {
                'statusCode': 404,
                'status': 'Failed',
                'data': {"message": f"'sectId' excepted a number but got '{sectId}'."}
            }
            return Response(response_data, status=404)



class GETAllActiveEventBySectIdAndCityId(APIView):
    pagination_class = CustomPagination

    def get(self, request, sectId, cityId, *args, **kwargs):
        try:
            status= request.GET.get('status')
            today_date = date.today()
            if status is None or status.strip().lower() == 'active':
                queryset = Event.objects.filter(sectId=sectId, cityId=cityId, isActive=True, isVerified=True, endDate__gte=today_date).order_by('title')
                print('==> ',queryset)
            elif status.strip().lower() == 'inactive':
                queryset = Event.objects.filter(sectId=sectId, cityId=cityId, isActive=True, isVerified=True,
                                        endDate__lt=today_date).order_by('title')
            else:
                response_data = {
                    'status': 400,
                    'statusCode': 'failed',
                    'data': {'message': f"'status' expected 'active' or 'inactive' value, but got '{status}'."}
                }
                return Response(response_data, status=400)

            if len(queryset) < 1:
                response_data = {
                    'status': 200,
                    'statusCode': 'Success',
                    'data': {'message': "No Record Found."}
                }
                return Response(response_data)
            # pagination
            pagination_data = {}
            paginator = self.pagination_class()
            page = paginator.paginate_queryset(queryset, request)
            if page is not None:
                serializer = GETAllActiveEvents(page, many=True)
                pagination_data = paginator.get_paginated_response(serializer.data)
            response_data = {**{
                'statusCode': 200,
                'status': 'Success'
            }, **pagination_data}
            return Response(response_data)
        except ValueError:
            message = None
            if not str(sectId).isdigit() and not str(cityId).isdigit():
                message = f"'cityId' and 'sectId' excepted a number but got '{cityId}' and '{sectId}'."
            elif not str(cityId).isdigit():
                message = f"'cityId' excepted a number but got '{cityId}'."
            elif not str(sectId).isdigit():
                message = f"'sectId' excepted a number but got '{sectId}'."

            response_data = {
                'status': 404,
                'statusCode': 'Failed',
                'data': {'message': message}
            }
            return Response(response_data, status=404)


class GETAllApprovedAndUnapprovedEventForAdmin(APIView):
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination

    def get(self, request, *args, **kwargs):
        # try:
            status = request.GET.get('status')
            if status is None or status.strip().lower() == 'active':
                queryset = Event.objects.filter(isActive=True, isVerified=True).order_by('title')
            elif status.strip().lower() == 'inactive':
                queryset = Event.objects.filter(Q(isActive=False) | Q(isVerified=False)).order_by('title')
            else:
                response_data = {
                    'status': 400,
                    'statusCode': 'failed',
                    'data': {'message': f"'status' expected 'active' or 'inactive' value, but got '{status}'."}
                }
                return Response(response_data, status=400)

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
                serializer = GETAllEventsForAdmin(page, many=True)
                pagination_data = paginator.get_paginated_response(serializer.data)
            # serializer = self.get_serializer(queryset, many=True)
            response_data = {**{
                'statusCode': 200,
                'status': 'Success'
            }, **pagination_data}

            return Response(response_data)

