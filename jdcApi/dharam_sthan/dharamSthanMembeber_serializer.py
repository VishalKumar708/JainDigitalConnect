from django.db.models import Q
from rest_framework import serializers
from jdcApi.models import DharamSthanMember, DharamSthan


class CREATEDharamSthanMemberSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True, allow_null=False)

    class Meta:
        model = DharamSthanMember
        fields = ['name', "dharamSthanId", 'position', 'phoneNumber']

    def create(self, validated_data):
        validated_data['name'] = validated_data['name'].title()
        # Create the user instance with modified data
        obj = self.Meta.model.objects.create(**validated_data)
        #  add data in field createdBy
        user_id_by_token = self.context.get('user_id_by_token')
        obj.createdBy = user_id_by_token
        obj.save()
        return obj

    def to_internal_value(self, data):
        dharam_sthan_id = data.get('dharamSthanId')
        phone_number = data.get('phoneNumber')
        errors = {}
        # custom validation
        if dharam_sthan_id:
            try:
                DharamSthan.objects.get(id=dharam_sthan_id)
            except DharamSthan.DoesNotExist:
                errors['dharamSthanId'] = ["Invalid Id."]
            except ValueError:
                errors['dharamSthanId'] = [f"excepted a number but got '{dharam_sthan_id}'."]

        if phone_number:
            if not str(phone_number).strip().isdigit() or len(str(phone_number).strip()) != 10:
                errors['phoneNumber'] = ['Please Enter Valid Phone Number.']
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


class UPDATEDharamSthanMemberByIdSerializer(serializers.ModelSerializer):

    class Meta:
        model = DharamSthanMember
        fields = ['name', "dharamSthanId", 'position', 'phoneNumber', 'isVerified', 'isActive']

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
        dharam_sthan_id = data.get('dharamSthanId')
        phone_number = data.get('phoneNumber')
        errors = {}
        # custom validation
        if dharam_sthan_id:
            try:
                DharamSthan.objects.get(id=dharam_sthan_id)
            except DharamSthan.DoesNotExist:
                errors['dharamSthanId'] = ["Invalid Id."]
            except ValueError:
                errors['dharamSthanId'] = [f"excepted a number but got '{dharam_sthan_id}'."]

        if phone_number:
            if not str(phone_number).strip().isdigit() or len(str(phone_number).strip()) != 10:
                errors['phoneNumber'] = ['Please Enter Valid Phone Number.']
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


class GETDharamSthanMemberDetialsByIdSerializer(serializers.ModelSerializer):

    class Meta:
        model = DharamSthanMember
        fields = ['id', 'name', 'position', 'phoneNumber', 'isActive', 'isVerified']



