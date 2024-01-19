from rest_framework import serializers
from jdcApi.models import City, Emergency
from utils.base_serializer import BaseSerializer


class CREATEEmergencySerializer(BaseSerializer):

    class Meta:
        fields = ['cityId', 'departmentName', 'phoneNumber', 'email', 'website']
        model = Emergency

    def to_internal_value(self, data):
        city_id = data.get('cityId')
        phone_number = data.get('phoneNumber')
        department_name = data.get('departmentName')
        errors = {}
        # custom validation
        if city_id:
            try:
                City.objects.get(cityId=city_id)
            except City.DoesNotExist:
                errors['cityId'] = ["Invalid City Id."]
            except ValueError:
                errors['cityId'] = [f"'city id' excepted a number but got '{city_id}'."]

        if phone_number:
            if not str(phone_number).strip().isdigit() or (len(str(phone_number)) < 3 and len(str(phone_number)) > 15):
                errors['phoneNumber'] = [f"Phone Number length should be between 3 to 15 digits."]

        if department_name and city_id:
            field = ['phoneNumber', 'email', 'website']
            at_least_one_field = [key for key in field if key in data]
            print('one field==> ', len(at_least_one_field))
            if len(at_least_one_field) < 1:
                errors['atLeastOneField'] = ['Please fill Either phoneNumber, email or website']

        # default validation
        validated_data = None
        try:
            # store all data in "validated_data" variable and return it
            validated_data = super().to_internal_value(data)
        except serializers.ValidationError as e:
            new_errors = e.detail.copy()  # Make a copy of the custom errors
            for key, value in new_errors.items():
                if key not in errors:
                    errors[key] = value  # Add new keys to the errors dictionary

        # raise validations errors
        if errors:
            # print('errors ==> ', errors)
            raise serializers.ValidationError(errors)

        return validated_data


class UPDATEEmergencySerializer(BaseSerializer):

    class Meta:
        fields = ['cityId', 'departmentName', 'phoneNumber', 'email', 'website', 'isVerified', 'isActive']
        model = Emergency

    def to_internal_value(self, data):
        updated_fields = {key: value for key, value in data.items() if key in self.Meta.fields}
        if len(updated_fields) == 0:
            raise serializers.ValidationError(
                {'update_validation_error': ["At least one field must be provided to update the record."]})

        city_id = data.get('cityId')
        phone_number = data.get('phoneNumber')

        errors = {}
        # custom validation
        if city_id:
            try:
                City.objects.get(cityId=city_id)
            except City.DoesNotExist:
                errors['cityId'] = ["Invalid City Id."]
            except ValueError:
                errors['cityId'] = [f"excepted a number but got '{city_id}'."]

        if phone_number:

            if not str(phone_number).strip().isdigit() or len(str(phone_number)) < 3:
                errors['phoneNumber'] = [f"Phone Number length should be between 3 to 15 digits."]

        # default validation
        validated_data = None
        try:
            # store all data in "validated_data" variable and return it
            validated_data = super().to_internal_value(data)
        except serializers.ValidationError as e:
            new_errors = e.detail.copy()  # Make a copy of the custom errors
            for key, value in new_errors.items():
                if key not in errors:
                    errors[key] = value  # Add new keys to the errors dictionary

        # raise validations errors
        if errors:
            # print('errors ==> ', errors)
            raise serializers.ValidationError(errors)

        return validated_data


class GETEmergencyDetailsSerializer(serializers.ModelSerializer):
    cityName = serializers.CharField(source='cityId.cityName')

    class Meta:
        fields = ['id', 'cityId', 'cityName', 'departmentName', 'phoneNumber', 'email', 'website', 'isVerified', 'isActive']
        model = Emergency


class GETCityWithCountSerializer(serializers.ModelSerializer):
    count = serializers.IntegerField()

    class Meta:
        model = City
        fields = ['cityId', 'cityName', 'count']


class GETCitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ['cityId', 'cityName']


class GETAllEmergencySerializer(serializers.ModelSerializer):

    class Meta:
        fields = ['id', 'departmentName', 'cityId', 'phoneNumber', 'email', 'website']
        model = Emergency

