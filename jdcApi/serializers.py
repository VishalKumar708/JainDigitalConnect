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


# ************************* city serializer  *****************************


#  ******************* State serializers *************************



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


#  *********************************************    Mst Serializer         ********************************************

#                       ***********************             Sect Serializers             ****************************


class GETAllSectWithCountForResidentsSerializer(serializers.ModelSerializer):
    count = serializers.SerializerMethodField()

    class Meta:
        model = MstSect
        fields = ['id', 'sectName', 'count']

    def get_count(self, sect):
        # Calculate the count of records in the 'Saint' model based on the 'Sect' field
        return User.objects.filter(sectId=sect.id).count()


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



