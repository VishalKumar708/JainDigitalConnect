from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import ListAPIView

from .models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from .auth import is_json, is_account_exist, check_number_exist_for_add_member, is_applicable_for_matrimonial, check_head_exist_by_id, check_same_name_member_in_a_head, before_update_check_number_exist
from .utils import is_valid_mobile_number, is_integer, string_to_bool
from rest_framework import status
from .serializers import HeadSerializer, MemberSerializer, GETFamilyByHeadIdSerializer, UpdateMemberSerializer, GETAllUserSerializer, GETUserDetailsByIdSerializer

from .push_notification import send_notification
from rest_framework.permissions import IsAuthenticated, AllowAny
from .auth import get_user_id_from_token_view
import logging
error_logger = logging.getLogger('error')
info_logger = logging.getLogger('info')


class RegisterHead(APIView):
    def post(self, request, *args, **kwargs):
        data = request.data
        head_phone_number = data.get('phoneNumber')

        # get head id from "access token" payload
        get_user_id = get_user_id_from_token_view(request)
        if get_user_id:
            # user_id_by_token = get_user_id
            serializer = HeadSerializer(data=data, context={'user_id_by_token': get_user_id})
        else:
            serializer = HeadSerializer(data=data)

        if serializer.is_valid():
            # save record
            obj = serializer.save()
            json_data = {
                'statusCode': 200,
                'status': 'Success',
                'data': {'headId': obj.id, 'message': 'Head Created Successfully.'}
            }

            # send notification to head
            title = 'New head has registered.'
            body = f'Head phone number is {head_phone_number}'
            send_notification(title=title, body=body)
            info_logger.info('Head Added Successfully.')
            return Response(json_data)

        # serializer error
        json_data = {
            'statusCode': 400,
            'status': 'failed',
            'data': serializer.errors
        }

        return Response(json_data, status=400)


class RegisterMember(APIView):

    def post(self, request, *args, **kwargs):
        data = request.data
        member_phone_number = data.get('phoneNumber')

        # get head id from "access token" payload
        get_user_id = get_user_id_from_token_view(request)
        if get_user_id:
            # user_id_by_token = get_user_id
            serializer = MemberSerializer(data=data, context={'user_id_by_token': get_user_id})
        else:
            serializer = MemberSerializer(data=data)

        # Put all data in serializer
        if serializer.is_valid():

            serializer.save()
            json_data = {
                'statusCode': 200,
                'status': 'Success',
                'data': {'message': 'Member Added Successfully.'}
            }
            # send notification to head
            title = 'New Member has registered.'
            body = f'A new member registered Phone Number is {member_phone_number}. Head id is {data.get("headId")} '
            send_notification(title=title, body=body)
            info_logger.info(f'headId = {data.get("headId")} user member added successfully.')

            return Response(json_data)

        json_data = {
            'statusCode': 400,
            'status': 'failed',
            'data': serializer.errors
        }
        return Response(json_data, status=400)


class GETFamilyByHeadId(APIView):
    permission_classes = [IsAuthenticated]
    # authentication_classes = []

    def get(self, request, head_id,  *args, **kwargs):
        try:
            int(head_id)
            User.objects.get(id=head_id, headId=None)
            filtered_obj = User.objects.filter(headId=head_id)
            if len(filtered_obj) == 0:
                json_data = {
                    'statusCode': 200,
                    'status': 'failed',
                    'data': {'message': 'No member found.'}
                }
                info_logger.info(f'headId = {head_id} user has No member found.')
                return Response(json_data)

            serializer = GETFamilyByHeadIdSerializer(filtered_obj, many=True)
            json_data = {
                'statusCode': 200,
                'status': 'Success',
                'data': serializer.data
            }
            info_logger.info(f'Send all family members data to headId = {head_id} user successfully.')
            return Response(json_data)
        except User.DoesNotExist:
            json_data = {
                'statusCode': 404,
                'status': 'failed',
                'data': {'message': 'Invalid Head Id.'}
            }
            error_logger.error(f'Head not found or Invalid headId.')
            return Response(json_data, status=404)
        except ValueError:
            json_data = {
                'statusCode': 404,
                'status': 'failed',
                'data': {'message': f"'HeadId' excepted a number but got '{head_id}' "}
            }
            error_logger.error(f"'headId' excepted a number but got '{head_id}'.")
            return Response(json_data, status=404)


#  check Member exist or not by Mobile Number
from .serializers import GETHeadSerializer
from rest_framework.permissions import AllowAny


class IsNumberExist(APIView):
    authentication_classes = []

    def post(self, request, *args, **kwargs):
        phone_number = request.data.get('phoneNumber')
        if phone_number is None:
            json_data = {
                'statusCode': 400,
                'status': 'Failed',
                'data': {'phoneNumber': ['PhoneNumber is required.']}
            }
            return Response(json_data, status=400)
        else:

            if not str(phone_number).isdigit() or len(phone_number.strip()) != 10:
                json_data = {
                    'statusCode': 400,
                    'status': 'Failed',
                    'data': {'phoneNumber': ['Please Provide a valid phone number.']}
                }
                return Response(json_data, status=400)

        try:
            obj = User.objects.get(phoneNumber=phone_number)
            if obj.headId is None:
                serializer = GETHeadSerializer(obj)
                json_data = {
                    'statusCode': 200,
                    'isHead': True,
                    'status': 'Success',
                    'data': serializer.data
                }
                info_logger.info(f'This number {phone_number} is already exist.')
                return Response(json_data, status=200)
            else:
                json_data = {
                    'statusCode': 200,
                    'status': 'Success',
                    'data': {'phoneNumber': ["This number is already exist"]}
                }
                info_logger.info(f'This number {phone_number} is already exist.')
                return Response(json_data, status=200)
        except User.DoesNotExist:
            json_data = {
                'statusCode': 404,
                'status': 'Failed',
                'data': {'message': 'user not found.'}
            }
            info_logger.info(f'This number {phone_number} user not found in database.')

            return Response(json_data, status=404)


class DeleteMemberById(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, user_id):
        try:
            # make user inactive
            member = User.objects.get(id=user_id)
            if not member.isActive:
                json_data = {
                    'statusCode': 400,
                    'status': 'Failed',
                    'data': {'message': 'This User is already deleted.'}
                }
                return Response(json_data, status=400)
            member.isActive = False
            get_user_id = get_user_id_from_token_view(request)
            member.updatedBy = get_user_id if get_user_id else member.id
            member.save()

            json_data = {
                'statusCode': 200,
                'status': 'Success',
                'data': {'message': 'User deleted successfully.'}
            }
            info_logger.info(f'user_id = {user_id} deleted(inactive) successfully.')

            return Response(json_data)
        except User.DoesNotExist:
            json_data = {
                'statusCode': 404,
                'status': 'Failed',
                'data': {'message': 'Invalid User Id.'}
            }
            error_logger.error(f"user_id = {user_id} doesn't exist.")

            return Response(json_data, status=404)
        except ValueError:
            json_data = {
                'statusCode': 404,
                'status': 'Failed',
                'data': {'message': f"'user_id' excepted a number but got '{user_id}'."}
            }
            info_logger.info(f'Wrong user id entered to delete user.')

            return Response(json_data, status=404)


class UpdateUserById(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, user_id,  *args, **kwargs):
        try:
            int(user_id)
            member = User.objects.get(id=user_id)
            # check 'isAdmin' field is available in data or not
            is_admin = None if request.data.get('isAdmin') is None else request.data.get('isAdmin')
            error = None
            admin = None

            if is_admin:
                if type(is_admin) != bool and type(is_admin) != str:
                    error = 'This field required only boolean values.'
                elif type(is_admin) == str:
                    check_value = is_admin.strip().lower()
                    if check_value != 'true' and check_value != 'false':
                        error = 'This field required only boolean values.'
                    elif check_value == 'true':
                        admin = True
                    elif check_value == 'false':
                        admin = False

            print('isAdmin==> ', request.data.get('isAdmin'))
            print("is_admin value in view==> ", is_admin)
            print(error)
            # get head id from "access token" payload
            get_user_id = get_user_id_from_token_view(request)
            if get_user_id:
                serializer = UpdateMemberSerializer(member, data=request.data, partial=True, context={'user_id_by_token': get_user_id, 'user_id': user_id, 'is_admin_error_message': error, 'admin': admin})
            else:
                serializer = UpdateMemberSerializer(member, data=request.data, partial=True, context={'is_admin_error_message': error, 'admin': admin})

            if serializer.is_valid():
                # Save the updated member
                serializer.save()

                json_data = {
                    'statusCode': status.HTTP_200_OK,
                    'status': 'Success',
                    'data': {'message': 'Record updated successfully.'}
                }
                info_logger.info(f'user_id = {user_id} record updated successfully.')
                return Response(json_data, status=status.HTTP_200_OK)

            json_data = {
                'statusCode': status.HTTP_400_BAD_REQUEST,
                'status': 'Failed',
                'data': serializer.errors
            }
            return Response(json_data, status=status.HTTP_400_BAD_REQUEST)

        except User.DoesNotExist:
            json_data = {
                'statusCode': 404,
                'status': 'Failed',
                'data': {'message': 'Invalid User Id.'}
            }
            error_logger.error(f'User Entered wrong user_id = {user_id} to update record.')
            return Response(json_data, status=400)
        except ValueError:
            json_data = {
                'statusCode': 400,
                'status': 'Failed',
                'data': {'message': f"'user id' excepted a number but got '{user_id}'."}
            }
            return Response(json_data, status=400)


from .pagination import CustomPagination


# from .custom_filter import
class GetAllResidents(ListAPIView):
    serializer_class = GETAllUserSerializer
    pagination_class = CustomPagination
    permission_classes = [IsAuthenticated]
    # queryset = User.objects.all()

    def get_queryset(self):
        qs = User.objects.all().order_by('name')
        return qs

    def list(self, request, *args, **kwargs):
        try:
            queryset = self.get_queryset()
            if len(queryset) == 0:
                response_data = {
                    'statusCode': 404,
                    'status': 'failed',
                    'data': {'msg': 'Record Not found.'},
                }
                info_logger.info('All user data retrieve failed because User not found. ')
                return Response(response_data)

            # Apply pagination
            # page_size = self.get_page_size(request)
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)

            # if pagination is disabled
            serializer = self.get_serializer(queryset, many=True)

            json_data = {
                'statusCode': 200,
                'status': 'success',
                'totalResidents': len(serializer.data),
                'results': serializer.data
            }
            info_logger.info('All user data retrieve successfully.')
            return Response(json_data)
        except Exception as e:
            error_logger.error('An exception occurred in "GetAllResidents" class. %s', str(e))
            json_data = {
                'statusCode': 500,
                'status': 'failed',
                'data': {'message': "Internal Server Error."}
            }
            return Response(json_data, status=500)


class GETUserDetailsById(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, user_id, *args, **kwargs):

        try:
            # Attempt to retrieve the product by its primary key (pk)
            int(user_id)
            user = User.objects.get(id=user_id)
            get_user_id = get_user_id_from_token_view(request)
            print('user id by token ==> ', get_user_id)
            if get_user_id:
                token_user_object = User.objects.get(id=get_user_id)
                # if admin user get details of any individual user then he will get an option 'admin Rights'
                if token_user_object.isAdmin:
                    serializer = GETUserDetailsByIdSerializer(user, context={'show_admin_right': True})
                else:
                    serializer = GETUserDetailsByIdSerializer(user)
            else:
                # if value get of a user who is admin then one more field will be added 'isAdmin'
                serializer = GETUserDetailsByIdSerializer(user, context={'admin': user.isAdmin})

            print("user_id get from token==> ", get_user_id)
            json_data = {
                'statusCode': 200,
                'status': 'Success',
                'data': serializer.data
            }
            info_logger.info(f'user_id = {user_id} data retrieve successfully.')

            return Response(json_data)

        except User.DoesNotExist:
            json_data = {
                'statusCode': 404,
                'status': 'Failed',
                'data': 'Invalid User Id.'
            }
            error_logger.error(f'user_id = {user_id} failed to retrieve data.')

            return Response(json_data, status=404)
        except ValueError:
            json_data = {
                'statusCode': 400,
                'status': 'Failed',
                'data': f"'user id' excepted a number but got '{user_id}'."
            }
            return Response(json_data, status=400)


