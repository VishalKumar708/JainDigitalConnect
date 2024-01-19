from django.db.models import Q
from rest_framework import serializers
from jdcApi.models import Literature, MstSect
from utils.base_serializer import BaseSerializer


class GETAllSectWithCountForLiteratureSerializer(serializers.ModelSerializer):
    count = serializers.IntegerField()

    class Meta:
        model = MstSect
        fields = ['id', 'sectName', 'count']




class GETLiteratureSerializer(serializers.ModelSerializer):
    uploadedBy = serializers.CharField(source="createdBy.name")

    class Meta:
        model = Literature
        fields = ['id', 'title', 'uploadedBy']




class CREATELiteratureSerializer(BaseSerializer):
    class Meta:
        model = Literature
        fields = ['title', 'sectId', 'order', 'body']


    def to_internal_value(self, data):
        title = data.get('title')
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

        if title:
            matching_literature_count = Literature.objects.filter(title__iexact=title.strip()).count()
            if matching_literature_count > 0:
                errors['title'] = ['This literature is already exist.']

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


class UPDATELiteratureSerializer(BaseSerializer):
    class Meta:
        model = Literature
        fields = ['title', 'sectId', 'order', 'body', 'isVerified', 'isActive']

    def to_internal_value(self, data):
        sect_id = data.get('sectId')
        title = data.get('title')
        errors = {}

        # custom validation
        if sect_id:
            try:
                MstSect.objects.get(id=sect_id)
            except MstSect.DoesNotExist:
                errors['sectId'] = ['Invalid Sect Id.']
            except ValueError:
                errors['sectId'] = [f"'sectId' excepted a number but got '{sect_id}."]

        if title:
            literature_id = self.context.get('literature_id')
            matching_literature_count = Literature.objects.filter(Q(title__iexact=title), ~Q(id=literature_id),).count()
            if matching_literature_count > 0:
                errors['title'] = ['This literature is already exist.']
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


class GETLiteratureByIdSerializer(serializers.ModelSerializer):
    sectName = serializers.CharField(source='sectId.sectName')

    class Meta:
        model = Literature
        fields = ['id', 'sectId', 'sectName', 'title', 'order', 'body', 'isVerified', 'isActive']


class GETLiteratureForAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Literature
        fields = ['id', 'title', 'body']
