from django.db.models import Q
from rest_framework import serializers
from jdcApi.models import DharamSthan, MstSect, City
from accounts.models import User
from datetime import date, datetime


class GETAllSectWithCountForDharamSthanSerializer(serializers.ModelSerializer):
    count = serializers.SerializerMethodField()

    class Meta:
        model = MstSect
        fields = ['id', 'sectName', 'count']

    def get_count(self, instance):
        return DharamSthan.objects.filter(isActive=True, isVerified=True, sectId=instance.id).count()


class GETAllCityWithCountForDharamSthanSerializer(serializers.ModelSerializer):
    count = serializers.SerializerMethodField()

    class Meta:
        model = City
        fields = ['cityId', 'cityName', 'count']

    def get_count(self, instance):
        return DharamSthan.objects.filter(isActive=True, isVerified=True, cityId=instance.cityId).count()


class SearchCitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ['cityId', 'cityName']


class GETDharamSthanSerializer(serializers.ModelSerializer):
    uploadedBy = serializers.SerializerMethodField()

    class Meta:
        model = DharamSthan
        fields = ['id', 'aartiName', 'uploadedBy']

    def get_uploadedBy(self, instance):
        try:
            user_obj = User.objects.get(id=instance.createdBy)
            return user_obj.name
        except User.DoesNotExist:
            return ""


class CREATEDharamSthanSerializer(serializers.ModelSerializer):
    foundationDate = serializers.DateField(input_formats=("%d %B %Y",))

    class Meta:
        model = DharamSthan
        fields = ['name', 'cityId', 'sectId', 'address', 'locationLink', 'postalCode', 'foundationDate', 'accountNumber', 'ifscCode', 'upiId']

    def create(self, validated_data):
        validated_data['name'] = validated_data['name'].title()
        # Create the user instance with modified data
        dharam_sthan_obj = self.Meta.model.objects.create(**validated_data)

        #  add data in field createdBy
        user_id_by_token = self.context.get('user_id_by_token')
        dharam_sthan_obj.createdBy = user_id_by_token
        dharam_sthan_obj.save()

        return dharam_sthan_obj

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

                if today_date < datetime.strptime(foundation_date, "%d %B %Y").date():
                    errors['foundationDate'] = ["Foundation date must be in the past."]
            except ValueError:
                errors['foundationDate'] = ["Invalid date format for foundation date."]
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


class UPDATEDharamSthanSerializer(serializers.ModelSerializer):
    foundationDate = serializers.DateField(input_formats=("%d %B %Y",))

    class Meta:
        model = DharamSthan
        fields = ['name', 'cityId', 'sectId', 'address', 'locationLink', 'postalCode', 'foundationDate',
                  'accountNumber', 'ifscCode', 'upiId', 'isVerified', 'isActive']

    def update(self, instance, validated_data):
        # Update the user instance with modified data
        if validated_data.get('name'):
            validated_data['name'] = validated_data['name'].title()

        user_id_by_token = self.context.get('user_id_by_token')
        validated_data['updatedBy'] = user_id_by_token
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

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

                if today_date < datetime.strptime(foundation_date, "%d %B %Y").date():
                    errors['foundationDate'] = ["Foundation date must be in the past."]
            except ValueError:
                errors['foundationDate'] = ["Invalid date format for foundation date."]
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
        return instance.foundationDate.strftime("%d %B %Y")


class GETAllDharamSthanSerializer(serializers.ModelSerializer):
    foundationDate = serializers.SerializerMethodField()
    sectName = serializers.CharField(source='sectId.sectName', read_only=True)
    uploadedBy = serializers.SerializerMethodField()

    class Meta:
        model = DharamSthan
        fields = ['id', 'name', 'foundationDate', 'postalCode', 'sectName', 'address', 'accountNumber', 'ifscCode',
                  'upiId', 'locationLink', 'uploadedBy']

    def get_foundationDate(self, instance):
        return instance.foundationDate.strftime("%d %B %Y")

    def get_uploadedBy(self, instance):
        try:
            obj = User.objects.get(id=instance.createdBy)
            return obj.name
        except User.DoesNotExist:
            return " "


class SearchDharamSthanSerializer(serializers.ModelSerializer):
    foundationDate = serializers.SerializerMethodField()

    class Meta:
        model = DharamSthan
        fields = ['id', 'name', 'foundationDate', 'postalCode', 'address',  'locationLink']

    def get_foundationDate(self, instance):
        return instance.foundationDate.strftime("%d %B %Y")


class GETAllDharamSthanForAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = DharamSthan
        fields = ['id', 'name', 'foundationDate', 'postalCode', 'address', 'locationLink']


class GETAllCityWithCountForDharamSthanForAdminSerializer(serializers.ModelSerializer):
    count = serializers.SerializerMethodField()

    class Meta:
        model = City
        fields = ['cityId', 'cityName', 'count']

    def get_count(self, instance):
        return DharamSthan.objects.filter(cityId=instance.cityId).count()
