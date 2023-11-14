from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import ListAPIView

from .models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from .auth import is_json, is_account_exist, check_number_exist_for_add_member, is_applicable_for_matrimonial, check_head_exist_by_id, check_same_name_member_in_a_head, before_update_check_number_exist
from .utils import is_valid_mobile_number, is_integer, string_to_bool
from rest_framework import status
from .serializers import HeadSerializer, MemberSerializer, GETFamilyByHeadIdSerializer, UpdateMemberSerializer, GETAllUserSerializer, GETMemberByIdSerializer

from .push_notification import send_notification
from rest_framework.permissions import IsAuthenticated, AllowAny
from .auth import get_user_id_from_token_view
import logging
# logger = logging.getLogger(__name__)
error_logger = logging.getLogger('error')
info_logger = logging.getLogger('info')


class RegisterHead(APIView):
    def post(self, request, *args, **kwargs):
        data = request.data
        head_phone_number = data.get('phoneNumber')

        # check number exist in whole tabel
        is_exist, instance = is_account_exist(phone_number=head_phone_number)
        if is_exist:
            json_data = {
                'statusCode': 400,
                'status': 'Failed',
                'data': {'message': 'This number is already exist.'}
            }
            info_logger.info('Head is already found.')
            return Response(json_data, status=400)

        print('head_phone_number====> ', head_phone_number)
        # check head phone number
        if head_phone_number is None:
            json_data = {
                'statusCode': 400,
                'status': 'Failed',
                'data': 'Please Provide head phoneNumber'
            }
            return Response(json_data, status=400)
        else:
            if not is_valid_mobile_number(head_phone_number):
                json_data = {
                    'statusCode': 400,
                    'status': 'Failed',
                    'data': 'Please Provide a valid phone number.'
                }
                return Response(json_data, status=400)

        # get head id from "access token" payload
        get_user_id = get_user_id_from_token_view(request)
        if get_user_id:
            # user_id_by_token = get_user_id
            serializer = HeadSerializer(data=data, context={'user_id_by_token': get_user_id})
        else:
            serializer = HeadSerializer(data=data)

        if serializer.is_valid():
            for_match = data.get('lookingForMatch')
            is_looking_for_match = False if for_match is None else string_to_bool(for_match)
            # is_looking_for_match = string_to_bool(data.get('lookingForMatch'))

            if is_looking_for_match:
                is_applicable, message = is_applicable_for_matrimonial(data.get('dob'), data.get('gender'))
                if not is_applicable:
                    json_data = {
                        'statusCode': 400,
                        'status': 'Failed',
                        'data': message
                    }
                    return Response(json_data, status=400)

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

        return Response(json_data, status=404)


class RegisterMember(APIView):

    def post(self, request, *args, **kwargs):
        data = request.data
        member_phone_number = data.get('phoneNumber')
        # check mobile number
        if member_phone_number != '0000000000':
            is_exist = check_number_exist_for_add_member(phone_number=member_phone_number)
            if is_exist:
                json_data = {
                    'statusCode': 400,
                    'status': 'failed',
                    'data': {'msg': 'This member has already exist.'}
                }
                info_logger.info(f'This {member_phone_number} Member is already exist.')
                return Response(json_data, status=400)

            # check head id is valid or not
        if not check_head_exist_by_id(id=data.get('headId')):
            json_data = {
                'statusCode': 404,
                'status': 'Failed',
                'data': {'msg': 'Head id not found or you entered wrong head id'}
            }
            info_logger.info(f'This {member_phone_number} user entered wrong headId.')
            return Response(json_data, status=404)

        member_name = data.get('name')
        if member_phone_number == '0000000000' and member_name is not None:
            is_member_exist = check_same_name_member_in_a_head(head_id=data.get('headId'), member_name=member_name)
            if is_member_exist:
                json_data = {
                    'statusCode': 400,
                    'status': 'Failed',
                    'data': {'msg': 'This member is already added. Please add different member.'}
                }
                info_logger.info(f'headId = {data.get("headId")} user try to add same member more than 1 time. ')
                return Response(json_data, status=400)

        # print('member_phone_number====> ', member_phone_number)
        # check member enter mobile no. or not
        if member_phone_number is None:
            json_data = {
                'statusCode': 400,
                'status': 'Failed',
                'data': {'msg': 'Please Provide member phone number.'}
            }
            return Response(json_data, status=400)
        else:
            if not is_valid_mobile_number(member_phone_number):
                json_data = {
                    'statusCode': 400,
                    'status': 'Failed',
                    'data': {'msg': 'Please Provide a valid phone number.'}
                }
                return Response(json_data, status=400)

                # get head id from "access token" payload
        get_user_id = get_user_id_from_token_view(request)
        if get_user_id:
            # user_id_by_token = get_user_id
            serializer = MemberSerializer(data=data, context={'user_id_by_token': get_user_id})
        else:
            serializer = MemberSerializer(data=data)

        # Put all data in serializer
        if serializer.is_valid():
            for_match = data.get('lookingForMatch')

            is_looking_for_match = False if for_match is None else string_to_bool(for_match)

            if is_looking_for_match:
                is_applicable, message = is_applicable_for_matrimonial(data.get('dob'), data.get('gender'))
                if not is_applicable:
                    json_data = {
                        'statusCode': 400,
                        'status': 'Failed',
                        'data': {'msg': message}
                    }
                    return Response(json_data, status=400)

            serializer.save()
            json_data = {
                'statusCode': 200,
                'status': 'Success',
                'data': {'msg': 'Member Added Successfully.'}
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
        is_valid_id = is_integer(head_id)
        if not is_valid_id:
            json_data = {
                'statusCode': 400,
                'status': 'failed',
                'data': 'Your entered wrong id. Id can only be integer.'
            }
            return Response(json_data, status=400)

        is_valid_head_id = check_head_exist_by_id(head_id)
        if not is_valid_head_id:
            json_data = {
                'statusCode': 404,
                'status': 'failed',
                'data': 'Your entered wrong head id.'
            }
            info_logger.info(f'User entered wrong headId = {head_id}.')

            return Response(json_data, status=404)

        filtered_obj = User.objects.filter(headId=head_id)
        if len(filtered_obj) > 0:
            serializer = GETFamilyByHeadIdSerializer(filtered_obj, many=True)
            json_data = {
                'statusCode': 200,
                'status': 'Success',
                'data': serializer.data
            }
            info_logger.info(f'Send all family members data to headId = {head_id} user successfully.')

            return Response(json_data)
        else:
            json_data = {
                'statusCode': 404,
                'status': 'failed',
                'data': {'message': 'No member found.'}
            }
            info_logger.info(f'headId = {head_id} user has No member found.')

            return Response(json_data, status=404)


#  check Member exist or not by Mobile Number
from .serializers import GETHeadSerializer
class IsUserExist(APIView):
    def post(self, request, *args, **kwargs):
        phone_number = request.data.get('phoneNumber')
        if phone_number is None:
            json_data = {
                'statusCode': 400,
                'status': 'Failed',
                'data': {'message': 'Please provide phone Number.'}
            }
            return Response(json_data, status=400)
        else:
            if not is_valid_mobile_number(phone_number):
                json_data = {
                    'statusCode': 400,
                    'status': 'Failed',
                    'data': {'message': 'Please Provide a valid phone number.'}
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
                    'data': {'msg': "This number is already exist"}
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


class DeleteMember(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, member_id):
        if not is_integer(member_id):
            json_data = {
                'statusCode': 404,
                'status': 'Failed',
                'data': 'member_id must be only integer.'
            }
            info_logger.info(f'Wrong user id entered to delete user.')

            return Response(json_data, status=404)

        try:

            # print('User id to delete==>', member_id)
            # make user inactive
            member = User.objects.get(id=member_id)
            if not member.isActive:
                json_data = {
                    'statusCode': 400,
                    'status': 'Failed',
                    'data': {'msg': 'This member is already deleted.'}
                }
                return Response(json_data, status=400)
            member.isActive = False
            get_user_id = get_user_id_from_token_view(request)

            member.updatedBy = get_user_id if get_user_id else member.id
            member.save()

            json_data = {
                'statusCode': 200,
                'status': 'Success',
                'data': {'msg': 'Member deleted successfully.'}
            }
            info_logger.info(f'user_id = {member_id} deleted(inactive) successfully.')

            return Response(json_data)
        except User.DoesNotExist:
            json_data = {
                'statusCode': 404,
                'status': 'Failed',
                'data': {'msg': 'id not found. Please input valid id.'}
            }
            error_logger.error(f"user_id = {member_id} doesn't exist.")

            return Response(json_data, status=404)


class UpdateUserById(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, member_id,  *args, **kwargs):
        if not is_integer(member_id):
            json_data = {
                'statusCode': 404,
                'status': 'Failed',
                'data': 'user_id must be only integer.'
            }
            return Response(json_data, status=404)

        try:
            member = User.objects.get(id=member_id)
            if len(request.data) < 1:

                serializer = UpdateMemberSerializer(member, data=request.data)
                if not serializer.is_valid():
                    json_data = {
                        'statusCode': 400,
                        'status': 'Failed',
                        'data': serializer.errors
                    }
                    return Response(json_data, status=400)
            # print("check number===>", request.data.get('phoneNumber'))
            # print("check number type ===>", type(request.data.get('phoneNumber')))
            if request.data.get('phoneNumber') is not None:
                exist = before_update_check_number_exist(request.data.get('phoneNumber'), user_id=member_id)
                # print('exist==>', exist)
                if exist:
                    json_data = {
                        'statusCode': 400,
                        'status': 'Failed',
                        'data': "This number is already exist.Number must be unique."
                    }
                    return Response(json_data, status=404)
                    # get head id from "access token" payload
            get_user_id = get_user_id_from_token_view(request)
            if get_user_id:
                # user_id_by_token = get_user_id
                serializer = UpdateMemberSerializer(member, data=request.data,partial=True, context={'user_id_by_token': get_user_id})
            else:
                serializer = UpdateMemberSerializer(member, data=request.data, partial=True)

            # serializer = UpdateMemberSerializer(member, data=request.data, partial=True)

            if serializer.is_valid():
                # Save the updated member
                serializer.save()

                json_data = {
                    'statusCode': status.HTTP_200_OK,
                    'status': 'Success',
                    'data': 'Member updated successfully.'
                }
                info_logger.info(f'user_id = {member_id} record updated successfully.')
                return Response(json_data, status=status.HTTP_200_OK)
            else:
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
                'data': 'id not found. Please input valid id.'
            }
            error_logger.error(f'User Entered wrong user_id = {member_id} to update record.')

            return Response(json_data, status=400)



from .pagination import CustomPagination


# from .custom_filter import
class GetAllResidents(ListAPIView):
    serializer_class = GETAllUserSerializer
    pagination_class = CustomPagination
    permission_classes = [IsAuthenticated]
    # queryset = User.objects.all()

    def get_queryset(self):
        qs = User.objects.all()
        return qs

    def list(self, request, *args, **kwargs):
        try:
            queryset = self.get_queryset()
            if len(queryset) < 1:
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
                'data': {'msg': str(e)}
            }
            return Response(json_data, status=500)


class GETUserById(APIView):
    permission_classes = [IsAuthenticated]

    def get(self,request, user_id, *args, **kwargs):

        if not is_integer(user_id):
            json_data = {
                'statusCode': 404,
                'status': 'Failed',
                'data': 'member_id must be only integer.'
            }
            return Response(json_data, status=404)

        try:
            # Attempt to retrieve the product by its primary key (pk)
            user = User.objects.get(id=user_id)
            serializer = GETMemberByIdSerializer(user)
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
                'data': 'id not found. Please input valid id.'
            }
            error_logger.error(f'user_id = {user_id} failed to retrieve data.')

            return Response(json_data, status=404)


