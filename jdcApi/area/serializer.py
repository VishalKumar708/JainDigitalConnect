from django.db.models import Q
from rest_framework import serializers
from jdcApi.models import Area, City
# from datetime import datetime
from accounts.models import User
from utils.base_serializer import BaseSerializer


class GETAreaForAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Area
        fields = ['areaId', 'areaName', 'areaContactNumber']


class CREATEAreaSerializer(BaseSerializer):
    class Meta:
        model = Area
        fields = ['cityId', 'areaName', 'areaMC', 'landmark', 'areaContactNumber']

    def to_internal_value(self, data):
        city_id = data.get('cityId')
        area_name = data.get('areaName')
        contact_number = data.get('areaContactNumber')
        errors = {}
        # custom validation
        if city_id:
            try:
                City.objects.get(cityId=city_id)
                if area_name:
                    matching_cities_count = Area.objects.filter(
                        Q(cityId=city_id) & Q(areaName__iexact=area_name.strip())).count()
                    if matching_cities_count > 0:
                        errors['areaName'] = [f"'{area_name}' is already exist."]
            except City.DoesNotExist:
                errors['cityId'] = ["Invalid City Id."]
            except ValueError:
                errors['cityId'] = [f"'city id' excepted a number but got '{city_id}'."]

        # if contact_number:
        #     if not str(contact_number).isdigit() or len(str(contact_number)) != 10:
        #         errors['areaContactNumber'] = ['Please Enter a Valid Number.']
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


class UPDATEAreaSerializer(BaseSerializer):
    class Meta:
        model = Area
        fields = ['cityId', 'areaName', 'areaMC', 'landmark', 'areaContactNumber', 'isActive', 'isVerified']

    def to_internal_value(self, data):
        updated_fields = {key: value for key, value in data.items() if key in self.Meta.fields}
        if len(updated_fields) == 0:
            raise serializers.ValidationError(
                {'update_validation_error': ["At least one field must be provided to update the record."]})

        city_id = data.get('cityId')
        area_name = data.get('areaName')

        errors = {}
        # custom validation
        if city_id:
            try:
                City.objects.get(cityId=city_id)
                if area_name:
                    area_id = self.context.get('areaId')
                    matching_cities_count = Area.objects.filter(Q(areaName__iexact=area_name.strip()),
                                                                ~Q(areaId=area_id), ~Q(cityId=city_id)).count()
                    if matching_cities_count > 0:
                        errors['areaName'] = [f"'{area_name}' is already exist."]
            except City.DoesNotExist:
                errors['cityId'] = ["Invalid City Id."]
            except ValueError:
                errors['cityId'] = [f"'city id' excepted a number but got '{city_id}'."]

        if city_id is None and area_name:
            errors['areaName'] = [f"to update 'areaName' must provide 'cityId' also."]
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


class GETResidentsByAreaId(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['cityId', 'areaName', 'areaMC', 'landmark', 'areaContactNumber', 'isActive', 'isVerified']


class GETAreaByAreaIdSerializer(serializers.ModelSerializer):
    class Meta:
        model = Area
        fields = ['cityId', 'areaName', 'areaMC', 'landmark', 'areaContactNumber', 'isActive', 'isVerified']


