from rest_framework.generics import ListAPIView
from .serializers import GETAllSectSerializer, GETAllSectWithCountSerializer
from .models import Sect
from rest_framework.response import Response


class GETAllSect(ListAPIView):
    serializer_class = GETAllSectSerializer

    def get_queryset(self):
        query_set = Sect.objects.all()
        return query_set

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        print(queryset)
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


class GETAllSectSaint(ListAPIView):
    """ Count 'Saint' by 'Sect' """
    serializer_class = GETAllSectWithCountSerializer

    def get_queryset(self):
        query_set = Sect.objects.all()
        return query_set

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        print(queryset)
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



