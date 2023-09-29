from rest_framework import serializers
from .models import *


def check_pincode_length(value):
    try:
        int(value)
    except ValueError:
        raise serializers.ValidationError('Please enter only number')
    if len(value) == 6:
        return value
    raise serializers.ValidationError('Pincode length must be 6 not less than or greater than 6.')


# ******************* Area serializers ***********************
class PartialAreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Area
        # fields = ['areaId', 'areaName', 'selectState', 'selectCity']
        fields = ['areaId', 'areaName']


class AreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Area
        exclude = ['updatedDate', 'createdDate', 'groupId', 'createdBy', 'updatedBy']


#  **************  Business Serializers  ***********************
class BusinessSerializer(serializers.ModelSerializer):
    class Meta:
        model = Business
        exclude = ['groupId', 'createdBy', 'updatedBy', 'createdDate', 'updatedDate']


class PartialBusinessSerializer(serializers.ModelSerializer):
    class Meta:
        model = Business
        fields = ['businessId', 'businessName', 'businessType', 'businessNumber', 'email', 'website', 'businessDescription']
# ************************* city serializer  *****************************
class CitySerializer(serializers.ModelSerializer):
    pincode = serializers.CharField(validators=[check_pincode_length])

    class Meta:
        model = City
        exclude = ['updatedDate', 'createdDate', 'groupId', 'createdBy', 'updatedBy']


class PartialCitySerializer(serializers.ModelSerializer):


    class Meta:
        model = City
        # fields = ['cityId', 'cityName','city_by_areas']
        fields = ['cityId', 'cityName']


class GetAllAreaByCitySerializer(serializers.ModelSerializer):
    GetAllAreaByCityId = PartialAreaSerializer(read_only=True, many=True)

    class Meta:
        model = City
        fields = ['cityId', 'cityName', 'GetAllAreaByCityId']


class GetAllBusinessByCitySerializer(serializers.ModelSerializer):
    GetAllBusinessByCityId = PartialBusinessSerializer(read_only=True, many=True)

    class Meta:
        model = City
        fields = ['cityId', 'cityName', 'GetAllBusinessByCityId']


#  ******************* State serializers *************************

class StateSerializer(serializers.ModelSerializer):

    class Meta:
        model = State
        exclude = ['updatedDate', 'createdDate', 'groupId', 'createdBy', 'updatedBy']


class PartialStateSerializer(serializers.ModelSerializer):

    class Meta:
        model = State
        fields = ['stateId', 'stateName']


class GetAllCitiesByStateSerializer(serializers.ModelSerializer):
    city_by_state = PartialCitySerializer(read_only=True, many=True)

    class Meta:
        model = State
        fields = ('stateId', 'stateName', 'city_by_state')


#  ***********************    Literature Serializer ******************
class PartialLiteratureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Literature
        fields = ['literatureId', 'title']


class LiteratureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Literature
        fields = ['literatureId', 'title', 'body', 'isVerified', 'isActive']


#  *******************************  Aarti Serializer  ********************
class PartialAartiSerializer(serializers.ModelSerializer):
    class Meta:
        model = Aarti
        fields = ['aartiId', 'aartiName']


class AartiSerializer(serializers.ModelSerializer):
    class Meta:
        model = Aarti
        fields = ['aartiId', 'aartiName', 'aartiText', 'isVerified', 'isActive']


