from rest_framework import serializers
from jdcApi.models import City, Business, State
from django.db.models import Q

from utils.base_serializer import BaseSerializer


class GETCitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        # fields = ['cityId', 'cityName','city_by_areas']
        fields = ['cityId', 'cityName']


class CREATECitySerializer(BaseSerializer):
    """ this serializer use both 'getById, create and update' """

    class Meta:
        model = City
        fields = ['cityName', 'pincode', 'stateId', 'description', 'isActiveForResidents']

    def to_internal_value(self, data):
        city_name = data.get('cityName')
        state_id = data.get('stateId')
        pincode = data.get('pincode')
        errors = {}

        #  custom validation
        if state_id:
            try:
                # check stateId is integer or not
                int(state_id)
                # check state is exist or not
                State.objects.get(stateId=state_id)

                # check city name is not None
                if city_name:
                    matching_cities_count = City.objects.filter(stateId=state_id, cityName=city_name.strip()).count()
                    if matching_cities_count > 0:
                        errors['cityName'] = [f"'{city_name}' is already exist."]
            except State.DoesNotExist:
                errors['stateId'] = ["Invalid State Id."]
                print('does not exist error occur')
            except ValueError:
                print('value error occur')
                errors['stateId'] = [f"'stateId' expected a number but got '{state_id}'."]
        if pincode:
            if not pincode.strip().isdigit():
                errors['pincode'] = ["Enter a valid pincode."]
        validated_data = None
        # default validation
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


class UPDATECitySerializer(BaseSerializer):
    class Meta:
        model = City
        fields = ['cityName', 'pincode', 'stateId', 'description', 'isVerified', 'isActive', 'isActiveForResidents']

    def to_internal_value(self, data):

        # if user not provide at least one field to update record
        updated_fields = {key: value for key, value in data.items() if key in self.Meta.fields}
        if len(updated_fields) < 1:
            raise serializers.ValidationError(
                {'update_validation_error': ["At least one field must be provided to update the record."]})

        city_name = data.get('cityName')
        state_id = data.get('stateId')
        pincode = data.get('pincode')
        errors = {}
        validated_data = None
        if state_id:
            try:
                # check stateId is integer or not
                int(state_id)
                # check state is exist or not
                State.objects.get(stateId=state_id)
                # check city name is not None
                if city_name:
                    city_id = self.context.get('city_id')
                    matching_cities_count = City.objects.filter(Q(stateId=state_id), Q(cityName__iexact=city_name.strip()), ~Q(cityId=city_id)).count()
                    if matching_cities_count > 0:
                        errors['cityName'] = [f"'{city_name}' is already exist."]
            except State.DoesNotExist:
                errors['stateId'] = ["Invalid State Id."]
                print('does not exist error occur')
            except ValueError:
                print('value error occur')
                errors['stateId'] = [f"'stateId' expected a number but got '{state_id}'."]
        if pincode:
            if not pincode.strip().isdigit():
                errors['pincode'] = ["Enter a valid pincode."]

        # default validation
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


class GETCityByCityIdSerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ['cityId', 'cityName', 'pincode', 'stateId', 'description', 'isActiveForResidents']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if self.context.get('status'):
            data['isVerified'] = instance.isVerified
        return data

