from django.db.models import Q
from rest_framework import serializers
from .models import *
from datetime import datetime


def check_pincode_length(value):
    try:
        int(value)
    except ValueError:
        raise serializers.ValidationError('Please enter only number')
    if len(value) == 6:
        return value
    raise serializers.ValidationError('Pincode length must be 6 not less than or greater than 6.')


def find_age_using_dob(dob):
    #  to find the age by using 'dob'
    birthdate = datetime.strptime(dob, '%Y-%m-%d')
    current_date = datetime.now()
    # Calculate the age
    age = current_date.year - birthdate.year - (
                (current_date.month, current_date.day) < (birthdate.month, birthdate.day))

    return age

# ******************* Area serializers ***********************
class GETAreaWithCountSerializer(serializers.ModelSerializer):
    count = serializers.SerializerMethodField()
    class Meta:
        model = Area
        fields = ['areaId', 'areaName', 'count']

    def get_count(self, instance):
        total_members = User.objects.filter(areaId=instance.areaId).count()
        return total_members


class GETAreaSerializer(serializers.ModelSerializer):

    class Meta:
        model = Area
        fields = ['areaId', 'areaName']


class GETAreaForAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Area
        fields = ['areaId', 'areaName', 'areaContactNumber']


class CREATEAreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Area
        fields = ['cityId', 'areaName', 'areaMC', 'landmark', 'areaContactNumber']

    def to_internal_value(self, data):
        city_id = data.get('cityId')
        area_name = data.get('areaName')
        errors = {}
        # custom validation
        if city_id:
            try:
                City.objects.get(cityId=city_id)
                if area_name:
                    matching_cities_count = Area.objects.filter(Q(cityId=city_id) & Q(areaName__iexact=area_name.strip())).count()
                    if matching_cities_count > 0:
                        errors['areaName'] = [f"'{area_name}' is already exist."]
            except City.DoesNotExist:
                errors['cityId'] = ["Invalid City Id."]
            except ValueError:
                errors['cityId'] = [f"'city id' excepted a number but got '{city_id}'."]

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
        validated_data['areaName'] = validated_data['areaName'].capitalize()
        # Create the user instance with modified data
        city_obj = self.Meta.model.objects.create(**validated_data)

        #  add data in field createdBy
        user_id_by_token = self.context.get('user_id_by_token')
        city_obj.createdBy = user_id_by_token
        city_obj.save()

        return city_obj


class UPDATEAreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Area
        fields = ['cityId', 'areaName', 'areaMC', 'landmark', 'areaContactNumber', 'isActive', 'isVerified']

    def update(self, instance, validated_data):
        # Update the user instance with modified data
        if validated_data.get('areaName'):
            validated_data['areaName'] = validated_data['areaName'].capitalize()

        user_id_by_token = self.context.get('user_id_by_token')
        validated_data['updatedBy'] = user_id_by_token
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

    def to_internal_value(self, data):
        updated_fields = {key: value for key, value in data.items() if key in self.Meta.fields}
        if len(updated_fields) == 0:
            raise serializers.ValidationError(
                {'update_validation_error': ["At least one field must be provided to update the record."]})

        city_id = data.get('cityId')
        area_name = data.get('areaName')
        errors = {}
        # custom validation
        if city_id:
            try:
                City.objects.get(cityId=city_id)
                if area_name:
                    area_id = self.context.get('areaId')
                    matching_cities_count = Area.objects.filter(Q(areaName__iexact=area_name.strip()), ~Q(areaId=area_id), ~Q(cityId=city_id)).count()
                    if matching_cities_count > 0:
                        errors['areaName'] = [f"'{area_name}' is already exist."]
            except City.DoesNotExist:
                errors['cityId'] = ["Invalid City Id."]
            except ValueError:
                errors['cityId'] = [f"'city id' excepted a number but got '{city_id}'."]

        if city_id is None and area_name:
            errors['areaName'] = [f"to update 'areaName' must provide 'cityId' also."]
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

class GETResidentsByAreaId(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['cityId', 'areaName', 'areaMC', 'landmark', 'areaContactNumber', 'isActive', 'isVerified']

class GETAreaByAreaIdSerializer(serializers.ModelSerializer):
    class Meta:
        model = Area
        fields = ['cityId', 'areaName', 'areaMC', 'landmark', 'areaContactNumber', 'isActive', 'isVerified']



#  **************  Business Serializers  ***********************
class CREATEBusinessSerializer(serializers.ModelSerializer):
    class Meta:
        model = Business
        fields = ['cityId', 'userId', 'businessName', 'businessType', 'businessPhoneNumber', 'email', 'website', 'businessDescription']

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
        user_id = data.get('userId')

        # Custom validation for cityId and userId
        if city_id is None:
            pass
        elif not City.objects.filter(cityId=city_id).exists():
            raise serializers.ValidationError({'cityId': ["Invalid cityId or Id does not exist."]})

        if user_id is None:
            pass
        elif not User.objects.filter(id=user_id).exists():
            raise serializers.ValidationError({'userId': ["Invalid userId or Id does not exist."]})

        return super().to_internal_value(data)


class UPDATEBusinessSerializer(serializers.ModelSerializer):
    class Meta:
        model = Business
        fields = ['businessName', 'businessType', 'businessPhoneNumber', 'email', 'website', 'businessDescription', 'isVerified', 'isActive']

    def update(self, instance, validated_data):
        # Update the user instance with modified data
        try:
            validated_data['businessName'] = validated_data['businessName'].capitalize()
        except KeyError:
            pass
        user_id_by_token = self.context.get('user_id_by_token')
        validated_data['updatedBy'] = user_id_by_token
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

    def to_internal_value(self, data):
        city_id = data.get('cityId')
        if not City.objects.filter(cityId=city_id).exists() and city_id is not None:
            raise serializers.ValidationError({'cityId': 'Invalid cityId - Id does not exist.'})

        return super().to_internal_value(data)


class GETBusinessSerializer(serializers.ModelSerializer):
    class Meta:
        model = Business
        fields = ['businessId', 'businessName', 'businessType', 'businessDescription', 'businessPhoneNumber', 'website', 'email']


class GETBusinessByIdSerializer(serializers.ModelSerializer):
    class Meta:
        model = Business
        fields = ['businessName', 'businessType', 'businessPhoneNumber', 'email', 'website', 'businessDescription', 'isVerified', 'isActive']

# ************************* city serializer  *****************************


class GETCitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        # fields = ['cityId', 'cityName','city_by_areas']
        fields = ['cityId', 'cityName']


class GETCityWithCountSerializer(serializers.ModelSerializer):
    count = serializers.SerializerMethodField()

    class Meta:
        model = City
        # fields = ['cityId', 'cityName','city_by_areas']
        fields = ['cityId', 'cityName', 'count']

    def get_count(self, instance):
        screen_type = self.context.get('screen_type')
        if screen_type == 'business':
            total_businesses = Business.objects.filter(cityId=instance.cityId, isActive=True, isVerified=True).count()
            return total_businesses
        else:
            total_members = User.objects.filter(cityId=instance.cityId).count()
            return total_members
class GETCityCountForBusinessSerializer(serializers.ModelSerializer):
    count = serializers.SerializerMethodField()

    class Meta:
        model = City
        # fields = ['cityId', 'cityName','city_by_areas']
        fields = ['cityId', 'cityName', 'count']

    def get_count(self, instance):
        total_businesses = Business.objects.filter(cityId=instance.cityId, isActive=True, isVerified=True).count()
        return total_businesses


class CREATECitySerializer(serializers.ModelSerializer):
    """ this serializer use both 'getById, create and update' """

    class Meta:
        model = City
        fields = ['cityName', 'pincode', 'stateId', 'description', 'isActiveForResidents']

    def to_internal_value(self, data):
        city_name = data.get('cityName')
        state_id = data.get('stateId')
        pincode = data.get('pincode')
        errors = {}

        #  custom validation
        if state_id:
            try:
                # check stateId is integer or not
                int(state_id)
                # check state is exist or not
                State.objects.get(stateId=state_id)

                # check city name is not None
                if city_name:
                    matching_cities_count = City.objects.filter(stateId=state_id, cityName=city_name.strip()).count()
                    if matching_cities_count > 0:
                        errors['cityName'] = [f"'{city_name}' is already exist."]
            except State.DoesNotExist:
                errors['stateId'] = ["Invalid State Id."]
                print('does not exist error occur')
            except ValueError:
                print('value error occur')
                errors['stateId'] = [f"'stateId' expected a number but got '{state_id}'."]
        if pincode:
            if not pincode.strip().isdigit():
                errors['pincode'] = ["Enter a valid pincode."]
        validated_data = None
        # default validation
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

    def create(self, validated_data):
        validated_data['cityName'] = validated_data['cityName'].capitalize()
        # Create the user instance with modified data
        city_obj = self.Meta.model.objects.create(**validated_data)

        #  add data in field createdBy
        user_id_by_token = self.context.get('user_id_by_token')
        city_obj.createdBy = user_id_by_token
        city_obj.updatedBy = user_id_by_token
        city_obj.save()
        return city_obj


class UPDATECitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ['cityName', 'pincode', 'stateId', 'description', 'isVerified', 'isActive', 'isActiveForResidents']

    def update(self, instance, validated_data):
        # Update the user instance with modified data
        validated_data['cityName'] = validated_data['cityName'].capitalize()

        user_id_by_token = self.context.get('user_id_by_token')
        validated_data['updatedBy'] = user_id_by_token
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

    def to_internal_value(self, data):

        # if user not provide at least one field to update record
        updated_fields = {key: value for key, value in data.items() if key in self.Meta.fields}
        if len(updated_fields) < 1:
            raise serializers.ValidationError(
                {'update_validation_error': ["At least one field must be provided to update the record."]})

        city_name = data.get('cityName')
        state_id = data.get('stateId')
        pincode = data.get('pincode')
        errors = {}
        validated_data = None
        if state_id:
            try:
                # check stateId is integer or not
                int(state_id)
                # check state is exist or not
                State.objects.get(stateId=state_id)
                # check city name is not None
                if city_name:
                    city_id = self.context.get('city_id')
                    matching_cities_count = City.objects.filter(Q(stateId=state_id), Q(cityName__iexact=city_name.strip()), ~Q(cityId=city_id)).count()
                    if matching_cities_count > 0:
                        errors['cityName'] = [f"'{city_name}' is already exist."]
            except State.DoesNotExist:
                errors['stateId'] = ["Invalid State Id."]
                print('does not exist error occur')
            except ValueError:
                print('value error occur')
                errors['stateId'] = [f"'stateId' expected a number but got '{state_id}'."]
        if pincode:
            if not pincode.strip().isdigit():
                errors['pincode'] = ["Enter a valid pincode."]

        # default validation
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


class GETCityByCityIdSerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ['cityId', 'cityName', 'pincode', 'stateId', 'description', 'isActiveForResidents']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if self.context.get('status'):
            data['isVerified'] = instance.isVerified
        return data


# class GetAllAreaByCitySerializer(serializers.ModelSerializer):
#     count = serializers.SerializerMethodField()
#
#     class Meta:
#         model = Area
#         fields = ['areaId', 'areaName', 'count']
#
#     def get_count(self, obj):
#         # Retrieve 'areaId' and 'areaName' fields from areas where isActive=True and isVerified=True
#         total_areas = Area.objects.filter(areaId=obj.areaId).count()
#         return total_areas


#  ******************* State serializers *************************

class GETStateSerializer(serializers.ModelSerializer):

    class Meta:
        model = State
        fields = ['stateId', 'stateName']


class CREATEStateSerializer(serializers.ModelSerializer):
    """ this serializer use both 'create and update' """
    class Meta:
        model = State
        fields = ['stateName']

    def to_internal_value(self, data):
        errors = {}
        validated_data = None

        # custom validation
        state_name = data.get('stateName')
        # check state already exist or not
        if state_name:
            if self.context.get('put_method'):  # if put method
                matching_state_count = State.objects.filter(Q(stateName__iexact=state_name.strip()),
                                                             ~Q(stateId=self.context.get('state_id'))).count()
            else:
                matching_state_count = State.objects.filter(stateName__iexact=state_name.strip()).count()
            if matching_state_count > 0:
                errors['stateName'] = [f"{state_name}' is already exists."]

        # default validation
        try:
            # store all data in "validated_data" variable and return it
            validated_data = super().to_internal_value(data)
        except serializers.ValidationError as e:
            new_errors = e.detail.copy()  # Make a copy of the custom errors
            for key, value in new_errors.items():
                if key not in errors:
                    errors[key] = value  # Add new keys to the errors dictionary

        # raise all errors
        if errors:
            # print('errors ==> ', errors)
            raise serializers.ValidationError(errors)

        return validated_data

    def create(self, validated_data):
        validated_data['stateName'] = validated_data['stateName'].strip().capitalize()
        # Create the user instance with modified data
        state_obj = self.Meta.model.objects.create(**validated_data)

        #  add data in field createdBy
        user_id_by_token = self.context.get('user_id_by_token')
        state_obj.createdBy = user_id_by_token
        state_obj.save()
        return state_obj

    def update(self, instance, validated_data):
        # Update the user instance with modified data
        validated_data['stateName'] = validated_data['stateName'].strip().capitalize()

        user_id_by_token = self.context.get('user_id_by_token')
        validated_data['updatedBy'] = user_id_by_token
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class GetAllCitiesByStateSerializer(serializers.ModelSerializer):
    cities = GETCitySerializer(read_only=True, many=True)

    class Meta:
        model = State
        fields = ('stateId', 'stateName', 'cities')


#  ***********************    Literature Serializer  ******************

class GETLiteratureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Literature
        fields = ['literatureId', 'title']


class CREATELiteratureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Literature
        fields = ['title', 'order', 'body']

    def create(self, validated_data):
        validated_data['title'] = validated_data['title'].capitalize()
        # Create the user instance with modified data
        state_obj = self.Meta.model.objects.create(**validated_data)

        #  add data in field createdBy
        user_id_by_token = self.context.get('user_id_by_token')
        state_obj.createdBy = user_id_by_token
        state_obj.save()

        return state_obj


class UPDATELiteratureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Literature
        fields = ['title', 'order', 'body', 'isVerified', 'isActive']

    def update(self, instance, validated_data):
        # Update the user instance with modified data
        try:
            validated_data['title'] = validated_data['title'].capitalize()
        except KeyError:
            pass

        user_id_by_token = self.context.get('user_id_by_token')
        validated_data['updatedBy'] = user_id_by_token
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class GETLiteratureByIdSerializer(serializers.ModelSerializer):
    class Meta:
        model = Literature
        fields = ['literatureId', 'title', 'body', 'isVerified', 'isActive']


#  *******************************  Aarti Serializer  ********************
class PartialAartiSerializer(serializers.ModelSerializer):
    class Meta:
        model = Aarti
        fields = ['aartiId', 'aartiName']


class AartiSerializer(serializers.ModelSerializer):
    class Meta:
        model = Aarti
        fields = ['aartiId', 'aartiName', 'aartiText', 'isVerified', 'isActive']


#                       ***********************             Saint Serializers             ****************************
class CREATESaintSerializer(serializers.ModelSerializer):
    dob = serializers.DateTimeField(input_formats=['%B %d, %Y %I:%M %p']) # according to 12hr clock to send default time 12:00 AM
    # dob = serializers.DateTimeField(input_formats=['%B %d, %Y %H:%M']) # according to 24hr clock to send default time 00:00
    dikshaDate = serializers.DateField(input_formats=['%B %d, %Y'])
    devlokDate = serializers.DateTimeField(input_formats=['%B %d, %Y %I:%M %p'], required=False, allow_null=True)

    class Meta:
        model = Saint
        fields = ['name', 'sectId', 'fatherName', 'motherName', 'birthPlace', 'dikshaPlace', 'guruName','dob','dikshaDate', 'devlokDate', 'gender', 'description']

    # def validate(self, data):
    #     """ set blank values to None """
    #     optional_fields = ['devlokDate', 'description']
    #     #check optional_field name in given data
    #     for field_name in optional_fields:
    #         if field_name in data and isinstance(data[field_name], str) and data[field_name].strip() == "":
    #             data[field_name] = None  # Set the field to None for empty strings with only spaces
    #     return data

    def to_internal_value(self, data):
        print(data)
        sect_id = data.get('sectId')
        if sect_id:
            try:
                MstSect.objects.get(id=sect_id)
            except MstSect.DoesNotExist:
                raise serializers.ValidationError({'sectId': ['Invalid Sect ID']})
            except ValueError:
                raise serializers.ValidationError({'sectId': [f"'sectId' excepted a number but got '{sect_id}."]})
        # print(self.validate(data))
        # print(data)
        return super().to_internal_value(data)

    def create(self, validated_data):
        validated_data['name'] = validated_data['name'].capitalize()
        validated_data['fatherName'] = validated_data['fatherName'].capitalize()
        validated_data['motherName'] = validated_data['motherName'].capitalize()
        validated_data['guruName'] = validated_data['guruName'].capitalize()
        validated_data['birthPlace'] = validated_data['birthPlace'].capitalize()

        # Create the user instance with modified data
        saint_obj = self.Meta.model.objects.create(**validated_data)

        #  add data in field createdBy
        user_id_by_token = self.context.get('user_id_by_token')
        saint_obj.createdBy = user_id_by_token
        saint_obj.save()

        return saint_obj


class UPDATESaintSerializer(serializers.ModelSerializer):
    dob = serializers.DateField(input_formats=['%B %d, %Y %I:%M %p'])
    dikshaDate = serializers.DateField(input_formats=['%B %d, %Y'])
    devlokDate = serializers.DateField(input_formats=['%B %d, %Y %I:%M %p'], required=False)

    class Meta:
        model = Saint
        fields = ['name', 'sectId', 'fatherName', 'motherName', 'birthPlace', 'dikshaPlace', 'guruName','dob','dikshaDate', 'devlokDate', 'gender', 'description', 'isVerified']

    def update(self, instance, validated_data):
        # Update the user instance with modified data
        try:
            validated_data['name'] = validated_data['name'].capitalize()
            validated_data['fatherName'] = validated_data['fatherName'].capitalize()
            validated_data['motherName'] = validated_data['motherName'].capitalize()
            validated_data['guruName'] = validated_data['guruName'].capitalize()
            validated_data['birthPlace'] = validated_data['birthPlace'].capitalize()
        except KeyError:
            pass

        user_id_by_token = self.context.get('user_id_by_token')
        validated_data['updatedBy'] = user_id_by_token
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

    def to_internal_value(self, data):
        sect_id = data.get('sectId')
        print(sect_id)
        if sect_id:
            try:
                MstSect.objects.get(id=sect_id)
            except MstSect.DoesNotExist:
                raise serializers.ValidationError({'sectId': ['Invalid Sect ID']})
            except ValueError:
                raise serializers.ValidationError({'sectId': [f"'sectId' excepted a number but got '{sect_id}."]})

        return super().to_internal_value(data)

    def validate(self, data):
        # Check if at least one field is being updated
        updated_fields = {key: value for key, value in data.items() if key in self.Meta.fields}
        if len(updated_fields) == 0:
            raise serializers.ValidationError({'update_validation_error':"At least one field must be provided for the update."})
        return data


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
    # dikshaDate = serializers.DateField(input_formats=['%B %d, %Y'])
    sectId = serializers.CharField(source='sectId.sectName', read_only=True)
    # dob = serializers.DateField(input_formats=['%B %d, %Y'])
    # age = serializers.SerializerMethodField()

    class Meta:
        model = Saint
        fields = ['name', 'sectId', 'fatherName', 'motherName', 'birthPlace', 'dikshaPlace', 'guruName', 'dikshaDate', 'gender', 'dob', 'description']

    def get_age(self, instance):
        return find_age_using_dob(str(instance.dob.date()))

    def to_representation(self, instance):
        data = super().to_representation(instance)
        # print(data)
        data['dikshaDate'] = instance.dikshaDate.strftime("%B %d, %Y")
        data['dob'] = instance.dob.strftime("%B %d, %Y %I:%M %p")

        return data

#  *********************************************    Mst Serializer         ********************************************

#                       ***********************             Sect Serializers             ****************************
class GETAllSectWithCountSerializer(serializers.ModelSerializer):
    count = serializers.SerializerMethodField()

    class Meta:
        model = MstSect
        fields = ['id', 'sectName', 'count']

    def get_count(self, sect):
        # Calculate the count of records in the 'Saint' model based on the 'Sect' field
        return Saint.objects.filter(sectId=sect).count()


class CREATESectSerializer(serializers.ModelSerializer):
    class Meta:
        model = MstSect
        fields = ['id', 'sectName', 'order']

    def create(self, validated_data):
        validated_data['sectName'] = validated_data['sectName'].capitalize()
        # Create the user instance with modified data
        obj = self.Meta.model.objects.create(**validated_data)
        #  add data in field createdBy
        user_id_by_token = self.context.get('user_id_by_token')
        obj.createdBy = user_id_by_token
        obj.updatedBy = user_id_by_token
        obj.isActive = True
        obj.save()
        return obj

    def to_internal_value(self, data):
        sectName = data.get('sectName')
        if sectName:
            filtered_obj_count = MstSect.objects.filter(sectName__iexact=sectName.strip()).count()
            if filtered_obj_count > 0:
                raise serializers.ValidationError({'sectName': [f"'{sectName}' is already exist."]})
        return super().to_internal_value(data)


class UPDATESectSerializer(serializers.ModelSerializer):
    class Meta:
        model = MstSect
        fields = ['id', 'sectName', 'order', 'isActive']

    def update(self, instance, validated_data):
        # Update the user instance with modified data
        try:
            validated_data['sectName'] = validated_data['sectName'].capitalize()
        except KeyError:
            pass

        user_id_by_token = self.context.get('user_id_by_token')
        validated_data['updatedBy'] = user_id_by_token
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

    def to_internal_value(self, data):
        sect_name = data.get('sectName')
        id = self.context.get('id')

        if sect_name:
            filtered_obj_count = MstSect.objects.filter(Q(sectName__iexact=sect_name.strip()),
                                                              ~Q(id=id)).count()
            if filtered_obj_count > 0:
                raise serializers.ValidationError({'sectName': [f"'{sect_name}' is already exist."]})

        return super().to_internal_value(data)

    def validate(self, data):
        # Check if at least one field is being updated
        updated_fields = {key: value for key, value in data.items() if key in self.Meta.fields}
        if len(updated_fields) == 0:
            raise serializers.ValidationError({"update_validation_error": ["At least one field must be provided for the update."]})
        return data


class GETSectDetailsByIdSerializer(serializers.ModelSerializer):
    class Meta:
        model = MstSect
        fields = ['id', 'sectName', 'order', 'isActive']


class GETAllSectSerializer(serializers.ModelSerializer):
    class Meta:
        model = MstSect
        fields = ['id', 'sectName', 'order']


class GETAllSectForDropDownSerializer(serializers.ModelSerializer):
    class Meta:
        model = MstSect
        fields = ['id', 'sectName']


#                 ***********************             Blood Group Serializers             ****************************
class CREATEBloodGroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = MstBloodGroup
        fields = ['bloodGroupName', 'order']

    def create(self, validated_data):
        validated_data['bloodGroupName'] = validated_data['bloodGroupName'].upper()
        # Create the user instance with modified data
        obj = self.Meta.model.objects.create(**validated_data)
        #  add data in field createdBy
        user_id_by_token = self.context.get('user_id_by_token')
        obj.createdBy = user_id_by_token
        obj.updatedBy = user_id_by_token
        obj.isActive = True
        obj.save()
        return obj

    def to_internal_value(self, data):
        bloodGroupName = data.get('bloodGroupName')
        if bloodGroupName:
            filtered_obj_count = MstBloodGroup.objects.filter(bloodGroupName__iexact=bloodGroupName.strip()).count()
            if filtered_obj_count > 0:
                raise serializers.ValidationError({'bloodGroupName': [f"'{bloodGroupName}' is already exist."]})
        return super().to_internal_value(data)


class UPDATEBloodGroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = MstBloodGroup
        fields = ['bloodGroupName', 'order', 'isActive']

    def update(self, instance, validated_data):
        # Update the user instance with modified data
        try:
            validated_data['bloodGroupName'] = validated_data['bloodGroupName'].capitalize()
        except KeyError:
            pass

        user_id_by_token = self.context.get('user_id_by_token')
        validated_data['updatedBy'] = user_id_by_token
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

    def to_internal_value(self, data):
        bloodGroupName = data.get('bloodGroupName')
        id = self.context.get('id')
        if bloodGroupName:
            filtered_obj_count = MstBloodGroup.objects.filter(Q(bloodGroupName__iexact=bloodGroupName.strip()), ~Q(id=id)).count()
            if filtered_obj_count > 0:
                raise serializers.ValidationError({'bloodGroupName': [f"'{bloodGroupName}' is already exist."]})
        return super().to_internal_value(data)

    def validate(self, data):
        # Check if at least one field is being updated
        updated_fields = {key: value for key, value in data.items() if key in self.Meta.fields}
        if len(updated_fields) == 0:
            raise serializers.ValidationError({"update_validation_error": ["At least one field must be provided for the update."]})
        return data


class GETBloodGroupByIdSerializer(serializers.ModelSerializer):

    class Meta:
        model = MstBloodGroup
        fields = ['id', 'bloodGroupName', 'order', 'isActive']


class GETAllBloodGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = MstBloodGroup
        fields = ['id', 'bloodGroupName', 'order']


class GETAllBloodGroupForDropDownSerializer(serializers.ModelSerializer):
    class Meta:
        model = MstBloodGroup
        fields = ['id', 'bloodGroupName']


#            ***********************             marital Status  Serializers             ****************************

class CREATEMaritalStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = MstMaritalStatus
        fields = ['id', 'maritalStatusName', 'order']

    def create(self, validated_data):
        validated_data['maritalStatusName'] = validated_data['maritalStatusName'].capitalize()
        # Create the user instance with modified data
        obj = self.Meta.model.objects.create(**validated_data)
        #  add data in field createdBy
        user_id_by_token = self.context.get('user_id_by_token')
        obj.createdBy = user_id_by_token
        obj.updatedBy = user_id_by_token
        obj.isActive = True
        obj.save()
        return obj

    def to_internal_value(self, data):
        maritalStatusName = data.get('maritalStatusName')
        if maritalStatusName:
            filtered_obj_count = MstMaritalStatus.objects.filter(maritalStatusName__iexact=maritalStatusName.strip()).count()
            if filtered_obj_count > 0:
                raise serializers.ValidationError({'maritalStatusName': [f"'{maritalStatusName}' is already exist."]})
        return super().to_internal_value(data)


class UPDATEMaritalStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = MstMaritalStatus
        fields = ['maritalStatusName', 'order', 'isActive']

    def update(self, instance, validated_data):
        # Update the user instance with modified data
        try:
            validated_data['maritalStatusName'] = validated_data['maritalStatusName'].capitalize()
        except KeyError:
            pass

        user_id_by_token = self.context.get('user_id_by_token')
        validated_data['updatedBy'] = user_id_by_token
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

    def to_internal_value(self, data):
        maritalStatusName = data.get('maritalStatusName')
        id = self.context.get('id')
        if maritalStatusName:
            filtered_obj_count = MstMaritalStatus.objects.filter(Q(maritalStatusName__iexact=maritalStatusName.strip()),
                                                              ~Q(id=id)).count()
            if filtered_obj_count > 0:
                raise serializers.ValidationError({'maritalStatusName': [f"'{maritalStatusName}' is already exist."]})
        return super().to_internal_value(data)

    def validate(self, data):
        # Check if at least one field is being updated
        updated_fields = {key: value for key, value in data.items() if key in self.Meta.fields}
        if len(updated_fields) == 0:
            raise serializers.ValidationError({"update_validation_error": ["At least one field must be provided for the update."]})
        return data


class GETMaritalStatusByIdSerializer(serializers.ModelSerializer):
    class Meta:
        model = MstMaritalStatus
        fields = ['id', 'maritalStatusName', 'order', 'isActive']


class GETAllMaritalStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = MstMaritalStatus
        fields = ['id', 'maritalStatusName', 'order']


class GETAllMaritalStatusForDropDownSerializer(serializers.ModelSerializer):
    class Meta:
        model = MstMaritalStatus
        fields = ['id', 'maritalStatusName']


#            ***********************             marital Status  Serializers             ****************************
class CREATERelationSerializer(serializers.ModelSerializer):
    class Meta:
        model = MstRelation
        fields = ['description', 'order']

    def create(self, validated_data):
        validated_data['description'] = validated_data['description'].capitalize()
        # Create the user instance with modified data
        obj = self.Meta.model.objects.create(**validated_data)
        #  add data in field createdBy
        user_id_by_token = self.context.get('user_id_by_token')
        obj.createdBy = user_id_by_token
        obj.updatedBy = user_id_by_token
        obj.isActive = True
        obj.save()
        return obj

    def to_internal_value(self, data):
        description = data.get('description')
        if description:
            filtered_obj_count = MstRelation.objects.filter(description__iexact=description.strip()).count()
            if filtered_obj_count > 0:
                raise serializers.ValidationError({'description': [f"'{description}' is already exist."]})
        return super().to_internal_value(data)


class UPDATERelationSerializer(serializers.ModelSerializer):
    class Meta:
        model = MstRelation
        fields = ['description', 'order', 'isActive']

    def update(self, instance, validated_data):
        # Update the user instance with modified data
        try:
            validated_data['description'] = validated_data['description'].capitalize()
        except KeyError:
            pass

        user_id_by_token = self.context.get('user_id_by_token')
        validated_data['updatedBy'] = user_id_by_token
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

    def to_internal_value(self, data):
        description = data.get('description')
        id = self.context.get('id')
        if description:
            filtered_obj_count = MstRelation.objects.filter(Q(description__iexact=description.strip()),
                                                              ~Q(id=id)).count()
            if filtered_obj_count > 0:
                raise serializers.ValidationError({'description': [f"'{description}' is already exist."]})
        return super().to_internal_value(data)

    def validate(self, data):
        # Check if at least one field is being updated
        updated_fields = {key: value for key, value in data.items() if key in self.Meta.fields}
        if len(updated_fields) == 0:
            raise serializers.ValidationError({"update_validation_error": ["At least one field must be provided for the update."]})
        return data

class GETRelationDetailsByIdSerializer(serializers.ModelSerializer):
    class Meta:
        model = MstRelation
        fields = ['id', 'description', 'order', 'isActive']


class GETAllRelationSerializer(serializers.ModelSerializer):
    class Meta:
        model = MstRelation
        fields = ['id', 'description', 'order']


class GETAllRelationForDropDownSerializer(serializers.ModelSerializer):
    class Meta:
        model = MstRelation
        fields = ['id', 'description']


#    ***********************************************    Profession ****************************
class CREATEProfessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = MstProfession
        fields = ['description', 'order']

    def create(self, validated_data):
        validated_data['description'] = validated_data['description'].capitalize()
        # Create the user instance with modified data
        obj = self.Meta.model.objects.create(**validated_data)
        #  add data in field createdBy
        user_id_by_token = self.context.get('user_id_by_token')
        obj.createdBy = user_id_by_token
        obj.updatedBy = user_id_by_token
        obj.isActive = True
        obj.save()
        return obj

    def to_internal_value(self, data):
        description = data.get('description')
        if description:
            filtered_obj_count = MstProfession.objects.filter(description__iexact=description.strip()).count()
            if filtered_obj_count > 0:
                raise serializers.ValidationError({'description': [f"'{description}' is already exist."]})
        return super().to_internal_value(data)


class UPDATEProfessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = MstProfession
        fields = ['description', 'order', 'isActive']

    def update(self, instance, validated_data):
        # Update the user instance with modified data
        try:
            validated_data['description'] = validated_data['description'].capitalize()
        except KeyError:
            pass

        user_id_by_token = self.context.get('user_id_by_token')
        validated_data['updatedBy'] = user_id_by_token
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

    def to_internal_value(self, data):
        description = data.get('description')
        id = self.context.get('id')

        if description:
            filtered_obj_count = MstProfession.objects.filter(Q(description__iexact=description.strip()),
                                                              ~Q(id=id)).count()
            if filtered_obj_count > 0:
                raise serializers.ValidationError({'description': [f"'{description}' is already exist."]})

        return super().to_internal_value(data)

    def validate(self, data):
        # Check if at least one field is being updated
        updated_fields = {key: value for key, value in data.items() if key in self.Meta.fields}
        if len(updated_fields) == 0:
            raise serializers.ValidationError({"update_validation_error": ["At least one field must be provided for the update."]})
        return data


class GETProfessionDetailsByIdSerializer(serializers.ModelSerializer):
    class Meta:
        model = MstProfession
        fields = ['id', 'description', 'order', 'isActive']


class GETAllProfessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = MstProfession
        fields = ['id', 'description', 'order']


class GETAllProfessionForDropDownSerializer(serializers.ModelSerializer):
    class Meta:
        model = MstProfession
        fields = ['id', 'description']



