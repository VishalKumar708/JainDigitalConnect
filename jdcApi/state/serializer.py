from rest_framework import serializers
from jdcApi.models import State, City
from django.db.models import Q


class GETStateSerializer(serializers.ModelSerializer):

    class Meta:
        model = State
        fields = ['stateId', 'stateName']


class CREATEStateSerializer(serializers.ModelSerializer):
    """ this serializer use both 'create and update' """
    class Meta:
        model = State
        fields = ['stateName', 'isVerified', 'isActive']

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


class GETCitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        # fields = ['cityId', 'cityName','city_by_areas']
        fields = ['cityId', 'cityName']


class GetAllCitiesByStateSerializer(serializers.ModelSerializer):
    cities = GETCitySerializer(read_only=True, many=True)

    class Meta:
        model = State
        fields = ('stateId', 'stateName', 'cities')


class GETStateById(serializers.ModelSerializer):
    class Meta:
        model = State
        fields = ('stateId', 'stateName', 'isVerified', 'isActive')
