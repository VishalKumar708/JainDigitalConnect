from rest_framework import serializers
from jdcApi.models import Event, MstSect, City
from datetime import date, datetime
from accounts.models import User
from utils.base_serializer import BaseSerializer


class CREATEEventSerializer(BaseSerializer):
    startDate = serializers.DateField(input_formats=("%d %B, %Y",))
    endDate = serializers.DateField(input_formats=("%d %B, %Y",))

    class Meta:
        fields = ['cityId', 'sectId', 'startDate', 'endDate', 'title', 'body']
        model = Event

    def to_internal_value(self, data):
        sect_id = data.get('sectId')
        city_id = data.get('cityId')
        start_date = data.get('startDate')
        end_date = data.get('endDate')
        errors = {}
        if sect_id:
            try:
                MstSect.objects.get(id=sect_id)
            except MstSect.DoesNotExist:
                errors['sectId'] = ['Invalid Sect Id.']
            except ValueError:
                errors['sectId'] = [f"'sectId' excepted a number but got '{sect_id}."]
        if city_id:
            try:
                City.objects.get(cityId=city_id)
            except City.DoesNotExist:
                errors['cityId'] = ['Invalid City Id.']
            except ValueError:
                errors['cityId'] = [f"'cityId' excepted a number but got '{sect_id}."]

        if start_date:
            today_date = date.today()
            try:
                if today_date > datetime.strptime(start_date, "%d %B, %Y").date():
                    errors['startDate'] = ["date must be in the today or future."]
            except ValueError:
                pass

        if start_date and end_date:
            try:
                if datetime.strptime(end_date, "%d %B, %Y").date() < datetime.strptime(start_date, "%d %B, %Y").date():
                    errors['endDate'] = ["date must be greater then 'startDate' or equal to 'startDate."]
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
            # print('errors ==> ', errors)
            raise serializers.ValidationError(errors)

        return validated_data


class UPDATEEventSerializer(BaseSerializer):
    startDate = serializers.DateField(input_formats=("%d %B, %Y",))
    endDate = serializers.DateField(input_formats=("%d %B, %Y",))

    class Meta:
        fields = ['cityId', 'sectId', 'startDate', 'endDate', 'title', 'body', 'isVerified', 'isActive']
        model = Event

    def to_internal_value(self, data):
        sect_id = data.get('sectId')
        city_id = data.get('cityId')
        start_date = data.get('startDate')
        end_date = data.get('endDate')
        errors = {}
        if sect_id:
            try:
                MstSect.objects.get(id=sect_id)
            except MstSect.DoesNotExist:
                errors['sectId'] = ['Invalid Sect Id.']
            except ValueError:
                errors['sectId'] = [f"'sectId' excepted a number but got '{sect_id}."]

        if city_id:
            try:
                City.objects.get(cityId=city_id)
            except City.DoesNotExist:
                errors['cityId'] = ['Invalid City Id.']
            except ValueError:
                errors['cityId'] = [f"'cityId' excepted a number but got '{sect_id}."]

        if start_date and end_date:
            try:
                if datetime.strptime(end_date, "%d %B, %Y").date() < datetime.strptime(start_date, "%d %B, %Y").date():
                    errors['endDate'] = ["date must be greater then 'startDate' or equal to 'startDate."]
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
            # print('errors ==> ', errors)
            raise serializers.ValidationError(errors)

        return validated_data


class GETEventDetailsSerializer(serializers.ModelSerializer):
    startDate = serializers.SerializerMethodField()
    endDate = serializers.SerializerMethodField()
    # cityName = serializers.CharField(source='cityId.cityName', read_only=True)
    # sectName = serializers.CharField(source='sectId.sectName', read_only=True)

    class Meta:
        fields = ['id', 'cityId', 'sectId', 'startDate', 'endDate', 'title', 'body', 'isVerified', 'isActive']
        model = Event

    def get_startDate(self, instance):
        return instance.startDate.strftime("%d %B, %Y")

    def get_endDate(self, instance):
        return instance.endDate.strftime("%d %B, %Y")


class GETAllSectWithCountForEventSerializer(serializers.ModelSerializer):
    count = serializers.IntegerField()

    class Meta:
        fields = ['id', 'sectName', 'count']
        model = MstSect


class SearchCitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ['cityId', 'cityName']


class GETAllCityWithCountForEventSerializer(serializers.ModelSerializer):
    count = serializers.IntegerField()

    class Meta:
        model = City
        fields = ['cityId', 'cityName', 'count']


class GETAllActiveEvents(serializers.ModelSerializer):
    uploadedBy = serializers.CharField(source="createdBy.name")

    class Meta:
        fields = ['id', 'title', 'body', 'uploadedBy']
        model = Event


class GETAllEventsForAdmin(serializers.ModelSerializer):
    class Meta:
        fields = ['id', 'title', 'body']
        model = Event
