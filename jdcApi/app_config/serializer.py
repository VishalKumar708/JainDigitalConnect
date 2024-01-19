from django.db.models import Q
from rest_framework import serializers
from jdcApi.models import MstSect, AppConfigurations
from accounts.models import User
from utils.base_serializer import BaseSerializer

class CREATEAppConfigurationSerializer(BaseSerializer):

    class Meta:
        fields = ['configurationKey', 'configurationValue', 'createdBy', 'updatedBy']
        model = AppConfigurations

    # def create(self, validated_data):
    #     # Transform configurationKey to the desired format
    #     configuration_key = validated_data.get('configurationKey', '')
    #     validated_data['configurationKey'] = configuration_key.replace(' ', '').lower()  # Remove spaces and convert to lowercase
    #
    #     return obj

    def to_internal_value(self, data):
        configuration_key = data.get('configurationKey')

        errors = {}
        # custom validation

        if configuration_key:
            filtered_object = AppConfigurations.objects.filter(configurationKey__iexact=configuration_key.strip().replace(' ', '')).count()
            # print('filtered object ==> ', filtered_object)
            if filtered_object > 0:
                errors['configurationKey'] = [f"'{configuration_key}' is already exist."]

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
            raise serializers.ValidationError(errors)
        if validated_data.get('configurationKey'):
            validated_data['configurationKey'] = configuration_key.replace(' ', '').lower()
        return validated_data


class UPDATEAppConfigurationSerializer(BaseSerializer):
    class Meta:
        fields = ['configurationKey', 'configurationValue', 'createdBy', 'updatedBy']
        model = AppConfigurations

    # def update(self, instance, validated_data):
    #     if validated_data.get('configurationKey'):
    #         validated_data['configurationKey'] = validated_data['configurationKey'].replace(' ', '').lower()
    #
    #     user_id_by_token = self.context.get('user_id_by_token')
    #     validated_data['updatedBy'] = user_id_by_token
    #     for attr, value in validated_data.items():
    #         setattr(instance, attr, value)
    #     instance.save()
    #     return instance

    def to_internal_value(self, data):
        configuration_key = data.get('configurationKey')

        errors = {}

        # custom validation
        if configuration_key:
            filtered_object = AppConfigurations.objects.filter(~Q(id=self.context.get('id')), Q(configurationKey__iexact=configuration_key.strip().replace(' ', ''))).count()
            # print('filtered object ==> ', filtered_object)
            if filtered_object > 0:
                errors['configurationKey'] = [f"'{configuration_key}' is already exist."]

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
            raise serializers.ValidationError(errors)

        if validated_data.get('configurationKey'):
            validated_data['configurationKey'] = configuration_key.replace(' ', '').lower()
        return validated_data


class GETAppConfigurationByIdSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ['id', 'configurationKey', 'configurationValue']
        model = AppConfigurations


class GETAllAppConfigurationSerializer(serializers.ModelSerializer):
    updatedBy = serializers.CharField(source='createdBy.name', default="")
    updatedDateTime = serializers.SerializerMethodField()

    class Meta:
        fields = ['id', 'configurationKey', 'configurationValue', 'updatedBy', 'updatedDateTime']
        model = AppConfigurations

    def get_updatedDateTime(self, instance):
        return instance.updatedDate.strftime("%d %B, %Y %I:%M %p")
