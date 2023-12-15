from django.core.exceptions import ValidationError
from django.db.models import Q
from rest_framework import serializers
from jdcApi.models import MstSect, LiteratureDocument
from accounts.models import User
from django.core.validators import URLValidator
import base64
from django.core.files.uploadedfile import UploadedFile


class CREATENewLiteratureDocumentSerializer(serializers.ModelSerializer):
    title = serializers.CharField(required=True)

    class Meta:
        fields = ['sectId', 'title', 'order', 'link', 'file']
        model = LiteratureDocument

    def create(self, validated_data):
        # Create the user instance with modified data
        obj = self.Meta.model.objects.create(**validated_data)

        #  add data in field createdBy
        user_id_by_token = self.context.get('user_id_by_token')
        obj.createdBy = user_id_by_token
        obj.save()

        return obj

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


class UPDATELiteratureDocumentByIdSerializer(serializers.ModelSerializer):
    title = serializers.CharField(required=True)

    class Meta:
        fields = ['sectId', 'title', 'order', 'link', 'file', 'isVerified', 'isActive']
        model = LiteratureDocument

    def update(self, instance, validated_data):
        # Update the user instance with modified data
        if validated_data.get('title'):
            validated_data['title'] = validated_data['title'].title()

        user_id_by_token = self.context.get('user_id_by_token')
        validated_data['updatedBy'] = user_id_by_token
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

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
    count = serializers.SerializerMethodField()

    class Meta:
        model = MstSect
        fields = ['id', 'sectName', 'count']

    def get_count(self, instance):
        return LiteratureDocument.objects.filter(isActive=True, isVerified=True, sectId=instance.id).count()


class GETAllLiteratureDocumentSerializer(serializers.ModelSerializer):
    file = serializers.SerializerMethodField()
    title = serializers.CharField(required=True)

    class Meta:
        fields = ['id', 'title', 'sectId', 'order', 'link', 'file', 'isVerified', 'isActive']
        model = LiteratureDocument


class GETAllActiveLiteratureDocumentSerializer(serializers.ModelSerializer):
    uploadedBy = serializers.SerializerMethodField()

    class Meta:
        fields = ['id', 'title', 'link', 'file', 'uploadedBy']
        model = LiteratureDocument

    def get_uploadedBy(self, instance):
        try:
            obj = User.objects.get(id=instance.createdBy)
            return obj.name
        except User.DoesNotExist:
            return ""




