from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .dharamSthanMembeber_serializer import *
from utils.get_id_by_token import get_user_id_from_token_view
from accounts.pagination import CustomPagination
from rest_framework.response import Response
from jdcApi.models import DharamSthanMember


class POSTNewDharamSthanMember(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        # try:
            get_user_id = get_user_id_from_token_view(request)
            serializer = CREATEDharamSthanMemberSerializer(data=request.data, context={'user_id_by_token': get_user_id})
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
        # except Exception as e:
        #     response_data = {
        #         'statusCode': 500,
        #         'status': 'error',
        #         'data': {'message': "Internal Server Error"},
        #     }
        #     return Response(response_data, status=500)


class PUTDharamSthanMemberById(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, dharamSthanMemberId, *args, **kwargs):
        try:
            get_user_id = get_user_id_from_token_view(request)
            instance = DharamSthanMember.objects.get(id=dharamSthanMemberId)
            serializer = UPDATEDharamSthanMemberByIdSerializer(instance, data=request.data, partial=True, context={'user_id_by_token': get_user_id})
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
        except DharamSthanMember.DoesNotExist:
            response_data = {
                'statusCode': 404,
                'status': 'failed',
                'data': {'message': "Invalid DharamSthanMember Id."},
            }
            return Response(response_data, status=404)
        except ValueError:
            response_data = {
                'statusCode': 404,
                'status': 'failed',
                'data': {'message': f"'DharamSthanMember id' excepted a number but got '{dharamSthanMemberId}'"},
            }
            return Response(response_data, status=404)
        # except Exception as e:
        #     response_data = {
        #         'statusCode': status.HTTP_500_INTERNAL_SERVER_ERROR,
        #         'status': 'error',
        #         'data': {'error': str(e)},
        #     }
        #     return Response(response_data, status=500)


class GETDharamSthanMemberDetailsById(APIView):

    def get(self, request, dharamSthanMemberId, *args, **kwargs):
        try:
            instance = DharamSthanMember.objects.get(id=dharamSthanMemberId)
            serializer = GETDharamSthanMemberDetialsByIdSerializer(instance)
            response_data = {
                'statusCode': 200,
                'status': 'success',
                'data': serializer.data
            }
            return Response(response_data)

        except DharamSthanMember.DoesNotExist:
            response_data = {
                'statusCode': 404,
                'status': 'failed',
                'data': {'message': "Invalid dharamSthanMember id."}
            }
            return Response(response_data, status=404)
        except ValueError:
            response_data = {
                'statusCode': 404,
                'status': 'failed',
                'data': {'message': f"excepted a number but you got '{dharamSthanMemberId}'."}
            }
            return Response(response_data, status=404)
        except Exception as e:
            response_data = {
                'statusCode': 500,
                'status': 'error',
                'data': {'message': 'Internal Server Error.'}
            }
            return Response(response_data, status=500)


class GETAllDharamSthanMembersByDharamSthanId(APIView):

    def get(self, request, dharamSthanId, *args, **kwargs):
        # try:
            queryset = DharamSthanMember.objects.filter(dharamSthanId=dharamSthanId)
            if len(queryset) < 1:
                response_data = {
                    'statusCode': 200,
                    'status': 'success',
                    'data': {"message": "No Record Found."}
                }
                return Response(response_data)
            serializer = GETDharamSthanMemberDetialsByIdSerializer(queryset, many=True)
            response_data = {
                'statusCode': 200,
                'status': 'success',
                'data': serializer.data
            }
            return Response(response_data)
        # except Exception as e:
        #     response_data = {
        #         'statusCode': 500,
        #         'status': 'error',
        #         'data': {'message': 'Internal Server Error.'}
        #     }
        #     return Response(response_data, status=500)