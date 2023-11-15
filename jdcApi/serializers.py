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
class GETAreaSerializer(serializers.ModelSerializer):

    class Meta:
        model = Area
        fields = ['areaId', 'areaName']


class CREATEAreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Area
        fields = ['cityId', 'areaName', 'areaMC', 'landmark', 'areaContactNumber']

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
        validated_data['areaName'] = validated_data['areaName'].capitalize()

        user_id_by_token = self.context.get('user_id_by_token')
        validated_data['updatedBy'] = user_id_by_token
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


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


class CREATECitySerializer(serializers.ModelSerializer):
    """ this serializer use both 'getById, create and update' """

    class Meta:
        model = City
        fields = ['cityName', 'pincode', 'stateId', 'description']

    def create(self, validated_data):
        validated_data['cityName'] = validated_data['cityName'].capitalize()
        # Create the user instance with modified data
        city_obj = self.Meta.model.objects.create(**validated_data)

        #  add data in field createdBy
        user_id_by_token = self.context.get('user_id_by_token')
        city_obj.createdBy = user_id_by_token
        city_obj.save()

        return city_obj


class UPDATECitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ['cityName', 'pincode', 'stateId', 'description', 'isVerified', 'isActive']

    def update(self, instance, validated_data):
        # Update the user instance with modified data
        validated_data['cityName'] = validated_data['cityName'].capitalize()

        user_id_by_token = self.context.get('user_id_by_token')
        validated_data['updatedBy'] = user_id_by_token
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class GETCityByCityIdSerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ['cityId', 'cityName', 'pincode', 'stateId', 'description']


class GetAllAreaByCitySerializer(serializers.ModelSerializer):
    areas = serializers.SerializerMethodField()

    class Meta:
        model = City
        fields = ['cityId', 'cityName', 'areas']

    def get_areas(self, obj):
        city_id = self.context.get('cityId')
        # Retrieve 'areaId' and 'areaName' fields from areas where isActive=True and isVerified=True
        areas = Area.objects.filter(isActive=True, isVerified=True, cityId=city_id).values('areaId', 'areaName')
        return areas


class GetAllBusinessByCitySerializer(serializers.ModelSerializer):
    # GetAllBusinessByCityId = PartialBusinessSerializer(read_only=True, many=True)
    allBusiness = serializers.SerializerMethodField()

    class Meta:
        model = City
        fields = ['cityId', 'cityName', 'allBusiness']

    def get_allBusiness(self, obj):
        city_id = self.context.get('cityId')
        business = Business.objects.filter(isActive=True, isVerified=True, cityId=city_id).values('businessId', 'businessName','businessType', 'businessDescription', 'businessNumber', 'email', 'website')
        return business


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

    def create(self, validated_data):
        validated_data['stateName'] = validated_data['stateName'].capitalize()
        # Create the user instance with modified data
        state_obj = self.Meta.model.objects.create(**validated_data)

        #  add data in field createdBy
        user_id_by_token = self.context.get('user_id_by_token')
        state_obj.createdBy = user_id_by_token
        state_obj.save()

        return state_obj

    def update(self, instance, validated_data):
        # Update the user instance with modified data
        validated_data['stateName'] = validated_data['stateName'].capitalize()

        user_id_by_token = self.context.get('user_id_by_token')
        validated_data['updatedBy'] = user_id_by_token
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class GetAllCitiesByStateSerializer(serializers.ModelSerializer):
    city_by_state = GETCitySerializer(read_only=True, many=True)

    class Meta:
        model = State
        fields = ('stateId', 'stateName', 'city_by_state')


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


#                       ***********************             Sect Serializers             ****************************
class GETAllSectWithCountSerializer(serializers.ModelSerializer):
    count = serializers.SerializerMethodField()
    class Meta:
        model = Sect
        fields = ['id', 'sectName', 'count']

    def get_count(self, sect):
        # Calculate the count of records in the 'Saint' model based on the 'Sect' field
        return Saint.objects.filter(selectSect=sect).count()


class GETAllSectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sect
        fields = ['id', 'sectName']


#                       ***********************             Saint Serializers             ****************************
class CREATESaintSerializer(serializers.ModelSerializer):
    dob = serializers.DateField(input_formats=['%B %d, %Y %I:%M:%S %p'])
    dikshaDate = serializers.DateField(input_formats=['%B %d, %Y'])
    devlokDate = serializers.DateField(input_formats=['%B %d, %Y %I:%M:%S %p'])

    class Meta:
        model = Saint
        fields = ['name', 'selectSect', 'fatherName', 'motherName', 'birthPlace', 'dikshaPlace', 'guruName','dob','dikshaDate', 'devlokDate', 'gender', 'description']

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

    def to_internal_value(self, data):
        select_sect_id = data.get('selectSect')
        if select_sect_id:
            try:
                Sect.objects.get(id=select_sect_id)
            except Sect.DoesNotExist:
                raise serializers.ValidationError({'selectSect': ['Invalid Sect ID']})
            except ValueError:
                raise serializers.ValidationError({'selectSect': [f"'selectSect' excepted a number but got '{select_sect_id}."]})

        return super().to_internal_value(data)


class UPDATESaintSerializer(serializers.ModelSerializer):
    dob = serializers.DateField(input_formats=['%B %d, %Y %I:%M:%S %p'])
    dikshaDate = serializers.DateField(input_formats=['%B %d, %Y'])
    devlokDate = serializers.DateField(input_formats=['%B %d, %Y %I:%M:%S %p'])

    class Meta:
        model = Saint
        fields = ['name', 'selectSect', 'fatherName', 'motherName', 'birthPlace', 'dikshaPlace', 'guruName','dob','dikshaDate', 'devlokDate', 'gender', 'description', 'isVerified']

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
        select_sect_id = data.get('selectSect')
        if select_sect_id:
            try:
                Sect.objects.get(id=select_sect_id)
            except Sect.DoesNotExist:
                raise serializers.ValidationError({'selectSect': ['Invalid Sect ID']})
            except ValueError:
                raise serializers.ValidationError({'selectSect': [f"'selectSect' excepted a number but got '{select_sect_id}."]})

        return super().to_internal_value(data)

    def validate(self, data):
        # Check if at least one field is being updated
        updated_fields = {key: value for key, value in data.items() if key in self.Meta.fields}
        if len(updated_fields) == 0:
            raise serializers.ValidationError("At least one field must be provided for the update.")
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
    sect = serializers.CharField(source='selectSect.sectName', read_only=True)
    # dob = serializers.DateField(input_formats=['%B %d, %Y'])
    # age = serializers.SerializerMethodField()

    class Meta:
        model = Saint
        fields = ['name', 'sect', 'fatherName', 'motherName', 'birthPlace', 'dikshaPlace', 'guruName', 'dikshaDate', 'gender', 'dob', 'description']

    def get_age(self, instance):
        print('get age method.')
        return find_age_using_dob(str(instance.dob.date()))

    def to_representation(self, instance):
        data = super().to_representation(instance)
        # print(data)
        data['dikshaDate'] = instance.dikshaDate.strftime("%B %d, %Y")
        data['dob'] = instance.dob.strftime("%B %d, %Y %I:%M:%S %p")

        return data

