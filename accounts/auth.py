import random
from django.conf import settings
from django.utils import timezone
from json import JSONDecodeError
import json
from twilio.rest import Client
from .models import CustomUser
from django.db.models import Q

import logging
logger = logging.getLogger(__name__)
logger_auth = logging.getLogger('auth_log')

import traceback


# check data is in json format or not
def is_json(data):
    """ Check the data is json or not"""
    # print("request.data==> ", data)
    try:
        json.loads(data)
        return True
    except JSONDecodeError:
        return False


# to generate otp
def generate_otp():
    """ Help to generate 6 digit OTP
    it returns 6 digit string value"""
    return str(random.randint(100000, 999999))


# check otp is expired or not
def is_otp_expired(timestamp):
    """help to check OTP is expired or not.
    it returns boolean value.
    default OTP expiry time is 5 minutes."""
    default_otp_expiry_time = 300
    otp_expiry_time = getattr(settings, 'OTP_EXPIRY_DURATION', default_otp_expiry_time)
    expiry_duration = timezone.timedelta(seconds=otp_expiry_time)
    now = timezone.now()
    if now > (timestamp+expiry_duration):
        return True  # means expired
    return False


# check otp send or not
def is_send_otp(phone_number, otp):
    """Help to send otp on a phone number"""
    try:
        cl = Client(settings.SID, settings.AUTH_TOKEN)
        cl.messages.create(
            body=f'Your 6 digit otp code is {otp} to login Jain Digital Connect. Thankyou for registration.',
            from_=settings.SENDER_NUMBER, to='+91' + phone_number)
        logger_auth.info('OTP Sent Successfully.')
        return True
    except Exception as e:
        # error_message = traceback.format_exception_only(str(e))[0]
        error_message = traceback.format_exception(e, limit=0)
        logger_auth.error('While sending OTP to client an exception occur == > %s ', error_message)
        print('While sending otp on mobile an exception occur===> ', Exception(e))
        return False


def check_number_exist_for_login(phone_number):
    """"to check user can login or not """
    filtered_data = CustomUser.objects.filter(phoneNumber=phone_number)
    print("Record found===>", filtered_data)
    if len(filtered_data) == 1:
        obj = filtered_data[0]
        return True, obj
    return False, None


def before_update_check_number_exist(phone_number, user_id):
    """"to check user can login or not """
    filtered_data = CustomUser.objects.filter(Q(phoneNumber=phone_number) & ~Q(userId=user_id))
    print("Record found===>", filtered_data)
    if len(filtered_data) == 1:
        return True
    return False


def is_account_exist(phone_number):
    """ to check the number already exists or not"""
    filtered_data = CustomUser.objects.filter(phoneNumber=phone_number)
    print("Record found===>", filtered_data)
    if len(filtered_data) == 1:
        obj = filtered_data[0]
        return True, obj.userId
    return False, None


def check_number_exist_for_add_member(phone_number):
    """to check member number exist or not"""
    filtered_data = CustomUser.objects.filter(phoneNumber=phone_number)
    # print("Record found===>", filtered_data)
    if len(filtered_data) == 1:
        return True
    return False


def check_head_exist_by_id(id):
    """ check user id is existed or not """
    try:
        CustomUser.objects.get(userId=id, headId=None)
        return True
    except CustomUser.DoesNotExist:
        return False


from datetime import datetime


def is_applicable_for_matrimonial(birthdate_str, gender):
    """ to check user is applicable for matrimonial or not"""
    # Convert the input date string to a datetime object
    try:
        birthdate = datetime.strptime(birthdate_str.strip(), '%B %d, %Y')

        # Get the current date
        current_date = datetime.now()

        # Calculate the age
        age = current_date.year - birthdate.year - (
                    (current_date.month, current_date.day) < (birthdate.month, birthdate.day))

        if gender == 'male' and age < 21:
            return False, 'Sorry! Your age is less then 21. So You are not eligible for matrimonial'
        elif gender == 'female' and age < 18:
            return False, 'Sorry! Your age is less then 18. So You are not eligible for matrimonial'
        return True, " "
    except Exception as e:
        print('failed===> ', e)
        return False, " "
    # return age


def get_age_by_dob(birthdate_str):
    """ to calculate age by date of birth"""
    birthdate = datetime.strptime(birthdate_str, '%B %d %Y')

    # Get the current date
    current_date = datetime.now()

    # Calculate the age
    age = current_date.year - birthdate.year - (
            (current_date.month, current_date.day) < (birthdate.month, birthdate.day))

    return age


def check_same_name_member_in_a_head(head_id, member_name):
    """if member number is 0000000000 then check name if name not same then add """
    filtered_data = CustomUser.objects.filter(phoneNumber='0000000000', headId=head_id, name__iexact=member_name)

    if len(filtered_data)>0:
        return True
    return False




