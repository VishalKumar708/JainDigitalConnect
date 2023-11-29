
from rest_framework import serializers
from jdcApi.models import City, Business
from accounts.models import User
from datetime import datetime


class CREATEBusinessSerializer(serializers.ModelSerializer):
    class Meta:
        model = Business
        fields = ['cityId', 'userId', 'businessName', 'businessType', 'businessPhoneNumber', 'email', 'website','gstNumber', 'address', 'businessDescription']

    def create(self, validated_data):
        validated_data['businessName'] = validated_data['businessName'].capitalize()
        # Create the user instance with modified data
        city_obj = self.Meta.model.objects.create(**validated_data)

        #  add data in field createdBy
        user_id_by_token = self.context.get('user_id_by_token')
        city_obj.createdBy = user_id_by_token
        city_obj.save()

        return city_obj

    def to_internal_value(self, data):
        city_id = data.get('cityId')
        business_name = data.get('businessName')
        user_id = data.get('userId')
        errors = {}
        # Custom validation for cityId and userId
        if city_id:
            try:
                City.objects.filter(cityId=city_id)
            except City.DoesNotExist:
                errors['cityId'] = ["Invalid cityId."]
            except ValueError:
                errors['cityId'] = [f"excepted a number but got {city_id}."]
        if user_id:
            try:
                User.objects.get(id=user_id)
            except User.DoesNotExist:
                errors['userId'] = ["Invalid User Id."]
            except ValueError:
                errors['userId'] = [f"excepted a number but got '{user_id}'."]

        if business_name and user_id:
            try:
                filtered_data = Business.objects.filter(userId=user_id,
                                                        businessName__icontains=business_name.strip()).count()
                if filtered_data > 0:
                    errors['businessName'] = [f"'{business_name}' already exist."]
            except ValueError:
                pass

        #  default validation
        validated_data = None
        try:
            # store all data in "validated_data" variable and return it
            validated_data = super().to_internal_value(data)
        except serializers.ValidationError as e:
            new_errors = e.detail.copy()  # Make a copy of the custom errors
            for key, value in new_errors.items():
                if key not in errors:
                    errors[key] = value  # Add new keys to the errors dictionary

        # return all validations errors
        if errors:
            # print('errors ==> ', errors)
            raise serializers.ValidationError(errors)

        return validated_data


class PUTBusinessSerializer(serializers.ModelSerializer):
    class Meta:
        model = Business
        fields = ['userId', 'cityId', 'businessName', 'businessType', 'businessPhoneNumber', 'email', 'website','gstNumber','address', 'businessDescription']

    def update(self, instance, validated_data):
        # Update the user instance with modified data
        if validated_data.get('businessName'):
            validated_data['businessName'] = validated_data['businessName'].capitalize()

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
                {'update_validation_error': ["At least one field must be provided to update the record."]})

        city_id = data.get('cityId')
        business_name = data.get('businessName')
        user_id = data.get('userId')
        errors = {}
        # Custom validation for cityId and userId
        if city_id:
            try:
                City.objects.filter(cityId=city_id)
            except City.DoesNotExist:
                errors['cityId'] = ["Invalid cityId."]
            except ValueError:
                errors['cityId'] = [f"excepted a number but got {city_id}."]
        if user_id:
            try:
                User.objects.get(id=user_id)
            except User.DoesNotExist:
                errors['userId'] = ["Invalid User Id."]
            except ValueError:
                errors['userId'] = [f"excepted a number but got '{user_id}'."]

        #  default validation
        validated_data = None
        try:
            # store all data in "validated_data" variable and return it
            validated_data = super().to_internal_value(data)
        except serializers.ValidationError as e:
            new_errors = e.detail.copy()  # Make a copy of the custom errors
            for key, value in new_errors.items():
                if key not in errors:
                    errors[key] = value  # Add new keys to the errors dictionary

        # return all validations errors
        if errors:
            # print('errors ==> ', errors)
            raise serializers.ValidationError(errors)

        return validated_data


class GETBusinessSerializer(serializers.ModelSerializer):
    class Meta:
        model = Business
        fields = ['businessId', 'businessName', 'businessType', 'businessDescription', 'businessPhoneNumber', 'website', 'email', 'gstNumber', 'address']


class GETBusinessByIdSerializer(serializers.ModelSerializer):
    cityName = serializers.CharField(source='cityId.cityName', read_only=True)

    class Meta:
        model = Business
        fields = ['businessId','cityId', 'cityName', 'businessName', 'businessType', 'businessPhoneNumber', 'email', 'website', 'gstNumber', 'businessDescription', 'isVerified', 'isActive']


class GETCityCountForBusinessSerializer(serializers.ModelSerializer):
    count = serializers.SerializerMethodField()

    class Meta:
        model = City
        fields = ['cityId', 'cityName', 'count']

    def get_count(self, instance):
        total_businesses = Business.objects.filter(cityId=instance.cityId, isActive=True, isVerified=True).count()
        return total_businesses


class GETCitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City

        fields = ['cityId', 'cityName']

