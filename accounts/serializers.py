
from .models import CustomUser
from rest_framework import serializers


class HeadSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ['name', 'fatherName', 'phoneNumber', 'cityId', 'address', 'maritalStatus', 'lookingForMatch', 'dob',
                  'sect', 'profession', 'phoneNumberVisibility', 'gender', 'gotra', 'bloodGroup', 'nativePlace',
                  'currentAddress']
        model = CustomUser

    def create(self, validated_data):
        request = self.context.get('request')
        created_by_user = request.user if request else validated_data['phoneNumber']
        validated_data['createdBy'] = created_by_user

        # Example: Transforming 'name' to uppercase
        validated_data['name'] = validated_data['name'].upper()

        # Create the user instance with modified data
        user = self.Meta.model.objects.create(**validated_data)

        return user

    # def update(self, instance, validated_data):
    #     request = self.context.get('request')
    #     updated_by_user = request.user if request else validated_data['phoneNumber']
    #
    #     # Set the 'updatedBy' field to the user who is updating the instance
    #     validated_data['updatedBy'] = updated_by_user
    #
    #     # Update the user instance with modified data
    #     for attr, value in validated_data.items():
    #         setattr(instance, attr, value)
    #     instance.save()
    #
    #     return instance


class MemberSerializer(serializers.ModelSerializer):
    headId = serializers.IntegerField()

    class Meta:
        fields = ['headId', 'name',  'relationWithHead', 'phoneNumber', 'maritalStatus', 'lookingForMatch', 'sect',
                  'profession', 'bloodGroup', 'dob', 'nativePlace', 'gotra', 'phoneNumberVisibility', 'gender']
        model = CustomUser

    def create(self, validated_data):
        request = self.context.get('request')
        # print('request user==>', request.user)
        created_by_user = request.user if request else validated_data['headId']
        validated_data['createdBy'] = created_by_user

        # Create the user instance with modified data
        user = self.Meta.model.objects.create(**validated_data)

        return user

    # def update(self, instance, validated_data):
    #     request = self.context.get('request')
    #     updated_by_user = request.user if request else validated_data['headId']
    #     print('updated_by_user ==> ', updated_by_user)
    #     # Set the 'updatedBy' field to the user who is updating the instance
    #     validated_data['updatedBy'] = updated_by_user
    #
    #     # Update the user instance with modified data
    #     for attr, value in validated_data.items():
    #         setattr(instance, attr, value)
    #     instance.save()
    #
    #     return instance


class UpdateMemberSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ['name',  'relationWithHead', 'phoneNumber', 'maritalStatus', 'lookingForMatch', 'sect',
                  'profession', 'bloodGroup', 'dob', 'nativePlace', 'gotra', 'phoneNumberVisibility', 'gender']
        model = CustomUser

    def update(self, instance, validated_data):
        # request = self.context.get('request')
        # updated_by_user = request.user if request else validated_data['headId']
        # print('updated_by_user ==> ', updated_by_user)
        # # Set the 'updatedBy' field to the user who is updating the instance
        # validated_data['updatedBy'] = updated_by_user

        # Update the user instance with modified data
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        return instance


class GETHeadSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ['userId', 'name', 'phoneNumber', 'gotra', 'dob', 'nativePlace', 'address']
        model = CustomUser

    def to_representation(self, instance):
        # Get the default representation of the instance
        data = super().to_representation(instance)

        # Modify the field before returning the data
        is_number_visible = self.context.get('phoneNumberVisibility')
        if not is_number_visible:
            data['phoneNumber'] = 'xx-xxxx-xxxx'
        return data


from .auth import get_age_by_dob


class GETFamilyByHeadIdSerializer(serializers.ModelSerializer):
    # age = serializers.CharField()
    class Meta:
        fields = ['userId', 'name', 'relationWithHead', 'gotra', 'profession', 'dob', 'nativePlace', 'address', 'phoneNumber','phoneNumberVisibility' ]
        model = CustomUser

    def to_representation(self, instance):
        # Get the default representation of the instance
        data = super().to_representation(instance)

        data['age'] = str(get_age_by_dob(data['dob']))+' Year'

        # Modify the field before returning the data
        is_number_visible = data['phoneNumberVisibility']
        if not is_number_visible:
            data['phoneNumber'] = 'xx-xxxx-xxxx'
        data.pop('phoneNumberVisibility')
        data.pop('dob')
        return data




class GETAllUserSerializer(serializers.ModelSerializer):
    # age = serializers.CharField()
    class Meta:
        fields = ['name', 'gotra',  'nativePlace', 'profession',  'dob',  'address', 'phoneNumber','phoneNumberVisibility' ]
        model = CustomUser

    def to_representation(self, instance):
        # Get the default representation of the instance
        data = super().to_representation(instance)

        data['age'] = str(get_age_by_dob(data['dob']))+' Year'

        # Modify the field before returning the data
        is_number_visible = data['phoneNumberVisibility']
        if not is_number_visible:
            data['phoneNumber'] = 'xx-xxxx-xxxx'
        data.pop('phoneNumberVisibility')
        data.pop('dob')
        return data


class GETMemberByIdSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ['name', 'phoneNumber', 'address', 'profession', 'bloodGroup', 'nativePlace',   'maritalStatus',
                  'lookingForMatch', 'relationWithHead', 'gotra', 'dob', 'phoneNumberVisibility', 'gender', 'phoneNumberVisibility']
        model = CustomUser