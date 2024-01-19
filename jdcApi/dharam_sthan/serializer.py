from django.db.models import Q
from rest_framework import serializers
from jdcApi.models import DharamSthan, City
from datetime import date, datetime
from utils.base_serializer import BaseSerializer
from masterApi.models import MstSect


class GETAllSectWithCountForDharamSthanSerializer(serializers.ModelSerializer):
    count = serializers.IntegerField()

    class Meta:
        model = MstSect
        fields = ['id', 'sectName', 'count']


class GETAllCityWithCountForDharamSthanSerializer(serializers.ModelSerializer):
    count = serializers.IntegerField()

    class Meta:
        model = City
        fields = ['cityId', 'cityName', 'count']


class SearchCitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ['cityId', 'cityName']


class CREATEDharamSthanSerializer(BaseSerializer):
    foundationDate = serializers.DateField(input_formats=("%d %B, %Y",))

    class Meta:
        model = DharamSthan
        fields = ['name', 'cityId', 'sectId', 'address', 'locationLink', 'postalCode', 'foundationDate', 'accountNumber', 'ifscCode', 'upiId']

    def to_internal_value(self, data):
        dharam_sthan_name = data.get('name')
        sect_id = data.get('sectId')
        city_id = data.get('cityId')
        foundation_date = data.get('foundationDate')
        postal_code = data.get('postalCode')

        errors = {}
        # custom validation
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
                errors['cityId'] = [f"'cityId' excepted a number but got '{city_id}."]

        if dharam_sthan_name:
            matching_dharam_sthan_count = DharamSthan.objects.filter(name__iexact=dharam_sthan_name.strip()).count()
            if matching_dharam_sthan_count > 0:
                errors['name'] = [f"{dharam_sthan_name} is already exist."]

        if postal_code:
            if not str(postal_code).isdigit() or len(str(postal_code).strip()) != 6:
                errors['postalCode'] = ["Please Enter Valid Pincode."]

        if foundation_date:
            today_date = date.today()

            try:
                # parsed_foundation_date = datetime.strptime(foundation_date, "%d %B %Y").date()

                if today_date < datetime.strptime(foundation_date, "%d %B, %Y").date():
                    errors['foundationDate'] = ["Foundation date must be in the past."]
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


class UPDATEDharamSthanSerializer(BaseSerializer):
    foundationDate = serializers.DateField(input_formats=("%d %B, %Y",))

    class Meta:
        model = DharamSthan
        fields = ['name', 'cityId', 'sectId', 'address', 'locationLink', 'postalCode', 'foundationDate',
                  'accountNumber', 'ifscCode', 'upiId', 'isVerified', 'isActive']

    def to_internal_value(self, data):
        dharam_sthan_name = data.get('name')
        sect_id = data.get('sectId')
        city_id = data.get('cityId')
        foundation_date = data.get('foundationDate')
        postal_code = data.get('postalCode')

        errors = {}
        # custom validation
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
                errors['cityId'] = [f"'cityId' excepted a number but got '{city_id}."]

        if dharam_sthan_name:
            matching_dharam_sthan_count = DharamSthan.objects.filter(Q(name__iexact=dharam_sthan_name.strip()), ~Q(id=self.context.get('dharam_sthan_id'))).count()
            if matching_dharam_sthan_count > 0:
                errors['name'] = [f"{dharam_sthan_name} is already exist."]

        if postal_code:
            if not str(postal_code).isdigit() or len(str(postal_code).strip()) != 6:
                errors['postalCode'] = ["Please Enter Valid Pincode."]

        if foundation_date:
            today_date = date.today()

            try:
                # parsed_foundation_date = datetime.strptime(foundation_date, "%d %B %Y").date()

                if today_date < datetime.strptime(foundation_date, "%d %B, %Y").date():
                    errors['foundationDate'] = ["Foundation date must be in the past."]
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


class GETDharamSthanDetailsSerializer(serializers.ModelSerializer):
    foundationDate = serializers.SerializerMethodField()
    sectName = serializers.CharField(source='sectId.sectName', read_only=True)

    class Meta:
        model = DharamSthan
        fields = ['id', 'name', 'cityId', 'sectId', 'sectName', 'address', 'locationLink', 'postalCode', 'foundationDate',
                  'accountNumber', 'ifscCode', 'upiId', 'isVerified', 'isActive']

    def get_foundationDate(self, instance):
        return instance.foundationDate.strftime("%d %B, %Y")


class GETAllDharamSthanSerializer(serializers.ModelSerializer):
    foundationDate = serializers.SerializerMethodField()
    sectName = serializers.CharField(source='sectId.sectName', read_only=True)
    uploadedBy = serializers.CharField(source='createdBy.name', read_only=True)

    class Meta:
        model = DharamSthan
        fields = ['id', 'name', 'foundationDate', 'postalCode', 'sectName', 'address', 'accountNumber', 'ifscCode',
                  'upiId', 'locationLink', 'uploadedBy']

    def get_foundationDate(self, instance):
        return instance.foundationDate.strftime("%d %B, %Y")


class SearchDharamSthanSerializer(serializers.ModelSerializer):
    foundationDate = serializers.SerializerMethodField()

    class Meta:
        model = DharamSthan
        fields = ['id', 'name', 'foundationDate', 'postalCode', 'address',  'locationLink']

    def get_foundationDate(self, instance):
        return instance.foundationDate.strftime("%d %B, %Y")


class GETAllDharamSthanForAdminSerializer(serializers.ModelSerializer):
    foundationDate = serializers.SerializerMethodField()

    class Meta:
        model = DharamSthan
        fields = ['id', 'name', 'foundationDate', 'postalCode', 'address', 'locationLink']

    def get_foundationDate(self, instance):
        return instance.foundationDate.strftime("%d %B, %Y")


class GETAllCityWithCountForDharamSthanForAdminSerializer(serializers.ModelSerializer):
    count = serializers.IntegerField()

    class Meta:
        model = City
        fields = ['cityId', 'cityName', 'count']

