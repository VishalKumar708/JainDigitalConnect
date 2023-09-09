from django.conf import settings

from .models import OTP, CustomUser
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Q
from .utils import is_json, is_otp_expired, generate_otp, is_valid_mobile_number, is_send_otp
from rest_framework import status
from .serializers import HeadSerializer


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
        data = request.body
        json_data = is_json(data=data)

        if not json_data:
            json_data = {
                'status_code': status.HTTP_406_NOT_ACCEPTABLE,
                'status': 'Failed',
                'message': 'Please provide valid JSONData.'
            }
            return Response(json_data, status=406)

        phone_number = request.data.get('phoneNumber')

        # check phone_number is None or not
        if phone_number is not None:
            # check phone_number is correct or not
            if not is_valid_mobile_number(phone_number):
                json_data = {
                    'status_code': status.HTTP_406_NOT_ACCEPTABLE,
                    'status': 'Failed',
                    'message': f'Please provide valid phoneNumber.'
                }
                return Response(json_data, status=406)
        else:
            json_data = {
                'status_code': 400,
                'status': 'Failed',
                'message': f'Please provide phoneNumber. You have not provide any phoneNumber.'
            }
            return Response(json_data, status=406)
        # before sending check email is locked or not

        check_timestamp = self.check_number_is_locked(phone_number)
        if check_timestamp is None or is_otp_expired(check_timestamp):
            # generate otp
            otp = generate_otp()
            # send otp
            is_send = is_send_otp(phone_number=phone_number, otp=otp)
            # create and save otp in tabel
            obj = OTP.objects.create(phoneNumber=phone_number, otp=otp)
            obj.save()
            # create a session and add phoneNumber in session
            request.session['phone_number'] = phone_number
            request.session.set_expiry(300)
            # print('+++++++++++++++++++++++++++')
            print(f'Expiry session time is {request.session.get_expiry_age()//60} minutes only.')
            # print(is_send)
            if is_send:
                json_data = {
                    'status_code': 200,
                    'status': 'Success',
                    'message': f'OTP has sent successfully.'
                }
                return Response(json_data)
        else:
            default_otp_expiry_time = 300
            otp_expiry_time = getattr(settings, 'OTP_EXPIRY_DURATION', default_otp_expiry_time)
            json_data = {
                'status_code': status.HTTP_200_OK,
                'status': 'Failed',
                'message': f'You entered more then 3 times wrong OTP. Please try again after {otp_expiry_time // 60} minutes.'
            }
            return Response(json_data)
        json_data = {
            'status_code': status.HTTP_500_INTERNAL_SERVER_ERROR,
            'status': 'failed',
            'message': 'Please try after some time.'
        }
        return Response(json_data, status=500)


class VerifyOTP(APIView):

    def get_active_otp_by_number(self, phone_number):
        obj = None
        filtered_data = OTP.objects.filter(Q(phoneNumber=phone_number) & Q(status='active')).order_by('-timestamp').first()
        if filtered_data is not None:
            obj = filtered_data
        return obj

    def check_number_exist(self, phone_number):
        filtered_data = CustomUser.objects.filter(phoneNumber=phone_number)

        print("Record found===>", filtered_data)
        if len(filtered_data) == 1:
            obj = filtered_data[0]
            return True, obj.userId
        return False, None

    def post(self, request, *args, **kwargs):
        # check data is json or not
        is_json_data = is_json(data=request.body)
        # print('value==> ', value)
        if not is_json_data:
            json_data = {
                'status_code': status.HTTP_406_NOT_ACCEPTABLE,
                'status': 'Failed',
                'message': 'Please provide valid JSONData.'
            }
            return Response(json_data, status=406)

        # convert data into python dict
        # phone_number = request.data.get('phoneNumber')
        try:
            phone_number = request.session['phone_number']
        except KeyError:
            json_data = {
                'status_code': 500,
                'status': 'Failed',
                'message': 'Again request for new otp. Your session has expired.'
            }
            return Response(json_data)

        otp = request.data.get('otp')
        # find the latest OTP by mail_id form database
        instance = self.get_active_otp_by_number(phone_number=phone_number)

        # instance is None
        if instance is None:
            json_data = {
                'status_code': status.HTTP_406_NOT_ACCEPTABLE,
                'status': 'Failed',
                'message': "Invalid OTP."
            }
            return Response(json_data, status=406)

        # check otp length
        if len(otp) != 6:
            instance.count += 1
            instance.save()
            json_data = {
                'status_code': status.HTTP_200_OK,
                'status': 'Failed',
                'message': 'You entered wrong OTP.'
            }

            return Response(json_data)
        # check OTP is expired or not
        # if expired
        if is_otp_expired(instance.timestamp):
            json_data = {
                'status_code': status.HTTP_406_NOT_ACCEPTABLE,
                'status': 'Failed',
                'message': 'Your OTP has expired.'
            }
            return Response(json_data, status=406)
        else:
            if instance.otp == otp:
                instance.status = 'inactive'
                instance.save()
                # if otp is correct then next step

                is_number_exist, user_id = self.check_number_exist(phone_number=phone_number)

                if is_number_exist:
                    json_data = {
                        'status_code': status.HTTP_200_OK,
                        'status': 'Success',
                        'message': 'Your OTP has matched successfully.',
                        'data': {'userid': user_id}
                    }
                    return Response(json_data)

                serializers = HeadSerializer(data=request.data)
                if serializers.is_valid():
                    json_data = {
                        'status_code': status.HTTP_200_OK,
                        'status': 'Success',
                        'message': 'Data Submit Successfully.'
                    }
                    return Response(json_data)
                else:
                    json_data = {
                        'status_code': status.HTTP_200_OK,
                        'status': 'failed',
                        'message': serializers.errors
                    }
                    return Response(json_data)



            # if user enter more than 3 times wrong otp
            if instance.count >= 3:
                instance.status = 'locked'
                instance.save()
                default_otp_expiry_time = 300
                otp_expiry_time = getattr(settings, 'OTP_EXPIRY_DURATION', default_otp_expiry_time)
                json_data = {
                     'status_code': status.HTTP_200_OK,
                     'status': 'Failed',
                     'message': f'You entered more then 3 times wrong OTP. Please try again after {otp_expiry_time//60} minutes.'
                }
                return Response(json_data)

            instance.count += 1
            instance.save()
            json_data = {
                'status_code': status.HTTP_200_OK,
                'status': 'Failed',
                'message': 'You entered wrong OTP.'
                }

            return Response(json_data)




