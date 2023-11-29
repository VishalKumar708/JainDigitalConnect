# from django.db.models import Q
from rest_framework import serializers
from jdcApi.models import MstSect, Saint
from datetime import datetime


class GETAllSectWithCountForSaintSerializer(serializers.ModelSerializer):
    count = serializers.SerializerMethodField()

    class Meta:
        model = MstSect
        fields = ['id', 'sectName', 'count']

    def get_count(self, sect):
        # print('sect ==> ', sect)
        # Calculate the count of records in the 'Saint' model based on the 'Sect' field
        return Saint.objects.filter(sectId=sect.id).count()


class CREATESaintSerializer(serializers.ModelSerializer):
    dob = serializers.DateTimeField(input_formats=['%B %d, %Y'])  # according to 12hr clock to send default time 12:00 AM
    dobTime = serializers.TimeField(input_formats=['%I:%M %p'], allow_null=True)
    dikshaDate = serializers.DateField(input_formats=['%B %d, %Y'])
    devlokDate = serializers.DateTimeField(input_formats=['%B %d, %Y'], required=False, allow_null=True)
    devlokTime = serializers.TimeField(input_formats=['%I:%M %p'], allow_null=True, required=False)

    class Meta:
        model = Saint
        fields = ['name', 'sectId', 'fatherName', 'motherName', 'birthPlace', 'dikshaPlace', 'guruName','dob', 'dobTime', 'dikshaDate', 'devlokDate', 'devlokTime', 'gender', 'description']

    def to_internal_value(self, data):
        sect_id = data.get('sectId')
        dob = data.get('dob')
        devlok_date = data.get('devlokDate')
        diksha_date = data.get('dikshaDate')
        errors = {}
        if sect_id:
            try:
                MstSect.objects.get(id=sect_id)
            except MstSect.DoesNotExist:
                errors['sectId'] = ['Invalid Sect Id.']
            except ValueError:
                errors['sectId'] = [f"'sectId' excepted a number but got '{sect_id}."]

        if dob and devlok_date:
            try:
                # Compare 'devlok_date' less than 'dob' and 'diksha_date'
                if datetime.strptime(devlok_date, '%B %d, %Y') < datetime.strptime(dob, '%B %d, %Y') or (diksha_date and datetime.strptime(devlok_date, '%B %d, %Y') < datetime.strptime(diksha_date, '%B %d, %Y')):
                    errors['devlokDate'] = [f"'Devlok Date' must be greater than 'Birth Date' and 'Diksha Date'."]
            except ValueError:
                pass

        if dob and diksha_date:
            try:
                #  compare if 'diksha_date' is greater than 'dob' and less than 'devlok_date'
                if datetime.strptime(diksha_date, '%B %d, %Y') < datetime.strptime(dob, '%B %d, %Y') or (diksha_date and datetime.strptime(diksha_date, '%B %d, %Y') > datetime.strptime(devlok_date, '%B %d, %Y')):
                    errors['dikshaDate'] = [f"'Diksha Date' must be greater than 'Birth Date' and less then 'Devlok Date'."]
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

    def create(self, validated_data):

        try:
            validated_data['name'] = validated_data['name'].title()
            validated_data['fatherName'] = validated_data['fatherName'].title()
            validated_data['motherName'] = validated_data['motherName'].title()
            validated_data['guruName'] = validated_data['guruName'].title()
            validated_data['birthPlace'] = validated_data['birthPlace'].title()
        except ValueError:
            pass
        # Create the user instance with modified data
        saint_obj = self.Meta.model.objects.create(**validated_data)

        #  add data in field createdBy
        user_id_by_token = self.context.get('user_id_by_token')
        saint_obj.createdBy = user_id_by_token
        saint_obj.save()

        return saint_obj


class UPDATESaintSerializer(serializers.ModelSerializer):
    dob = serializers.DateField(input_formats=['%B %d, %Y'])
    dikshaDate = serializers.DateField(input_formats=['%B %d, %Y'])
    devlokDate = serializers.DateField(input_formats=['%B %d, %Y'],  allow_null=True)
    dobTime = serializers.TimeField(input_formats=['%I:%M %p'], allow_null=True)
    devlokTime = serializers.TimeField(input_formats=['%I:%M %p'], allow_null=True)

    class Meta:
        model = Saint
        fields = ['name', 'sectId', 'fatherName', 'motherName', 'birthPlace', 'dikshaPlace', 'guruName','dob', 'dobTime', 'dikshaDate', 'devlokDate','devlokTime', 'gender', 'description', 'isVerified']

    def update(self, instance, validated_data):
        # Update the user instance with modified data
        if validated_data.get('name'):
            validated_data['name'] = validated_data['name'].title()
        if validated_data.get('fatherName'):
            validated_data['fatherName'] = validated_data['fatherName'].title()
        if validated_data.get('motherName'):
            validated_data['motherName'] = validated_data['motherName'].title()
        if validated_data.get('guruName'):
            validated_data['guruName'] = validated_data['guruName'].title()
        if validated_data.get('birthPlace'):
            validated_data['birthPlace'] = validated_data['birthPlace'].title()

        user_id_by_token = self.context.get('user_id_by_token')
        validated_data['updatedBy'] = user_id_by_token
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

    def to_internal_value(self, data):
        updated_fields = {key: value for key, value in data.items() if key in self.Meta.fields}
        if len(updated_fields) < 1:
            raise serializers.ValidationError(
                {'update_validation_error': "At least one field must be provided for the update."})

        sect_id = data.get('sectId')
        errors = {}
        dob = data.get('dob')
        devlok_date = data.get('devlokDate')
        diksha_date = data.get('dikshaDate')

        if sect_id:
            try:
                MstSect.objects.get(id=sect_id)
            except MstSect.DoesNotExist:
                errors['sectId'] = ['Invalid Sect Id.']
            except ValueError:
                errors['sectId'] = [f"'sectId' excepted a number but got '{sect_id}."]

        if dob and devlok_date:
            try:
                # Compare 'devlok_date' less than 'dob' and 'diksha_date'
                if datetime.strptime(devlok_date, '%B %d, %Y') < datetime.strptime(dob, '%B %d, %Y') or (diksha_date and datetime.strptime(devlok_date, '%B %d, %Y') < datetime.strptime(diksha_date, '%B %d, %Y')):
                    errors['devlokDate'] = [f"'Devlok Date' must be greater than 'Birth Date' and 'Diksha Date'."]
            except ValueError:
                pass

        if dob and diksha_date:
            try:
                #  compare if 'diksha_date' is greater than 'dob' and less than 'devlok_date'
                if datetime.strptime(diksha_date, '%B %d, %Y') < datetime.strptime(dob, '%B %d, %Y') or (diksha_date and datetime.strptime(diksha_date, '%B %d, %Y') > datetime.strptime(devlok_date, '%B %d, %Y')):
                    errors['dikshaDate'] = [f"'Diksha Date' must be greater than 'Birth Date' and less then 'Devlok Date'."]
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


# for search Saint
class GETAllSaintSerializer(serializers.ModelSerializer):
    dikshaDate = serializers.SerializerMethodField()

    class Meta:
        model = Saint
        fields = ['id', 'name', 'birthPlace', 'dikshaPlace', 'dikshaDate']

    def get_dikshaDate(self, saint):
        return saint.dikshaDate.strftime("%B %d, %Y")


class GETAllSaintBySectIdSerializer(serializers.ModelSerializer):
    dikshaDate = serializers.SerializerMethodField()
    dob = serializers.SerializerMethodField()

    class Meta:
        model = Saint
        fields = ['id', 'name', 'dob', 'birthPlace', 'dikshaPlace', 'dikshaDate']

    def get_dikshaDate(self, instance):
        return instance.dikshaDate.strftime("%B %d, %Y")

    def get_dob(self, instance):
        return instance.dob.strftime("%B %d, %Y")


class GETAllSaintForAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Saint
        fields = ['id', 'name']


class GETSaintByIdSerializer(serializers.ModelSerializer):
    sect = serializers.CharField(source='sectId.sectName', read_only=True)
    dob = serializers.SerializerMethodField()
    devlokDate = serializers.SerializerMethodField()
    dikshaDate = serializers.SerializerMethodField()
    age = serializers.SerializerMethodField()
    dobTime = serializers.SerializerMethodField()
    devlokTime = serializers.SerializerMethodField()

    class Meta:
        model = Saint
        fields = ['id', 'name', 'sect','sectId', 'fatherName', 'motherName', 'birthPlace', 'dikshaPlace', 'guruName', 'age', 'dikshaDate','devlokDate', 'devlokTime', 'gender', 'dob', 'dobTime', 'dobTime', 'description']

    def get_age(self, instance):
        dob = instance.dob
        #  to find the age by using 'dob'
        birthdate = datetime.strptime(str(dob), '%Y-%m-%d')
        current_date = instance.devlokDate if instance.devlokDate else datetime.now()
        # Calculate the age
        age = current_date.year - birthdate.year - (
                (current_date.month, current_date.day) < (birthdate.month, birthdate.day))

        return age

    def get_dikshaDate(self, instance):
        return instance.dikshaDate.strftime("%B %d, %Y")

    def get_dob(self, instance):
        return instance.dob.strftime("%B %d, %Y")

    def get_dobTime(self, instance):
        dob_time = instance.dobTime
        return dob_time.strftime('%I:%M %p') if dob_time else ""

    def get_devlokDate(self, instance):
        dob_time = instance.devlokDate
        return dob_time.strftime("%B %d, %Y") if dob_time else ""
    def get_devlokTime(self, instance):
        devlok_time = instance.devlokTime

        return devlok_time.strftime('%I:%M %p') if devlok_time else ""


