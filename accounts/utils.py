import random
from json import JSONDecodeError

from django.conf import settings
from django.core.mail import send_mail
from django.utils import timezone

import json
import re

from twilio.rest import Client


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

def is_valid_mobile_number(number):
    # Define a regular expression pattern for a valid mobile number with a maximum of 12 digits
    pattern = r'^\d{1,10}$'

    # Use re.match to check if the input matches the pattern
    if re.match(pattern, number):
        return True
    else:
        return False


def is_integer(id):
    try:
        int(id)
        return True
    except ValueError:
        return False


def string_to_bool(input_str):
    if input_str.lower() == "true":
        return True
    elif input_str.lower() == "false":
        return False

# def validate_email_address(value):
#     pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
#     is_matched = re.match(pattern, value) is not None
#     if is_matched:
#         return True
#     return False
