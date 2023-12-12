

from rest_framework import serializers
from jdcApi.models import MstSect, DharamSthanHistory, DharamSthan, LiveLocation
from django.utils import timezone
from datetime import datetime
from accounts.models import User

class GETAllSectWithCountForDharamSthanHistorySerializer(serializers.ModelSerializer):
    count = serializers.SerializerMethodField()

    class Meta:
        fields = ['id', 'sectName', 'count']
        model = MstSect

    def get_count(self, instance):
        current_year = timezone.now().year
        count = DharamSthanHistory.objects.filter(
            isActive=True,
            dharamSthanId__isActive=True,
            dharamSthanId__isVerified=True,
            dharamSthanId__sectId=instance.id,
            year=current_year
        ).count()
        return count


class GETAllSectForLiveLocationSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ['id', 'sectName']
        model = MstSect




class GETAllDharamSthanHistorySerializer(serializers.ModelSerializer):

    class Meta:
        model = DharamSthanHistory
        fields = ['id', 'dharamSthanId', 'title', "year", 'body', 'isActive']


class GETDharamSthanDetailsSerializer(serializers.ModelSerializer):

    class Meta:
        model = DharamSthan
        fields = ['name', 'foundationDate', 'postalCode', 'address', 'locationLink']


#  Live Location Serializer
class CREATENewLiveLocationSerializer(serializers.ModelSerializer):
    startDate = serializers.DateField(input_formats=('%d %B %Y',))
    endDate = serializers.DateField(input_formats=('%d %B %Y',))

    class Meta:
        fields = ['sectId', 'title', 'person1Name', 'phoneNumber1', 'person2Name', 'phoneNumber2', 'startDate',
                    'endDate', 'locationLink', 'address', 'description']
        model = LiveLocation

    def create(self, validated_data):
        validated_data['title'] = validated_data['title'].title()
        if validated_data.get('person1Name'):
            validated_data['person1Name'] = validated_data['person1Name'].title()

        if validated_data.get('person2Name'):
            validated_data['person2Name'] = validated_data['person2Name'].title()
        # Create the user instance with modified data
        state_obj = self.Meta.model.objects.create(**validated_data)

        #  add data in field createdBy
        user_id_by_token = self.context.get('user_id_by_token')
        state_obj.createdBy = user_id_by_token
        state_obj.save()

        return state_obj

    def to_internal_value(self, data):
        phoneNumber1 = data.get('phoneNumber1')
        phoneNumber2 = data.get('phoneNumber2')
        startDate = data.get('startDate')
        endDate = data.get('endDate')

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

        if phoneNumber1:
            if not str(phoneNumber1).strip().isdigit() and len(str(phoneNumber1).strip()) != 10:
                errors['phoneNumber1'] = ["Please Enter Valid PhoneNumber!"]

        if phoneNumber2:
            if not str(phoneNumber2).strip().isdigit() and len(str(phoneNumber2).strip()) != 10:
                errors['phoneNumber2'] = ["Please Enter Valid PhoneNumber!"]

        if startDate:
            try:
                current_date = timezone.now().date()
                print(current_date)
                if datetime.strptime(startDate, "%d %B %Y").date() < current_date :
                    errors['startDate'] = ["Date should be today or a date in the future."]
            except ValueError:
                pass

        if endDate:
            try:
                current_date = timezone.now().date()
                if datetime.strptime(endDate, "%d %B %Y").date() < current_date :
                    errors['endDate'] = ["Date should be today or a date in the future."]
            except ValueError:
                pass

        if startDate and endDate:
            try:
                if datetime.strptime(endDate, "%d %B %Y") < datetime.strptime(startDate, "%d %B %Y"):
                    errors['endDate'] = [f"This date must be later than the 'start date'."]
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


class UPDATELiveLocationSerializer(serializers.ModelSerializer):
    startDate = serializers.DateField(input_formats=('%d %B %Y',))
    endDate = serializers.DateField(input_formats=('%d %B %Y',))

    class Meta:
        fields = ['sectId', 'title', 'person1Name', 'phoneNumber1', 'person2Name', 'phoneNumber2', 'startDate',
                    'endDate', 'locationLink', 'address', 'description', 'isVerified', 'isActive']
        model = LiveLocation

    def update(self, instance, validated_data):
        # Update the user instance with modified data
        if validated_data.get('title'):
            validated_data['title'] = validated_data['title'].title()

        if validated_data.get('person1Name'):
            validated_data['person1Name'] = validated_data['person1Name'].title()

        if validated_data.get('person2Name'):
            validated_data['person2Name'] = validated_data['person2Name'].title()

        user_id_by_token = self.context.get('user_id_by_token')
        validated_data['updatedBy'] = user_id_by_token
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

    def to_internal_value(self, data):
        phoneNumber1 = data.get('phoneNumber1')
        phoneNumber2 = data.get('phoneNumber2')
        startDate = data.get('startDate')
        endDate = data.get('endDate')

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

        if phoneNumber1:
            if not str(phoneNumber1).strip().isdigit() and len(str(phoneNumber1).strip()) != 10:
                errors['phoneNumber1'] = ["Please Enter Valid PhoneNumber!"]

        if phoneNumber2:
            if not str(phoneNumber2).strip().isdigit() and len(str(phoneNumber2).strip()) != 10:
                errors['phoneNumber2'] = ["Please Enter Valid PhoneNumber!"]

        if startDate:
            try:
                current_date = timezone.now().date()
                print(current_date)
                if datetime.strptime(startDate, "%d %B %Y").date() < current_date :
                    errors['startDate'] = ["Date should be today or a date in the future."]
            except ValueError:
                pass

        if endDate:
            try:
                current_date = timezone.now().date()
                if datetime.strptime(endDate, "%d %B %Y").date() < current_date :
                    errors['endDate'] = ["Date should be today or a date in the future."]
            except ValueError:
                pass

        if startDate and endDate:
            try:
                if datetime.strptime(endDate, "%d %B %Y") < datetime.strptime(startDate, "%d %B %Y"):
                    errors['endDate'] = [f"This date must be later than the 'start date'."]
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


class GETLiveLocationDetailByIdSerializer(serializers.ModelSerializer):
    startDate = serializers.SerializerMethodField()
    endDate = serializers.SerializerMethodField()

    class Meta:
        fields = ['id', 'sectId', 'title', 'person1Name', 'phoneNumber1', 'person2Name', 'phoneNumber2', 'startDate',
                    'endDate', 'locationLink', 'address', 'description', 'isVerified', 'isActive']
        model = LiveLocation

    def get_startDate(self,instance):
        return instance.startDate.strftime('%d %B %Y')

    def get_endDate(self, instance):
        return instance.endDate.strftime('%d %B %Y')


class GETAllLiveLocationByUserIdSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ['id',  'title']
        model = LiveLocation


class GETAllLiveLocationBySectIdSerializer(serializers.ModelSerializer):
    uploadedBy = serializers.SerializerMethodField()

    class Meta:
        fields = ['id', 'title', 'description', 'uploadedBy']
        model = LiveLocation

    def get_uploadedBy(self,instance):
        try:
            user_obj = User.objects.get(id=instance.createdBy)
            return user_obj.name
        except User.DoesNotExist:
            return ""
