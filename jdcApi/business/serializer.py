
from rest_framework import serializers
from jdcApi.models import City, Business
from accounts.models import User
from datetime import datetime

from utils.base_serializer import BaseSerializer
from phonenumber_field.serializerfields import PhoneNumberField


class CREATEBusinessSerializer(BaseSerializer):
    businessPhoneNumber = PhoneNumberField()

    class Meta:
        model = Business
        fields = ['cityId', 'userId', 'businessName', 'businessType', 'businessPhoneNumber', 'email', 'website','gstNumber', 'address', 'businessDescription']

    def to_internal_value(self, data):
        city_id = data.get('cityId')
        business_name = data.get('businessName')
        user_id = data.get('userId')
        errors = {}
        # Custom validation for cityId and userId
        if city_id:
            try:
                City.objects.filter(cityId=city_id)
            except City.DoesNotExist:
                errors['cityId'] = ["Invalid cityId."]
            except ValueError:
                errors['cityId'] = [f"excepted a number but got {city_id}."]
        if user_id:
            try:
                User.objects.get(id=user_id)
            except User.DoesNotExist:
                errors['userId'] = ["Invalid User Id."]
            except ValueError:
                errors['userId'] = [f"excepted a number but got '{user_id}'."]

        if business_name and user_id:
            try:
                filtered_data = Business.objects.filter(userId=user_id,
                                                        businessName__icontains=business_name.strip()).count()
                if filtered_data > 0:
                    errors['businessName'] = [f"'{business_name}' already exist."]
            except ValueError:
                pass

        #  default validation
        validated_data = None
        try:
            # store all data in "validated_data" variable and return it
            validated_data = super().to_internal_value(data)
        except serializers.ValidationError as e:
            new_errors = e.detail.copy()  # Make a copy of the custom errors
            for key, value in new_errors.items():
                if key not in errors:
                    errors[key] = value  # Add new keys to the errors dictionary

        # return all validations errors
        if errors:
            # print('errors ==> ', errors)
            raise serializers.ValidationError(errors)

        return validated_data


class PUTBusinessSerializer(BaseSerializer):
    businessPhoneNumber = PhoneNumberField()
    class Meta:
        model = Business
        fields = ['userId', 'cityId', 'businessName', 'businessType', 'businessPhoneNumber', 'email', 'website','gstNumber','address', 'businessDescription', 'isVerified', 'isActive']

    def to_internal_value(self, data):
        updated_fields = {key: value for key, value in data.items() if key in self.Meta.fields}
        if len(updated_fields) < 1:
            raise serializers.ValidationError(
                {'update_validation_error': ["At least one field must be provided to update the record."]})

        city_id = data.get('cityId')
        user_id = data.get('userId')
        errors = {}
        # Custom validation for cityId and userId
        if city_id:
            try:
                City.objects.filter(cityId=city_id)
            except City.DoesNotExist:
                errors['cityId'] = ["Invalid cityId."]
            except ValueError:
                errors['cityId'] = [f"excepted a number but got {city_id}."]
        if user_id:
            try:
                User.objects.get(id=user_id)
            except User.DoesNotExist:
                errors['userId'] = ["Invalid User Id."]
            except ValueError:
                errors['userId'] = [f"excepted a number but got '{user_id}'."]

        #  default validation
        validated_data = None
        try:
            # store all data in "validated_data" variable and return it
            validated_data = super().to_internal_value(data)
        except serializers.ValidationError as e:
            new_errors = e.detail.copy()  # Make a copy of the custom errors
            for key, value in new_errors.items():
                if key not in errors:
                    errors[key] = value  # Add new keys to the errors dictionary

        # return all validations errors
        if errors:
            # print('errors ==> ', errors)
            raise serializers.ValidationError(errors)

        return validated_data


class GETBusinessSerializer(serializers.ModelSerializer):
    businessPhoneNumber = PhoneNumberField(default="")
    class Meta:
        model = Business
        fields = ['businessId', 'businessName', 'businessType', 'businessDescription', 'businessPhoneNumber', 'website', 'email', 'gstNumber', 'address']


class GETBusinessByIdSerializer(serializers.ModelSerializer):
    cityName = serializers.CharField(source='cityId.cityName', read_only=True)
    businessPhoneNumber = PhoneNumberField(default="")
    countryCode = serializers.SerializerMethodField()
    phoneNumber = serializers.CharField(source='businessPhoneNumber.national_number', default=None)

    class Meta:
        model = Business
        fields = ['businessId','cityId', 'cityName','countryCode','phoneNumber', 'businessName', 'businessType', 'businessPhoneNumber', 'email', 'website', 'gstNumber', 'businessDescription', 'isVerified', 'isActive']

    def get_countryCode(self, instance):
        print('business phoneNumber==> ',instance.businessPhoneNumber)
        if instance.businessPhoneNumber:
            return f"+{instance.businessPhoneNumber.country_code}"
        return None


class GETCityCountForBusinessSerializer(serializers.ModelSerializer):
    count = serializers.IntegerField()

    class Meta:
        model = City
        fields = ['cityId', 'cityName', 'count']


class GETCitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City

        fields = ['cityId', 'cityName']

