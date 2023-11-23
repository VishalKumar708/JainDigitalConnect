from datetime import datetime

from django.db.models import Q

from .models import User, Notification
from rest_framework import serializers
from .auth import get_user_id_from_token_view
from jdcApi.models import City, Area, MstSect, MstBloodGroup, MstMaritalStatus, MstRelation, MstProfession
from .utils import is_valid_mobile_number


class HeadSerializer(serializers.ModelSerializer):
    dob = serializers.DateField(input_formats=("%B %d, %Y",), required=False)

    class Meta:
        fields = ['name', 'fatherName', 'phoneNumber', 'cityId', 'areaId', 'permanentAddress', 'maritalStatusId', 'lookingForMatch', 'dob',
                  'sectId', 'professionId', 'phoneNumberVisibility', 'gender', 'gotra', 'bloodGroupId', 'nativePlace',
                  'currentAddress']
        model = User

    def create(self, validated_data):

        # Example: Transforming 'name' to uppercase
        validated_data['name'] = validated_data['name'].upper()
        # Create the user instance with modified data
        user = self.Meta.model.objects.create(**validated_data)

        #  add data in field createdBy
        user_id_by_token = self.context.get('user_id_by_token')
        user.createdBy = user_id_by_token if user_id_by_token else user.id
        user.updatedBy = user.createdBy
        user.save()
        return user

    def to_internal_value(self, data):
        validated_data = None
        phoneNumber = data.get('phoneNumber')
        sectId = data.get('sectId')
        cityId = data.get('cityId')
        areaId = data.get('areaId')
        professionId = data.get('professionId')
        maritalStatusId = data.get('maritalStatusId')
        bloodGroupId = data.get('bloodGroupId')

        # print(phoneNumber, sectId, cityId, areaId)
        errors = {}
        #  custom validation
        if phoneNumber:
            if not is_valid_mobile_number(str(phoneNumber)):
                errors['phoneNumber'] = ["Please enter a valid phone number.11"]
            else:
                filtered_objects = User.objects.filter(phoneNumber=phoneNumber)
                if len(filtered_objects) > 0:
                    # raise serializers.ValidationError({'phoneNumber': ['Please enter unique phoneNumber.']})
                    errors['phoneNumber'] = ["Please enter unique phoneNumber."]

        if sectId:
            try:
                MstSect.objects.get(id=sectId)
            except MstSect.DoesNotExist:
                errors['sectId'] = ['Invalid Sect Id.']
            except ValueError:
                errors['sectId'] = [f"excepted number but got '{sectId}'."]

        if cityId:
            try:
                City.objects.get(cityId=cityId)
            except City.DoesNotExist:
                errors['cityId'] = ['Invalid City Id.']
            except ValueError:
                errors['cityId'] = [f"excepted number but got '{cityId}'."]

        if areaId:
            try:
                Area.objects.get(areaId=areaId)
            except Area.DoesNotExist:
                errors['areaId'] = ['Invalid Area Id.']
            except ValueError:
                errors['areaId'] = [f"excepted number but got '{areaId}'."]

        if professionId:
            try:
                MstProfession.objects.get(id=professionId)
            except MstProfession.DoesNotExist:
                errors['professionId'] = ['Invalid Profession Id.']
            except ValueError:
                errors['professionId'] = [f"excepted number but got '{professionId}'."]

        if maritalStatusId:
            try:
                MstMaritalStatus.objects.get(id=maritalStatusId)
            except MstMaritalStatus.DoesNotExist:
                errors['maritalStatusId'] = ['Invalid MaritalStatus Id.']
            except ValueError:
                errors['maritalStatusId'] = [f"excepted number but got '{maritalStatusId}'."]

        if bloodGroupId:
            try:
                MstBloodGroup.objects.get(id=bloodGroupId)
            except MstBloodGroup.DoesNotExist:
                errors['bloodGroupId'] = ['Invalid BloodGroup Id.']
            except ValueError:
                errors['bloodGroupId'] = [f"excepted number but got '{bloodGroupId}'."]

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


class MemberSerializer(serializers.ModelSerializer):
    headId = serializers.IntegerField()
    dob = serializers.DateField(input_formats=("%B %d, %Y",), required=False)
    relationId = serializers.IntegerField(required=True)
    sectId = serializers.IntegerField(required=False)
    cityId = serializers.IntegerField(required=False)
    areaId = serializers.IntegerField(required=False)

    class Meta:
        fields = ['headId', 'name',  'relationId', 'phoneNumber', 'phoneNumberVisibility',  'gender',
                  'sectId', 'bloodGroupId', 'nativePlace',  'gotra', 'maritalStatusId', 'lookingForMatch',
                  'professionId',  'dob', 'cityId', 'areaId']
        model = User

    def create(self, validated_data):
        # Create the user instance with modified data
        user = self.Meta.model.objects.create(**validated_data)

        #  add data in field createdBy
        user_id_by_token = self.context.get('user_id_by_token')
        user.createdBy = user_id_by_token if user_id_by_token else user.id
        user.updatedBy = user.createdBy
        user.save()
        return user

    def to_internal_value(self, data):
        validated_data = None
        head_id = data.get('headId')
        phone_number = data.get('phoneNumber')

        errors = {}

        # custom validation
        # check headId is valid or not
        try:
            head_obj = User.objects.get(id=head_id, headId=None)
            data['cityId'] = head_obj.cityId
            data['areaId'] = head_obj.areaId
            if 'sectId' not in data:
                data['sectId'] = head_obj.sectId

        except User.DoesNotExist:
            errors['headId'] = ['Invalid Head Id.']
        except ValueError:
            errors['headId'] = [f"'headId' excepted number but got '{head_id}'."]

        # check phoneNumber is valid or not
        if phone_number:
            # check phoneNumber format
            if not phone_number.isdigit() or len(phone_number.strip()) != 10:
                errors['phoneNumber'] = ["Please Enter Valid Phone Number."]

            #  check phoneNumber is already exist or not if phoneNumber is not equal to 0000000000
            if str(phone_number) != '0000000000':
                filtered_data = User.objects.filter(phoneNumber=phone_number).count()
                if filtered_data > 0:
                    errors['phoneNumber'] = ["Please Enter Unique Phone Number."]
            #  check phoneNumber is already exist or not if phoneNumber is equal to 0000000000
            elif str(phone_number) == '0000000000':
                member_name = data.get('name')
                if member_name:
                    filtered_data = User.objects.filter(phoneNumber='0000000000', headId=head_id, name__iexact=member_name.strip()).count()
                    if filtered_data > 0:
                        errors['phoneNumber'] = ["This Member is already exist."]

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


class UpdateMemberSerializer(serializers.ModelSerializer):
    dob = serializers.DateField(input_formats=("%B %d, %Y",), allow_null=True)

    class Meta:
        fields = ['name', 'fatherName', 'phoneNumber', 'currentAddress', 'professionId', 'maritalStatusId', 'lookingForMatch',
         'relationId', 'dob', 'sectId', 'cityId', 'areaId', 'gender', 'phoneNumberVisibility',
         'bloodGroupId', 'nativePlace', 'gotra']
        model = User

    def update(self, instance, validated_data):
        # Update the user instance with modified data
        user_id_by_token = self.context.get('user_id_by_token')
        validated_data['updatedBy'] = user_id_by_token if user_id_by_token else instance.id
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        # serializer context field
        is_admin = self.context.get('admin')
        if is_admin is not None:
            instance.isAdmin = is_admin
        instance.save()

        return instance

    def to_internal_value(self, data):
        # check user enter value at least one field or not
        updated_fields = {key: value for key, value in data.items() if key in self.Meta.fields}
        if len(updated_fields) < 1:
            raise serializers.ValidationError(
                {'update_validation_error': ["At least one field must be provided to update the record."]})

        validated_data = None
        phoneNumber = data.get('phoneNumber')
        sectId = data.get('sectId')
        cityId = data.get('cityId')
        areaId = data.get('areaId')
        professionId = data.get('professionId')
        maritalStatusId = data.get('maritalStatusId')
        bloodGroupId = data.get('bloodGroupId')

        errors = {}

        # value get from serializer 'context' field
        is_admin_field_error_message = self.context.get('is_admin_error_message')
        if is_admin_field_error_message:
            errors['isAdmin'] = is_admin_field_error_message

        #  custom validation
        if phoneNumber:
            if not is_valid_mobile_number(str(phoneNumber)):
                errors['phoneNumber'] = ["Please enter a valid phone number."]
            else:
                user_id = self.context.get('user_id')
                filtered_data = User.objects.filter(Q(phoneNumber=phoneNumber) & ~Q(id=user_id)).count()
                if filtered_data > 0:
                    errors['phoneNumber'] = ['Please enter unique Number.']
                    # raise serializers.ValidationError({'phoneNumber': 'Please enter unique Number.'})

        if sectId:
            try:
                MstSect.objects.get(id=sectId)
            except MstSect.DoesNotExist:
                errors['sectId'] = ['Invalid Sect Id.']
            except ValueError:
                errors['sectId'] = [f"excepted number but got '{sectId}'."]

        if cityId:
            try:
                City.objects.get(cityId=cityId)
            except City.DoesNotExist:
                errors['cityId'] = ['Invalid City Id.']
            except ValueError:
                errors['cityId'] = [f"excepted number but got '{cityId}'."]

        if areaId:
            try:
                Area.objects.get(areaId=areaId)
            except Area.DoesNotExist:
                errors['areaId'] = ['Invalid Area Id.']
            except ValueError:
                errors['areaId'] = [f"excepted number but got '{areaId}'."]

        if professionId:
            try:
                MstProfession.objects.get(id=professionId)
            except MstProfession.DoesNotExist:
                errors['professionId'] = ['Invalid Profession Id.']
            except ValueError:
                errors['professionId'] = [f"excepted number but got '{professionId}'."]

        if maritalStatusId:
            try:
                MstMaritalStatus.objects.get(id=maritalStatusId)
            except MstMaritalStatus.DoesNotExist:
                errors['maritalStatusId'] = ['Invalid MaritalStatus Id.']
            except ValueError:
                errors['maritalStatusId'] = [f"excepted number but got '{maritalStatusId}'."]

        if bloodGroupId:
            try:
                MstBloodGroup.objects.get(id=bloodGroupId)
            except MstBloodGroup.DoesNotExist:
                errors['bloodGroupId'] = ['Invalid BloodGroup Id.']
            except ValueError:
                errors['bloodGroupId'] = [f"excepted number but got '{bloodGroupId}'."]

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


    # def validate(self, data):
    #     # Check if at least one field is being updated
    #     updated_fields = {key: value for key, value in data.items() if key in self.Meta.fields}
    #     if len(updated_fields) < 1:
    #         raise serializers.ValidationError({'update_validation_error': ["At least one field must be provided to update the record."]})
    #
    #     user_id = self.context.get('user_id')
    #     phoneNumber = data.get('phoneNumber')
    #
    #     if phoneNumber:
    #         filtered_data = User.objects.filter(Q(phoneNumber=phoneNumber) & ~Q(id=user_id)).count()
    #         if filtered_data > 0:
    #             raise serializers.ValidationError({'phoneNumber': 'Please enter unique Number.'})
    #     return data


class GETHeadSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ['id', 'name', 'phoneNumber', 'gotra', 'dob', 'nativePlace', 'currentAddress']
        model = User

    def to_representation(self, instance):
        # Get the default representation of the instance
        data = super().to_representation(instance)

        # Modify the field before returning the data
        is_number_visible = self.context.get('phoneNumberVisibility')
        if not is_number_visible:
            data['phoneNumber'] = 'xx-xxxx-xxxx'
        return data


# from .auth import get_age_by_dob


class GETFamilyByHeadIdSerializer(serializers.ModelSerializer):
    # age = serializers.CharField()
    relation = serializers.SerializerMethodField()
    profession = serializers.SerializerMethodField()
    age = serializers.SerializerMethodField()
    phoneNumber = serializers.SerializerMethodField()

    class Meta:
        fields = ['id', 'name', 'relation', 'gotra', 'profession', 'age',  'nativePlace', 'currentAddress', 'phoneNumber']
        model = User

    def get_relation(self, instance):
        try:
            obj = MstRelation.objects.get(id=instance.relationId)
            return obj.description
        except MstRelation.DoesNotExist:
            return ""

    def get_profession(self, instance):
        try:
            obj = MstProfession.objects.get(id=instance.professionId)
            return obj.description
        except MstProfession.DoesNotExist:
            return ""

    def get_age(self, instance):
        dob = instance.dob
        if dob:
            birthdate = datetime.strptime(str(dob), '%Y-%m-%d')
            current_date = datetime.now()
            # Calculate the age
            age = current_date.year - birthdate.year - (
                    (current_date.month, current_date.day) < (birthdate.month, birthdate.day))
            # return age
            return str(age) + ' Year'
        else:
            return ''

    def get_phoneNumber(self, instance):

        is_number_visible = instance.phoneNumberVisibility
        if not is_number_visible:
            return 'xx-xxxx-xxxx'
        return instance.phoneNumber

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        # Loop through each field and convert null values to empty strings
        for key, value in representation.items():
            if value is None:
                representation[key] = ""
        return representation


class GETAllUserSerializer(serializers.ModelSerializer):
    age = serializers.SerializerMethodField()
    phoneNumber = serializers.SerializerMethodField()
    profession = serializers.SerializerMethodField()
    sect = serializers.SerializerMethodField()

    class Meta:
        fields = ['id', 'name', 'gotra', 'profession','sect', 'age', 'nativePlace', 'currentAddress', 'phoneNumber']
        model = User

    def get_profession(self, instance):
        try:
            obj = MstProfession.objects.get(id=instance.professionId)
            return obj.description
        except MstProfession.DoesNotExist:
            return ""

    def get_sect(self, instance):
        try:
            obj = MstSect.objects.get(id=instance.sectId)
            return obj.sectName
        except MstProfession.DoesNotExist:
            return ""

    def get_age(self, instance):
        dob = instance.dob
        if dob:
            birthdate = datetime.strptime(str(dob), '%Y-%m-%d')
            current_date = datetime.now()
            # Calculate the age
            age = current_date.year - birthdate.year - (
                    (current_date.month, current_date.day) < (birthdate.month, birthdate.day))
            # return age
            return str(age) + ' Year'
        else:
            return ''

    def get_phoneNumber(self, instance):

        is_number_visible = instance.phoneNumberVisibility
        if not is_number_visible:
            return 'xx-xxxx-xxxx'
        return instance.phoneNumber

    def get_profession(self, instance):
        try:
            obj = MstProfession.objects.get(id=instance.professionId)
            return obj.description
        except MstProfession.DoesNotExist:
            return ""

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        # Loop through each field and convert null values to empty strings
        for key, value in representation.items():
            if value is None:
                representation[key] = ""
        return representation


class GETUserDetailsByIdSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ['name', 'fatherName', 'phoneNumber', 'currentAddress', 'professionId', 'maritalStatusId', 'lookingForMatch',
                   'relationId', 'dob', 'sectId', 'cityId', 'areaId', 'gender', 'phoneNumberVisibility',
                  'bloodGroupId', 'nativePlace', 'gotra']
        model = User

    def to_representation(self, instance):
        # Get the default representation of the instance
        data = super().to_representation(instance)

        is_admin = self.context.get('admin')

        #  if admin check own profile then he will get this field value
        if is_admin:
            data['isAdmin'] = True

        # if user
        if self.context.get('show_admin_right'):
            data['isAdmin'] = instance.isAdmin

        #  to find the age by using 'dob'
        if data.get('dob'):
            original_dob = datetime.strptime(data['dob'], "%Y-%m-%d")
            data['dob'] = original_dob.strftime("%B %d, %Y")

        return data


class CreateNewNotificationSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ['userId', 'title', 'body', 'screen', 'type']
        model = Notification

    def create(self, validated_data):
        user_obj = self.context.get('user_obj')
        print('In serializer user object==> ', user_obj)
        # created_by_user = request.user if request else validated_data['userId']
        print("user_obj.id==> ", user_obj.id)
        created_by_user = user_obj.id
        validated_data['createdBy'] = created_by_user

        # Create the user instance with modified data
        user = self.Meta.model.objects.create(**validated_data)

        return user


#  *********************************************  get members by areaId  ***********************************************

class GETAllMemberByAreaIdSerializer(serializers.ModelSerializer):
    age = serializers.SerializerMethodField()
    phoneNumber = serializers.SerializerMethodField()
    profession = serializers.SerializerMethodField()
    sect = serializers.SerializerMethodField()

    class Meta:
        fields = ['id', 'name', 'gotra', 'profession', 'sect', 'age', 'nativePlace', 'currentAddress', 'phoneNumber']
        model = User


    def get_profession(self, instance):
        try:
            obj = MstProfession.objects.get(id=instance.professionId)
            return obj.description
        except MstProfession.DoesNotExist:
            return ""

    def get_sect(self, instance):
        try:
            obj = MstSect.objects.get(id=instance.sectId)
            return obj.sectName
        except MstProfession.DoesNotExist:
            return ""

    def get_age(self, instance):
        dob = instance.dob
        if dob:
            birthdate = datetime.strptime(str(dob), '%Y-%m-%d')
            current_date = datetime.now()
            # Calculate the age
            age = current_date.year - birthdate.year - (
                    (current_date.month, current_date.day) < (birthdate.month, birthdate.day))
            # return age
            return str(age) + ' Year'
        else:
            return ''

    def get_phoneNumber(self, instance):

        is_number_visible = instance.phoneNumberVisibility
        if not is_number_visible:
            return 'xx-xxxx-xxxx'
        return instance.phoneNumber

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        # Loop through each field and convert null values to empty strings
        for key, value in representation.items():
            if value is None:
                representation[key] = ""
        return representation


class GETAllFamilyByAreaIdSerializer(serializers.ModelSerializer):
    age = serializers.SerializerMethodField()
    phoneNumber = serializers.SerializerMethodField()
    profession = serializers.SerializerMethodField()
    sect = serializers.SerializerMethodField()

    class Meta:
        fields = ['id', 'name', 'gotra', 'profession', 'sect', 'age', 'nativePlace', 'currentAddress', 'phoneNumber']
        model = User

    def get_profession(self, instance):
        try:
            obj = MstProfession.objects.get(id=instance.professionId)
            return obj.description
        except MstProfession.DoesNotExist:
            return ""

    def get_sect(self, instance):
        try:
            obj = MstSect.objects.get(id=instance.sectId)
            return obj.sectName
        except MstProfession.DoesNotExist:
            return ""

    def get_age(self, instance):
        dob = instance.dob
        if dob:
            birthdate = datetime.strptime(str(dob), '%Y-%m-%d')
            current_date = datetime.now()
            # Calculate the age
            age = current_date.year - birthdate.year - (
                    (current_date.month, current_date.day) < (birthdate.month, birthdate.day))
            # return age
            return str(age) + ' Year'
        else:
            return ''

    def get_phoneNumber(self, instance):

        is_number_visible = instance.phoneNumberVisibility
        if not is_number_visible:
            return 'xx-xxxx-xxxx'
        return instance.phoneNumber

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        # Loop through each field and convert null values to empty strings
        for key, value in representation.items():
            if value is None:
                representation[key] = ""
        return representation


class SearchResidentsInAreaSerializer(serializers.ModelSerializer):
    phoneNumber = serializers.SerializerMethodField()

    class Meta:
        fields = ['id', 'name', 'phoneNumber', 'currentAddress']
        model = User

    def get_phoneNumber(self, instance):
        is_number_visible = instance.phoneNumberVisibility
        if not is_number_visible:
            return 'xx-xxxx-xxxx'
        return instance.phoneNumber

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        # Loop through each field and convert null values to empty strings
        for key, value in representation.items():
            if value is None:
                representation[key] = ""
        return representation
