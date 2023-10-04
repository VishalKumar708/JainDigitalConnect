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
class GETAreaSerializer(serializers.ModelSerializer):

    class Meta:
        model = Area
        fields = ['areaId', 'areaName']


class CREATEAreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Area
        fields = ['cityId', 'areaName', 'areaMC', 'landmark', 'areaContactNumber']

    def create(self, validated_data):
        validated_data['areaName'] = validated_data['areaName'].capitalize()
        # Create the user instance with modified data
        city_obj = self.Meta.model.objects.create(**validated_data)

        #  add data in field createdBy
        user_id_by_token = self.context.get('user_id_by_token')
        city_obj.createdBy = user_id_by_token
        city_obj.save()

        return city_obj


class UPDATEAreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Area
        fields = ['cityId', 'areaName', 'areaMC', 'landmark', 'areaContactNumber', 'isActive', 'isVerified']

    def update(self, instance, validated_data):
        # Update the user instance with modified data
        validated_data['areaName'] = validated_data['areaName'].capitalize()

        user_id_by_token = self.context.get('user_id_by_token')
        validated_data['updatedBy'] = user_id_by_token
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class GETAreaByAreaIdSerializer(serializers.ModelSerializer):
    class Meta:
        model = Area
        fields = ['cityId', 'areaName', 'areaMC', 'landmark', 'areaContactNumber', 'isActive', 'isVerified']


#  **************  Business Serializers  ***********************
class CREATEBusinessSerializer(serializers.ModelSerializer):
    class Meta:
        model = Business
        fields = ['cityId', 'userId', 'businessName', 'businessType', 'businessPhoneNumber', 'email', 'website', 'businessDescription']

    def create(self, validated_data):
        validated_data['businessName'] = validated_data['businessName'].capitalize()
        # Create the user instance with modified data
        city_obj = self.Meta.model.objects.create(**validated_data)

        #  add data in field createdBy
        user_id_by_token = self.context.get('user_id_by_token')
        city_obj.createdBy = user_id_by_token
        city_obj.save()

        return city_obj

    def to_internal_value(self, data):
        city_id = data.get('cityId')
        user_id = data.get('userId')

        # Custom validation for cityId and userId
        if not City.objects.filter(cityId=city_id).exists():
            raise serializers.ValidationError({'cityId': 'Invalid cityId - Id does not exist.'})

        if not User.objects.filter(id=user_id).exists():
            raise serializers.ValidationError({'userId': 'Invalid userId - Id does not exist.'})

        return super().to_internal_value(data)


class UPDATEBusinessSerializer(serializers.ModelSerializer):
    class Meta:
        model = Business
        fields = ['businessName', 'businessType', 'businessPhoneNumber', 'email', 'website', 'businessDescription', 'isVerified', 'isActive']

    def update(self, instance, validated_data):
        # Update the user instance with modified data
        try:
            validated_data['businessName'] = validated_data['businessName'].capitalize()
        except KeyError:
            pass
        user_id_by_token = self.context.get('user_id_by_token')
        validated_data['updatedBy'] = user_id_by_token
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

    def to_internal_value(self, data):
        city_id = data.get('cityId')
        if not City.objects.filter(cityId=city_id).exists() and city_id is not None:
            raise serializers.ValidationError({'cityId': 'Invalid cityId - Id does not exist.'})

        return super().to_internal_value(data)

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



class UPDATECitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ['cityName', 'pincode', 'stateId', 'description', 'isVerified', 'isActive']

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
    areas = serializers.SerializerMethodField()

    class Meta:
        model = City
        fields = ['cityId', 'cityName', 'areas']

    def get_areas(self, obj):
        city_id = self.context.get('cityId')
        # Retrieve 'areaId' and 'areaName' fields from areas where isActive=True and isVerified=True
        areas = Area.objects.filter(isActive=True, isVerified=True, cityId=city_id).values('areaId', 'areaName')
        return areas


class GetAllBusinessByCitySerializer(serializers.ModelSerializer):
    # GetAllBusinessByCityId = PartialBusinessSerializer(read_only=True, many=True)
    allBusiness = serializers.SerializerMethodField()

    class Meta:
        model = City
        fields = ['cityId', 'cityName', 'allBusiness']

    def get_allBusiness(self, obj):
        city_id = self.context.get('cityId')
        business = Business.objects.filter(isActive=True, isVerified=True, cityId=city_id).values('businessId', 'businessName','businessType', 'businessDescription', 'businessNumber', 'email', 'website')
        return business



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


