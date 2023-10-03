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

class GETCitySerializer(serializers.ModelSerializer):

    class Meta:
        model = City
        # fields = ['cityId', 'cityName','city_by_areas']
        fields = ['cityId', 'cityName']


class CREATECitySerializer(serializers.ModelSerializer):
    """ this serializer use both 'getById, create and update' """

    class Meta:
        model = City
        fields = ['cityName', 'pincode', 'stateId', 'description']

    def create(self, validated_data):
        validated_data['cityName'] = validated_data['cityName'].capitalize()
        # Create the user instance with modified data
        city_obj = self.Meta.model.objects.create(**validated_data)

        #  add data in field createdBy
        user_id_by_token = self.context.get('user_id_by_token')
        city_obj.createdBy = user_id_by_token
        city_obj.save()

        return city_obj

    def update(self, instance, validated_data):
        # Update the user instance with modified data
        validated_data['cityName'] = validated_data['cityName'].capitalize()

        user_id_by_token = self.context.get('user_id_by_token')
        validated_data['updatedBy'] = user_id_by_token
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class GETCityByCityIdSerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ['cityId', 'cityName', 'pincode', 'stateId', 'description']


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

class GETStateSerializer(serializers.ModelSerializer):

    class Meta:
        model = State
        fields = ['stateId', 'stateName']


class CREATEStateSerializer(serializers.ModelSerializer):
    """ this serializer use both 'create and update' """
    class Meta:
        model = State
        fields = ['stateName']

    def create(self, validated_data):
        validated_data['stateName'] = validated_data['stateName'].capitalize()
        # Create the user instance with modified data
        state_obj = self.Meta.model.objects.create(**validated_data)

        #  add data in field createdBy
        user_id_by_token = self.context.get('user_id_by_token')
        state_obj.createdBy = user_id_by_token
        state_obj.save()

        return state_obj

    def update(self, instance, validated_data):
        # Update the user instance with modified data
        validated_data['stateName'] = validated_data['stateName'].capitalize()

        user_id_by_token = self.context.get('user_id_by_token')
        validated_data['updatedBy'] = user_id_by_token
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class GetAllCitiesByStateSerializer(serializers.ModelSerializer):
    city_by_state = GETCitySerializer(read_only=True, many=True)

    class Meta:
        model = State
        fields = ('stateId', 'stateName', 'city_by_state')


#  ***********************    Literature Serializer  ******************
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


