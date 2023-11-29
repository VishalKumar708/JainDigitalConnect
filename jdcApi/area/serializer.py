from django.db.models import Q
from rest_framework import serializers
from jdcApi.models import Area, City
# from datetime import datetime
from accounts.models import User


class GETAreaWithCountSerializer(serializers.ModelSerializer):
    count = serializers.SerializerMethodField()

    class Meta:
        model = Area
        fields = ['areaId', 'areaName', 'count']

    def get_count(self, instance):
        total_members = User.objects.filter(areaId=instance.areaId).count()
        return total_members


class GETAreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Area
        fields = ['areaId', 'areaName']


class GETAreaForAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Area
        fields = ['areaId', 'areaName', 'areaContactNumber']


class CREATEAreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Area
        fields = ['cityId', 'areaName', 'areaMC', 'landmark', 'areaContactNumber']

    def to_internal_value(self, data):
        city_id = data.get('cityId')
        area_name = data.get('areaName')
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
        if validated_data.get('areaName'):
            validated_data['areaName'] = validated_data['areaName'].capitalize()

        user_id_by_token = self.context.get('user_id_by_token')
        validated_data['updatedBy'] = user_id_by_token
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

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


