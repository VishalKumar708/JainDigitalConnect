import random
from json import JSONDecodeError

from django.conf import settings
from django.core.mail import send_mail
from django.utils import timezone

import json
import re

from twilio.rest import Client


def generate_otp():
    """ Help to generate 6 digit OTP
    it returns 6 digit string value"""
    return str(random.randint(100000, 999999))


# def send_mail_to_client(mail_id, otp):
#     """ Help to send mail to recipient
#     it returns boolean value """
#     try:
#         # otp = generate_otp()
#         subject = "Jain Digit Connect Login OTP."
#         message = f"Your 6 digit otp is {otp} to verify email."
#         print('your otp==> ', otp)
#         from_email = settings.EMAIL_HOST_USER
#         recipient_list = (mail_id,)
#         send_mail(subject, message, from_email, recipient_list)
#         return True
#
#     except Exception as e:
#         print('Exception while sending email to client.', e)
#         return False


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


def is_json(data):
    """ Check the data is json or not"""
    try:
        json.loads(data)
        return True
    except JSONDecodeError:
        return False
    # except TypeError:
    #     return False


def is_valid_mobile_number(number):
    # Define a regular expression pattern for a valid mobile number with a maximum of 12 digits
    pattern = r'^\d{1,12}$'

    # Use re.match to check if the input matches the pattern
    if re.match(pattern, number):
        if len(number) == 10:
            return True
        else:
            return False
    else:
        return False


def is_send_otp(phone_number, otp):
    try:
        cl = Client(settings.SID, settings.AUTH_TOKEN)
        cl.messages.create(
            body=f'Your 6 digit otp code is {otp} to login Jain Digital Connect. Thankyou for registration.',
            from_=settings.SENDER_NUMBER, to='+91' + phone_number)
        return True
    except Exception as e:
        print('While sending otp on mobile an exception occur===> ', e)
        return False

# def validate_email_address(value):
#     pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
#     is_matched = re.match(pattern, value) is not None
#     if is_matched:
#         return True
#     return False
