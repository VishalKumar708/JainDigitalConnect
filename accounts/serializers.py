from .models import CustomUser
from rest_framework import serializers


class HeadSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ['name', 'fatherName', 'phoneNumber', 'cityId', 'address', 'maritalStatus', 'lookingForMatch', 'dob',
                  'sect', 'profession', 'phoneNumberVisibility', 'gender', 'gotra', 'bloodGroup', 'nativePlace',
                  'currentAddress']
        model = CustomUser



