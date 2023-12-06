from django.db.models import Q
from rest_framework import serializers
from jdcApi.models import Literature, MstSect
from accounts.models import User


class GETAllSectWithCountForLiteratureSerializer(serializers.ModelSerializer):
    count = serializers.SerializerMethodField()

    class Meta:
        model = MstSect
        fields = ['id', 'sectName', 'count']

    def get_count(self, instance):
        return Literature.objects.filter(isActive=True, isVerified=True, sectId=instance.id).count()


class GETLiteratureSerializer(serializers.ModelSerializer):
    uploadedBy = serializers.SerializerMethodField()

    class Meta:
        model = Literature
        fields = ['id', 'title', 'uploadedBy']

    def get_uploadedBy(self, instance):
        try:
            user_obj = User.objects.get(id=instance.createdBy)
            return user_obj.name
        except User.DoesNotExist:
            return ""


class CREATELiteratureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Literature
        fields = ['title', 'sectId', 'order', 'body']

    def create(self, validated_data):
        validated_data['title'] = validated_data['title'].capitalize()
        # Create the user instance with modified data
        state_obj = self.Meta.model.objects.create(**validated_data)

        #  add data in field createdBy
        user_id_by_token = self.context.get('user_id_by_token')
        state_obj.createdBy = user_id_by_token
        state_obj.save()

        return state_obj

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


class UPDATELiteratureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Literature
        fields = ['title', 'sectId', 'order', 'body', 'isVerified', 'isActive']

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
