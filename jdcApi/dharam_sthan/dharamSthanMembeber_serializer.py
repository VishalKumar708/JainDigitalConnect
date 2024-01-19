from django.db.models import Q
from rest_framework import serializers
from jdcApi.models import DharamSthanMember, DharamSthan
from utils.base_serializer import BaseSerializer


class CREATEDharamSthanMemberSerializer(BaseSerializer):
    name = serializers.CharField(required=True, allow_null=False)

    class Meta:
        model = DharamSthanMember
        fields = ['name', "dharamSthanId", 'position', 'phoneNumber']

    def to_internal_value(self, data):
        dharam_sthan_id = data.get('dharamSthanId')
        errors = {}
        # custom validation
        if dharam_sthan_id:
            try:
                DharamSthan.objects.get(id=dharam_sthan_id)
            except DharamSthan.DoesNotExist:
                errors['dharamSthanId'] = ["Invalid Id."]
            except ValueError:
                errors['dharamSthanId'] = [f"excepted a number but got '{dharam_sthan_id}'."]

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


class UPDATEDharamSthanMemberByIdSerializer(BaseSerializer):

    class Meta:
        model = DharamSthanMember
        fields = ['name', "dharamSthanId", 'position', 'phoneNumber', 'isVerified', 'isActive']

    def to_internal_value(self, data):
        dharam_sthan_id = data.get('dharamSthanId')
        errors = {}
        # custom validation
        if dharam_sthan_id:
            try:
                DharamSthan.objects.get(id=dharam_sthan_id)
            except DharamSthan.DoesNotExist:
                errors['dharamSthanId'] = ["Invalid Id."]
            except ValueError:
                errors['dharamSthanId'] = [f"excepted a number but got '{dharam_sthan_id}'."]

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


class GETDharamSthanMemberDetialsByIdSerializer(serializers.ModelSerializer):

    class Meta:
        model = DharamSthanMember
        fields = ['id', 'name', 'position', 'phoneNumber', 'isActive', 'isVerified']



