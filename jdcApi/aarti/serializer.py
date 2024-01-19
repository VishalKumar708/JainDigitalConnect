from django.db.models import Q
from rest_framework import serializers
from jdcApi.models import Aarti
from masterApi.models import MstSect
from accounts.models import User
from utils.base_serializer import BaseSerializer


class GETAllSectWithCountForAartiSerializer(serializers.ModelSerializer):
    count = serializers.IntegerField()

    class Meta:
        model = MstSect
        fields = ['id', 'sectName', 'count']


class GETAartiSerializer(serializers.ModelSerializer):
    uploadedBy = serializers.CharField(source='createdBy.name', default="")

    class Meta:
        model = Aarti
        fields = ['id', 'aartiName', 'uploadedBy']



class CREATEAartiSerializer(BaseSerializer):
    class Meta:
        model = Aarti
        fields = ['aartiName', 'sectId', 'order', 'aartiText']



    def to_internal_value(self, data):
        aarti_name = data.get('aartiName')
        sect_id = data.get('sectId')

        errors = {}
        # custom validation
        if sect_id:
            try:
                MstSect.objects.get(id=sect_id)
            except MstSect.DoesNotExist:
                errors['sectId'] = ['Invalid Sect Id.']
            except ValueError:
                errors['sectId'] = [f"'sectId' excepted a number but got '{sect_id}."]

        if aarti_name:
            matching_literature_count = Aarti.objects.filter(aartiName__iexact=aarti_name.strip()).count()
            if matching_literature_count > 0:
                errors['title'] = ['This Aarti is already exist.']

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


class UPDATEAartiSerializer(BaseSerializer):
    class Meta:
        model = Aarti
        fields = ['aartiName', 'sectId', 'order', 'aartiText', 'isVerified', 'isActive']

    def to_internal_value(self, data):
        sect_id = data.get('sectId')
        aarti_name = data.get('title')
        errors = {}

        # custom validation
        if sect_id:
            try:
                MstSect.objects.get(id=sect_id)
            except MstSect.DoesNotExist:
                errors['sectId'] = ['Invalid Sect Id.']
            except ValueError:
                errors['sectId'] = [f"'sectId' excepted a number but got '{sect_id}."]

        if aarti_name:
            aarti_id = self.context.get('aarti_id')
            matching_aarti_count = Aarti.objects.filter(Q(aartiName=aarti_name), ~Q(id=aarti_id),).count()
            if matching_aarti_count > 0:
                errors['title'] = ['This Aarti is already exist.']
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


class GETAartiByIdSerializer(serializers.ModelSerializer):
    sectName = serializers.CharField(source='sectId.sectName')

    class Meta:
        model = Aarti
        fields = ['id', 'aartiName', 'sectId', 'sectName', 'order', 'aartiText', 'isVerified', 'isActive']


class GETAartiForAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Aarti
        fields = ['id', 'aartiName']
