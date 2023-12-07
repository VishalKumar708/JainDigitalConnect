
from rest_framework import serializers
from jdcApi.models import DharamSthanHistory, DharamSthan
from django.utils import timezone
from datetime import datetime


class CREATEDharamSthanHistorySerializer(serializers.ModelSerializer):
    startDate = serializers.DateField(input_formats=("%d %B %Y",))
    endDate = serializers.DateField(input_formats=("%d %B %Y",))

    class Meta:
        model = DharamSthanHistory
        fields = ['dharamSthanId', "year", 'startDate', 'endDate', 'title', 'body', 'isActive']

    def create(self, validated_data):
        validated_data['title'] = validated_data['title'].title()
        # Create the user instance with modified data
        obj = self.Meta.model.objects.create(**validated_data)
        #  add data in field createdBy
        user_id_by_token = self.context.get('user_id_by_token')
        obj.createdBy = user_id_by_token
        obj.save()
        return obj

    def to_internal_value(self, data):
        dharam_sthan_id = data.get('dharamSthanId')
        year = data.get('year')
        startDate = data.get('startDate')
        endDate = data.get('endDate')
        errors = {}
        # custom validation
        if dharam_sthan_id:
            try:
                DharamSthan.objects.get(id=dharam_sthan_id)
            except DharamSthan.DoesNotExist:
                errors['dharamSthanId'] = ["Invalid Id."]
            except ValueError:
                errors['dharamSthanId'] = [f"excepted a number but got '{dharam_sthan_id}'."]

        if year:
            try:
                current_year = timezone.now().year
                if int(year) > current_year:
                    errors['year'] = [f"Year must be '{current_year}' or earlier"]
            except ValueError:
                pass

        if startDate and endDate:
            try:
                if year and datetime.strptime(startDate, "%d %B %Y").year != int(year):
                    errors['startDate'] = [f"startDate 'year' must be equal to your selected year '{year}'."]
                else:
                    if datetime.strptime(endDate, "%d %B %Y") < datetime.strptime(startDate, "%d %B %Y"):
                        errors['endDate'] = [f"This date must be later than the start date '{startDate}'."]
            except ValueError:
                pass
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

        return validated_data


class UPDATEDharamSthanHistorySerializer(serializers.ModelSerializer):
    startDate = serializers.DateField(input_formats=("%d %B %Y",))
    endDate = serializers.DateField(input_formats=("%d %B %Y",))

    class Meta:
        model = DharamSthanHistory
        fields = ['dharamSthanId', "year", 'startDate', 'endDate', 'title', 'body', 'isActive']

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
        dharam_sthan_id = data.get('dharamSthanId')
        year = data.get('year')
        startDate = data.get('startDate')
        endDate = data.get('endDate')
        errors = {}
        # custom validation
        if dharam_sthan_id:
            try:
                DharamSthan.objects.get(id=dharam_sthan_id)
            except DharamSthan.DoesNotExist:
                errors['dharamSthanId'] = ["Invalid Id."]
            except ValueError:
                errors['dharamSthanId'] = [f"excepted a number but got '{dharam_sthan_id}'."]

        if year:
            try:
                current_year = timezone.now().year
                if int(year) > current_year:
                    errors['year'] = [f"Year must be '{current_year}' or earlier"]
            except ValueError:
                pass

        if startDate and endDate:
            try:
                if year and datetime.strptime(startDate, "%d %B %Y").year != int(year):
                    errors['startDate'] = [f"startDate 'year' must be equal to your selected year '{year}'."]
                else:
                    if datetime.strptime(endDate, "%d %B %Y") < datetime.strptime(startDate, "%d %B %Y"):
                        errors['endDate'] = [f"This date must be later than the start date '{startDate}'."]
            except ValueError:
                pass
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

        return validated_data


class GETDharamSthanHistoryDetialsSerializer(serializers.ModelSerializer):

    class Meta:
        model = DharamSthanHistory
        fields = ['id', 'dharamSthanId', "year", 'startDate', 'endDate', 'title', 'body', 'isActive']


class GETAllDharamSthanHistorySerializer(serializers.ModelSerializer):

    class Meta:
        model = DharamSthanHistory
        fields = ['id', 'title', "year", 'body', 'isActive']