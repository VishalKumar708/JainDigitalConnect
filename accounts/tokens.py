import re

from django.utils import timezone

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from django.conf import settings
from .models import User  # Import your User model here

from rest_framework import serializers


def is_valid_mobile_number(number):
    # Define a regular expression pattern for a valid mobile number with a maximum of 12 digits
    pattern = r'^\d{1,10}$'

    # Use re.match to check if the input matches the pattern
    if re.match(pattern, number) and len(number) == 10:
        return number
    else:
        raise serializers.ValidationError("Phone Number length should be 10 or only integers are allowed.")


class ObtainTokeSerializer(serializers.Serializer):
    id = serializers.CharField()
    # phoneNumber = serializers.CharField(validators=[is_valid_mobile_number])


@api_view(['POST'])
# @permission_classes([])
def obtain_token(request):
    serializer = ObtainTokeSerializer(data=request.data)
    if not serializer.is_valid():
        json_data = {
            'statusCode': status.HTTP_400_BAD_REQUEST,
            'status': 'failed',
            'data': {'error': serializer.errors}
        }
        return Response(json_data, status=400)
    user_id = request.data.get('id')  # Replace with your authentication criteria
    # Authenticate the user based on userId and phoneNumber
    try:
        user = User.objects.get(id=user_id)
        print("user ==> ", user)
    except User.DoesNotExist:
        json_data = {
            'statusCode': status.HTTP_400_BAD_REQUEST,
            'status': 'failed',
            'data': {'error': 'Invalid credentials.'}
        }
        return Response(json_data, status=status.HTTP_400_BAD_REQUEST)

    # Generate a refresh token
    refresh = RefreshToken.for_user(user)

    # Set the token expiration time
    refresh.access_token.set_exp(timezone.now() + settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'])

    # Manually set a unique identifier (JTI) for the refresh token
    # refresh['jti'] = 'your_unique_jti_value'

    # Create a dictionary with access and refresh tokens
    tokens = {
        'access': str(refresh.access_token),
        'refresh': str(refresh),
    }

    return Response(tokens, status=status.HTTP_200_OK)


def generate_tokens(user_id, phone_number):

    # Authenticate the user based on userId and phoneNumber
    try:
        user = User.objects.get(id=user_id, phoneNumber=phone_number)
        print("user ==> ", user)
    except User.DoesNotExist:
        return False, {'error': 'Invalid credentials.'}


    # Generate a refresh token
    refresh = RefreshToken.for_user(user)

    # Set the token expiration time
    refresh.access_token.set_exp(timezone.now() + settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'])

    # Manually set a unique identifier (JTI) for the refresh token
    # refresh['jti'] = 'your_unique_jti_value'

    # Create a dictionary with access and refresh tokens
    tokens = {
        'access': str(refresh.access_token),
        'refresh': str(refresh),
    }

    return True, tokens


