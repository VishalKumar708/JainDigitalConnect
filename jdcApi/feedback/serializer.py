from rest_framework import serializers
from jdcApi.models import MstFeedbackTitle, Aarti, Feedback
from datetime import date, datetime
from accounts.models import User


class CREATEFeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = ['feedbackTitleId', 'body']

    def create(self, validated_data):

        obj = self.Meta.model.objects.create(**validated_data)

        #  add data in field createdBy
        user_id_by_token = self.context.get('user_id_by_token')
        obj.createdBy = user_id_by_token
        obj.save()

        return obj

    def to_internal_value(self, data):
        feedbackTitle_id = data.get('feedbackTitleId')
        errors = {}
        # custom validation
        if feedbackTitle_id:
            try:
                MstFeedbackTitle.objects.get(id=feedbackTitle_id)
            except MstFeedbackTitle.DoesNotExist:
                errors['feedbackTitleId'] = ['Invalid feedbackTitle Id.']
            except ValueError:
                errors['feedbackTitleId'] = [f"'feedbackTitleId' excepted a number but got '{feedbackTitle_id}."]

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


class UPDATEFeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = ['feedbackTitleId', 'body']

    def update(self, instance, validated_data):

        user_id_by_token = self.context.get('user_id_by_token')
        validated_data['updatedBy'] = user_id_by_token
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

    def to_internal_value(self, data):
        feedbackTitle_id = data.get('feedbackTitleId')
        errors = {}
        # custom validation
        if feedbackTitle_id:
            try:
                MstFeedbackTitle.objects.get(id=feedbackTitle_id)
            except MstFeedbackTitle.DoesNotExist:
                errors['feedbackTitleId'] = ['Invalid feedbackTitle Id.']
            except ValueError:
                errors['feedbackTitleId'] = [f"'feedbackTitleId' excepted a number but got '{feedbackTitle_id}."]

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


class GETFeedbackDetailsSerializer(serializers.ModelSerializer):
    title = serializers.CharField(source='feedbackTitleId.title')

    class Meta:
        model = Feedback
        fields = ['id', 'title', 'body']


class GETAllFeedbackForAdminSerializer(serializers.ModelSerializer):
    title = serializers.CharField(source='feedbackTitleId.title')
    postedDate = serializers.SerializerMethodField()
    postedTime = serializers.SerializerMethodField()
    uploadedBy = serializers.SerializerMethodField()

    class Meta:
        model = Feedback
        fields = ['id', 'title', 'postedDate', 'postedTime', 'uploadedBy']

    def get_postedDate(self, instance):
        return instance.createdDate.strftime("%d %B, %Y")

    def get_postedTime(self, instance):
        return instance.createdDate.strftime("%I:%M %p")

    def get_uploadedBy(self, instance):
        try:
            user_obj = User.objects.get(id=instance.createdBy)
            return user_obj.name
        except User.DoesNotExist:
            return ""
