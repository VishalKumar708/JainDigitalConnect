from rest_framework.generics import ListAPIView

from .models import CustomUser
from rest_framework.views import APIView
from rest_framework.response import Response
from .auth import is_json, is_account_exist, check_number_exist_for_add_member, is_applicable_for_matrimonial, check_head_exist_by_id, check_same_name_member_in_a_head, before_update_check_number_exist
from .utils import is_valid_mobile_number, is_integer, string_to_bool
from rest_framework import status
from .serializers import HeadSerializer, MemberSerializer, GETFamilyByHeadIdSerializer, UpdateMemberSerializer, GETAllUserSerializer, GETMemberByIdSerializer

import logging
logger = logging.getLogger(__name__)
logger_user = logging.getLogger('user_log')

class RegisterHead(APIView):
    def post(self, request, *args, **kwargs):
        is_json_data = is_json(data=request.body)
        print('is json==>', is_json_data)

        if not is_json_data:
            json_data = {
                'statusCode': status.HTTP_406_NOT_ACCEPTABLE,
                'status': 'Failed',
                'data': 'Please provide valid JSONData.'
            }
            return Response(json_data, status=406)

        data = request.data
        head_phone_number = data.get('phoneNumber')

        # check number exist in whole tabel
        is_exist, instance = is_account_exist(phone_number=head_phone_number)
        if is_exist:
            # have to send head data
            # try:
                # Fetch user data based on the user ID
                # obj = CustomUser.objects.get(userId=instance)
                # if obj.headId is not None:
                    json_data = {
                        'statusCode': 400,
                        'status': 'Failed',
                        'data': 'Head is already exist.'
                    }
                    logger_user.info('Head is already found.')
                    return Response(json_data)
                # Serialize the retrieved data
                # serializer = GETHeadSerializer(instance=obj, context={'phoneNumberVisibility': obj.phoneNumberVisibility})
                # json_data = {
                #     'statusCode': 200,
                #     'status': 'Success',
                #     'data': serializer.data
                # }
                # return Response(json_data)
            # except CustomUser.DoesNotExist:
            #     json_data = {
            #         'statusCode': 404,
            #         'status': 'Failed',
            #         'data': 'User id not found.'
            #     }
            #     return Response(json_data)

        print('head_phone_number====> ', head_phone_number)
        # check head phone number
        if head_phone_number is None:
            json_data = {
                'statusCode': 400,
                'status': 'Failed',
                'data': 'Please Provide head phoneNumber'
            }
            return Response(json_data)
        else:
            if not is_valid_mobile_number(head_phone_number):
                json_data = {
                    'statusCode': 400,
                    'status': 'Failed',
                    'data': 'Please Provide a valid phone number.'
                }
                return Response(json_data)

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
                    return Response(json_data)

            # save record
            serializer.save()
            json_data = {
                'statusCode': 200,
                'status': 'Success',
                'data': 'Head Created Successfully.'
            }
            logger_user.info('Head Added Successfully.')
            return Response(json_data, status=406)

        # serializer error
        json_data = {
            'statusCode': 400,
            'status': 'failed',
            'data': serializer.errors
        }

        return Response(json_data, status=406)


class RegisterMember(APIView):
    def post(self, request, *args, **kwargs):
        is_json_data = is_json(data=request.body)
        print('is json==>', is_json_data)

        if not is_json_data:
            json_data = {
                'statusCode': status.HTTP_406_NOT_ACCEPTABLE,
                'status': 'Failed',
                'data': 'Please provide valid JSONData.'
            }
            return Response(json_data, status=406)

        data = request.data
        member_phone_number = data.get('phoneNumber')
        # check mobile number
        if member_phone_number != '0000000000':
            is_exist = check_number_exist_for_add_member(phone_number=member_phone_number)
            if is_exist:
                json_data = {
                    'statusCode': 200,
                    'status': 'Success',
                    'data': 'This member has already exist.'
                }
                logger_user.info(f'This {member_phone_number} Member is already exist.')
                return Response(json_data)

            # check head id is valid or not
        if not check_head_exist_by_id(id=data.get('headId')):
            json_data = {
                'statusCode': 404,
                'status': 'Failed',
                'data': 'Head id not found or you entered wrong head id'
            }
            logger_user.info(f'This {member_phone_number} user entered wrong headId.')
            return Response(json_data)

        member_name = data.get('name')
        if member_phone_number == '0000000000' and member_name is not None:
            is_member_exist = check_same_name_member_in_a_head(head_id=data.get('headId'), member_name=member_name)
            if is_member_exist:
                json_data = {
                    'statusCode': 400,
                    'status': 'Failed',
                    'data': 'This member is already added. Please add different member.'
                }
                logger_user.info(f'headId = {data.get("headId")} user try to add same member more than 1 time. ')
                return Response(json_data)


        print('member_phone_number====> ', member_phone_number)
        # check member enter mobile no. or not
        if member_phone_number is None:
            json_data = {
                'statusCode': 400,
                'status': 'Failed',
                'data': 'Please Provide member phone number.'
            }
            return Response(json_data)
        else:
            if not is_valid_mobile_number(member_phone_number):
                json_data = {
                    'statusCode': 400,
                    'status': 'Failed',
                    'data': 'Please Provide a valid phone number.'
                }
                return Response(json_data)

        # Put all data in serializer
        serializer = MemberSerializer(data=data)
        if serializer.is_valid():
            for_match = data.get('lookingForMatch')

            is_looking_for_match = False if for_match is None else string_to_bool(for_match)

            if is_looking_for_match:
                is_applicable, message = is_applicable_for_matrimonial(data.get('dob'), data.get('gender'))
                if not is_applicable:
                    json_data = {
                        'statusCode': 400,
                        'status': 'Failed',
                        'data': message
                    }
                    return Response(json_data)

            serializer.save()
            json_data = {
                'statusCode': 200,
                'status': 'Success',
                'data': 'Member Added Successfully.'
            }
            logger_user.info(f'headId = {data.get("headId")} user member added successfully.')

            return Response(json_data, status=406)

        json_data = {
            'statusCode': 400,
            'status': 'failed',
            'data': serializer.errors
        }
        return Response(json_data, status=406)


class GETFamilyByHeadId(APIView):

    def get(self, request, head_id,  *args, **kwargs):

        is_valid_id = is_integer(head_id)
        if not is_valid_id:
            json_data = {
                'statusCode': 400,
                'status': 'failed',
                'data': 'Your entered wrong id. Id can only be integer.'
            }
            return Response(json_data, status=406)

        is_valid_head_id = check_head_exist_by_id(head_id)
        if not is_valid_head_id:
            json_data = {
                'statusCode': 404,
                'status': 'failed',
                'data': 'Your entered wrong head id.'
            }
            logger_user.info(f'User entered wrong headId = {head_id}.')

            return Response(json_data)

        filtered_obj = CustomUser.objects.filter(headId=head_id)
        if len(filtered_obj) > 0:
            serializer = GETFamilyByHeadIdSerializer(filtered_obj, many=True)
            json_data = {
                'statusCode': 200,
                'status': 'Success',
                'data': serializer.data
            }
            logger_user.info(f'Send all family members data to headId = {head_id} user successfully.')

            return Response(json_data)
        else:
            json_data = {
                'statusCode': 404,
                'status': 'failed',
                'data': 'No member found.'
            }
            logger_user.info(f'headId = {head_id} user has No member found.')

            return Response(json_data)


#  check Member exist or not by Mobile Number
class IsUserExist(APIView):
    def post(self, request, *args, **kwargs):
        phone_number = request.data.get('phoneNumber')
        # data = request.data
        # phone_number = data.get('phoneNumber')
        if phone_number is None:
            json_data = {
                'statusCode': 400,
                'status': 'Failed',
                'data': {'message': 'Please provide phone Number.'}
            }
            return Response(json_data)
        else:
            if not is_valid_mobile_number(phone_number):
                json_data = {
                    'statusCode': 400,
                    'status': 'Failed',
                    'data': {'message':'Please Provide a valid phone number.'}
                }
                return Response(json_data)

        is_available = check_number_exist_for_add_member(phone_number)
        print("number exist or not==> ", is_available)
        if is_available:
            json_data = {
                'statusCode': 200,
                'status': 'Success',
                'data': {'message': 'Number already exist'}
            }
            logger_user.info(f'This number {phone_number} is already exist.')

            return Response(json_data)

        json_data = {
            'statusCode': 404,
            'status': 'Failed',
            'data': {'message': 'user not found.'}
        }
        logger_user.info(f'This number {phone_number} user not found in database.')

        return Response(json_data)


class DeleteMember(APIView):

    def delete(self, request, member_id):
        if not is_integer(member_id):
            json_data = {
                'statusCode': 404,
                'status': 'Failed',
                'data': 'member_id must be only integer.'
            }
            logger_user.info(f'Wrong user id entered to delete user.')

            return Response(json_data)

        try:
            # make user inactive
            member = CustomUser.objects.get(userId=member_id)
            member.isActive = False
            member.save()

            json_data = {
                'statusCode': 200,
                'status': 'Success',
                'data': 'Member deleted successfully.'
            }
            logger_user.info(f'user_id = {member_id} deleted(inactive) successfully.')

            return Response(json_data)
        except CustomUser.DoesNotExist:
            json_data = {
                'statusCode': 404,
                'status': 'Failed',
                'data': 'id not found. Please input valid id.'
            }
            logger_user.info(f"user_id = {member_id} doesn't exist.")

            return Response(json_data)

        #
        # member.delete()
        # json_data = {
        #     'statusCode': 200,
        #     'status': 'Success',
        #     'data': 'Member deleted successfully.'
        # }
        # return Response(json_data)


class UpdateUserById(APIView):

    def put(self, request, member_id,  *args, **kwargs):
        if not is_integer(member_id):
            json_data = {
                'statusCode': 404,
                'status': 'Failed',
                'data': 'user_id must be only integer.'
            }
            return Response(json_data)

        try:
            member = CustomUser.objects.get(userId=member_id)
            if len(request.data) < 1:
                serializer = UpdateMemberSerializer(member, data=request.data)
                if not serializer.is_valid():
                    json_data = {
                        'statusCode': 400,
                        'status': 'Failed',
                        'data': serializer.errors
                    }
                    return Response(json_data)
            # print("check number===>", request.data.get('phoneNumber'))
            # print("check number type ===>", type(request.data.get('phoneNumber')))
            if request.data.get('phoneNumber') is not None:
                exist = before_update_check_number_exist(request.data.get('phoneNumber'), user_id=member_id)
                print('exist==>', exist)
                if exist:
                    json_data = {
                        'statusCode': 400,
                        'status': 'Failed',
                        'data': "This number is already exist.Number must be unique."
                    }
                    return Response(json_data)

            serializer = UpdateMemberSerializer(member, data=request.data, partial=True)

            if serializer.is_valid():
                # Save the updated member
                serializer.save()

                json_data = {
                    'statusCode': status.HTTP_200_OK,
                    'status': 'Success',
                    'data': 'Member updated successfully.'
                }
                logger_user.info(f'user_id = {member_id} record updated successfully.')
                return Response(json_data, status=status.HTTP_200_OK)
            else:
                json_data = {
                    'statusCode': status.HTTP_400_BAD_REQUEST,
                    'status': 'Failed',
                    'data': serializer.errors
                }
                return Response(json_data, status=status.HTTP_400_BAD_REQUEST)

        except CustomUser.DoesNotExist:
            json_data = {
                'statusCode': 404,
                'status': 'Failed',
                'data': 'id not found. Please input valid id.'
            }
            logger_user.info(f'User Entered wrong user_id = {member_id} to update record.')

            return Response(json_data)


class GetAllResidents(ListAPIView):
    serializer_class = GETAllUserSerializer
    queryset = CustomUser.objects.all()

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        if len(queryset) < 1:
            response_data = {
                'statusCode': 404,
                'status': 'failed',
                'data': {'msg': 'User Not found.'},
            }
            logger_user.info('All user data retrieve failed because User not found. ')
            return Response(response_data)
        serializer = self.get_serializer(queryset, many=True)

        response_data = {
            'statusCode': 200,
            'status': 'success',
            'totalResidents':len(serializer.data),
            'data': serializer.data,
        }
        logger_user.info('All user data retrieve successfully.')

        return Response(response_data)


class GETUserById(APIView):
    def get(self,request, user_id, *args, **kwargs):

        if not is_integer(user_id):
            json_data = {
                'statusCode': 404,
                'status': 'Failed',
                'data': 'member_id must be only integer.'
            }
            return Response(json_data)

        try:
            # Attempt to retrieve the product by its primary key (pk)
            user = CustomUser.objects.get(userId=user_id)
            serializer = GETMemberByIdSerializer(user)
            json_data = {
                'statusCode': 200,
                'status': 'Success',
                'data': serializer.data
            }
            logger_user.info(f'user_id = {user_id} data retrieve successfully.')

            return Response(json_data)

        except CustomUser.DoesNotExist:
            json_data = {
                'statusCode': 404,
                'status': 'Failed',
                'data': 'id not found. Please input valid id.'
            }
            logger_user.info(f'user_id = {user_id} failed to retrieve data.')

            return Response(json_data)
