
from django.conf import settings

from .models import OTP
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Q
from .auth import is_otp_expired, generate_otp, is_send_otp, check_number_exist_for_login
from .utils import is_valid_mobile_number
from rest_framework import status
# from .push_notification import send_notification_to_admin
import logging
info_logger = logging.getLogger('info')
error_logger = logging.getLogger('error')


class SendOTPWithNumber(APIView):
    def check_number_is_locked(self, phoneNumber):
        filtered_data = OTP.objects.filter(Q(phoneNumber=phoneNumber) & Q(status='locked')).order_by('-timestamp').first()
        print(filtered_data)
        if filtered_data is not None:
            obj = filtered_data
            return obj.timestamp
        else:
            return None

    def post(self, request, *args, **kwargs):
        # data = request.body
        phone_number = request.data.get('phoneNumber')
        # print('phone Number==> ', phone_number)

        # check phone_number is None or not
        if phone_number is not None:
            # check phone_number is correct or not
            if not is_valid_mobile_number(phone_number):
                json_data = {
                    'statusCode': status.HTTP_406_NOT_ACCEPTABLE,
                    'status': 'Failed',
                    'data': f'Please provide valid phoneNumber.'
                }
                return Response(json_data, status=406)
        else:
            json_data = {
                'statusCode': 400,
                'status': 'Failed',
                'data': f'Please provide phoneNumber. You have not provide any phoneNumber.'
            }
            return Response(json_data, status=400)
        # before sending check email is locked or not

        check_timestamp = self.check_number_is_locked(phone_number)
        if check_timestamp is None or is_otp_expired(check_timestamp):
            # generate otp
            otp = generate_otp()

            # send otp

            is_send = is_send_otp(phone_number=phone_number, otp=otp)
            obj = OTP.objects.create(phoneNumber=phone_number, otp=otp)
            obj.save()
            if is_send:
                json_data = {
                    'statusCode': 200,
                    'status': 'Success',
                    'data': f'OTP has sent successfully.'
                }
                return Response(json_data)
        else:
            default_otp_expiry_time = 300
            otp_expiry_time = getattr(settings, 'OTP_EXPIRY_DURATION', default_otp_expiry_time)
            json_data = {
                'statusCode': status.HTTP_400_BAD_REQUEST,
                'status': 'Failed',
                'data': f'You entered more then 3 times wrong OTP. Please try again after {otp_expiry_time // 60} minutes.'
            }
            return Response(json_data, status=400)
        json_data = {
            'statusCode': status.HTTP_500_INTERNAL_SERVER_ERROR,
            'status': 'failed',
            'data': 'Please try after some time.'
        }

        return Response(json_data, status=500)


class VerifyOTP(APIView):

    def get_active_otp_by_number(self, phone_number):
        obj = None
        filtered_data = OTP.objects.filter(Q(phoneNumber=phone_number) & Q(status='active')).order_by('-timestamp').first()
        if filtered_data is not None:
            obj = filtered_data
        return obj

    def post(self, request, *args, **kwargs):
        otp = request.data.get('otp')
        phone_number = request.data.get('phoneNumber')

        if phone_number is None:
            json_data = {
                'statusCode': 400,
                'status': 'Failed',
                'data': "Please Provide Phone Number."
            }
            return Response(json_data, status=400)

        if otp is None:
            json_data = {
                'statusCode': 400,
                'status': 'Failed',
                'data': "Please Provide OTP."
            }
            return Response(json_data, status=400)
        # find the latest OTP by mail_id form database
        instance = self.get_active_otp_by_number(phone_number=phone_number)

        # instance is None
        if instance is None:
            json_data = {
                'statusCode': status.HTTP_400_BAD_REQUEST,
                'status': 'Failed',
                'data': "Invalid OTP."
            }
            return Response(json_data, status=400)


        # check otp length
        if len(otp) != 6:
            instance.count += 1
            instance.save()
            json_data = {
                'statusCode': status.HTTP_400_BAD_REQUEST,
                'status': 'Failed',
                'data': 'You entered wrong OTP.'
            }

            return Response(json_data, status=400)
        # check OTP is expired or not
        # if expired
        if is_otp_expired(instance.timestamp):
            json_data = {
                'statusCode': status.HTTP_400_BAD_REQUEST,
                'status': 'Failed',
                'data': 'Your OTP has expired.'
            }
            info_logger.info(f'This OTP {otp} has expired.')
            return Response(json_data, status=400)
        else:
            if instance.otp == otp:
                instance.status = 'inactive'
                instance.save()
                # if otp is correct then next step

                is_number_exist, user_obj = check_number_exist_for_login(phone_number=phone_number)

                if is_number_exist:
                    if not user_obj.isActive:
                        json_data = {
                            'statusCode': status.HTTP_200_OK,
                            'status': 'Success',
                            'message': 'OTP Matched.Please activate your account.',
                            'data': {'userid': user_obj.userId}
                        }
                        info_logger.info(f'This {phone_number} is Inactive and try to login.')
                        title = "Logged In for Inactive User."
                        body = f"A User who's mobile number is '{phone_number}'has login failed in JAIN DIGITAL CONNECT. "
                        # send_notification_to_admin(title=title, body=body)
                        return Response(json_data)
                    else:
                        json_data = {
                            'statusCode': status.HTTP_200_OK,
                            'status': 'Success',
                            'message': 'Your OTP has matched successfully.',
                            'data': {'userid': user_obj.userId}
                        }
                        # for Notification
                        title = "Logged In for Active User."
                        body = f"A User who's mobile number is '{phone_number}'has successful login in JAIN DIGITAL CONNECT. "
                        # if send_notification_to_admin(title=title, body=body):
                        #     info_logger.info(f'OTP matched successfully and This {phone_number} user has logged in.')
                        # else:
                        #     error_logger.error(f'Failed to add data in "NotificationHistory" tabel.')
                        return Response(json_data)
                else:
                    json_data = {
                        'statusCode': 404,
                        'status': 'Failed',
                        'data': 'Account not found',
                    }
                    return Response(json_data, status=404)

            # if user enter more than 3 times wrong otp
            if instance.count >= 3:
                instance.status = 'locked'
                instance.save()
                default_otp_expiry_time = 300
                otp_expiry_time = getattr(settings, 'OTP_EXPIRY_DURATION', default_otp_expiry_time)
                json_data = {
                     'statusCode': status.HTTP_400_BAD_REQUEST,
                     'status': 'Failed',
                     'data': f'You entered more then 3 times wrong OTP. Please try again after {otp_expiry_time//60} minutes.'
                }
                info_logger.info(f'This {phone_number} has locked for next {otp_expiry_time//60} minutes.')
                return Response(json_data, status=400)

            instance.count += 1
            instance.save()
            json_data = {
                'statusCode': status.HTTP_400_BAD_REQUEST,
                'status': 'Failed',
                'data': 'You entered wrong OTP.'
                }

            return Response(json_data, status=400)

