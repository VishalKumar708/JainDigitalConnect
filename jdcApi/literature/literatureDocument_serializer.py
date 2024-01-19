from django.core.exceptions import ValidationError
from django.db.models import Q
from rest_framework import serializers
from jdcApi.models import MstSect, LiteratureDocument
from accounts.models import User
from django.core.validators import URLValidator
import base64
from django.core.files.uploadedfile import UploadedFile
from utils.base_serializer import BaseSerializer


class CREATENewLiteratureDocumentSerializer(BaseSerializer):
    title = serializers.CharField(required=True)

    class Meta:
        fields = ['sectId', 'title', 'order', 'link', 'file']
        model = LiteratureDocument

    def to_internal_value(self, data):
        link = data.get('link')
        file = data.get('file')
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

        if link:
            try:
                validator = URLValidator()
                validator(link.strip())
            except ValidationError:
                errors['link'] = ["Invalid Link."]

        if file and not isinstance(file, UploadedFile):
            errors['file'] = ["Invalid File Data."]
            # print("file name==> ", file.name)
            # print("file==> ", file)
            # print("file content_type==> ", file.content_type)
            # print("file size==> ", file.size)

        if not link and not file:
            # raise serializers.ValidationError("Please provide either 'link' or 'file'.")
            errors['link'] = ["Please provide either 'link' or 'file'."]
            errors['file'] = ["Please provide either 'file' or 'link'."]

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


class UPDATELiteratureDocumentByIdSerializer(BaseSerializer):
    title = serializers.CharField(required=True)

    class Meta:
        fields = ['sectId', 'title', 'order', 'link', 'file', 'isVerified', 'isActive']
        model = LiteratureDocument

    def to_internal_value(self, data):
        link = data.get('link')
        file = data.get('file')
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

        if link:
            try:
                validator = URLValidator()
                validator(link.strip())
            except ValidationError:
                errors['link'] = ["Invalid Link."]

        if file and not isinstance(file, UploadedFile):
            errors['file'] = ["Invalid File Data."]
            # print("file name==> ", file.name)
            # print("file==> ", file)
            # print("file content_type==> ", file.content_type)
            # print("file size==> ", file.size)

        if not link and not file:
            # raise serializers.ValidationError("Please provide either 'link' or 'file'.")
            errors['link'] = ["Please provide either 'link' or 'file'."]
            errors['file'] = ["Please provide either 'file' or 'link'."]

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


class GETLiteratureDocumentDetailsSerializer(serializers.ModelSerializer):
    # file = serializers.SerializerMethodField()
    title = serializers.CharField(required=True)

    class Meta:
        fields = ['id', 'sectId', 'title', 'order', 'link', 'file', 'isVerified', 'isActive']
        model = LiteratureDocument

    # def get_file(self, obj):
    #     try:
    #         with open(obj.file.path, 'rb') as file:
    #             file_content = file.read()
    #             return base64.b64encode(file_content).decode('utf-8')
    #     except FileNotFoundError:
    #         return None


class GETAllSectWithCountForLiteratureDocumentSerializer(serializers.ModelSerializer):
    count = serializers.IntegerField()

    class Meta:
        model = MstSect
        fields = ['id', 'sectName', 'count']



class GETAllLiteratureDocumentSerializer(serializers.ModelSerializer):
    file = serializers.SerializerMethodField()
    title = serializers.CharField(required=True)

    class Meta:
        fields = ['id', 'title', 'sectId', 'order', 'link', 'file', 'isVerified', 'isActive']
        model = LiteratureDocument


class GETAllActiveLiteratureDocumentSerializer(serializers.ModelSerializer):
    uploadedBy = serializers.CharField(source='createdBy.name')

    class Meta:
        fields = ['id', 'title', 'link', 'file', 'uploadedBy']
        model = LiteratureDocument




