from rest_framework import serializers
from jdcApi.models import MstMaritalStatus
from django.db.models import Q


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
        errors = {}
        if maritalStatusName:
            filtered_obj_count = MstMaritalStatus.objects.filter(maritalStatusName__iexact=maritalStatusName.strip()).count()
            if filtered_obj_count > 0:
                errors['maritalStatusName'] = [f"'{maritalStatusName}' is already exist."]

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

        # return all validations errors
        if errors:
            raise serializers.ValidationError(errors)

        return validated_data


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
        errors = {}
        if maritalStatusName:
            filtered_obj_count = MstMaritalStatus.objects.filter(Q(maritalStatusName__iexact=maritalStatusName.strip()),
                                                              ~Q(id=id)).count()
            if filtered_obj_count > 0:
                errors['maritalStatusName'] = [f"'{maritalStatusName}' is already exist."]

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
