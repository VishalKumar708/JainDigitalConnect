from datetime import datetime

from .models import User, Notification
from rest_framework import serializers





class HeadSerializer(serializers.ModelSerializer):
    dob = serializers.DateField(input_formats=("%B %d %Y",))

    class Meta:
        fields = ['name', 'fatherName', 'phoneNumber', 'cityId', 'address', 'maritalStatus', 'lookingForMatch', 'dob',
                  'sect', 'profession', 'phoneNumberVisibility', 'gender', 'gotra', 'bloodGroup', 'nativePlace',
                  'currentAddress']
        model = User

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
    dob = serializers.DateField(input_formats=("%B %d %Y",))


    class Meta:
        fields = ['headId', 'name',  'relationWithHead', 'phoneNumber', 'maritalStatus', 'lookingForMatch', 'sect',
                  'profession', 'bloodGroup', 'dob', 'nativePlace', 'gotra', 'phoneNumberVisibility', 'gender']
        model = User

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
    dob = serializers.DateField(input_formats=("%B %d %Y",))


    class Meta:
        fields = ['name',  'relationWithHead', 'phoneNumber', 'maritalStatus', 'lookingForMatch', 'sect',
                  'profession', 'bloodGroup', 'dob', 'nativePlace', 'gotra', 'phoneNumberVisibility', 'gender']
        model = User

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
        model = User

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
        model = User

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
    dob = serializers.DateField(input_formats=['%Y-%m-%d'])

    class Meta:
        fields = ['name', 'gotra',  'nativePlace', 'profession',  'dob',  'address', 'phoneNumber','phoneNumberVisibility' ]
        model = User

    def to_representation(self, instance):
        # Get the default representation of the instance
        data = super().to_representation(instance)

        #  to find the age by using 'dob'
        birthdate = datetime.strptime(data['dob'], '%Y-%m-%d')
        current_date = datetime.now()
        # Calculate the age
        age = current_date.year - birthdate.year - ((current_date.month, current_date.day) < (birthdate.month, birthdate.day))

        # add new key 'age' in serializer
        data['age'] = str(age)+' Year'

        # Modify the field before returning the data
        is_number_visible = data['phoneNumberVisibility']
        if not is_number_visible:
            data['phoneNumber'] = 'xx-xxxx-xxxx'

        # remove unnecessary fields
        data.pop('phoneNumberVisibility')
        data.pop('dob')
        return data


class GETMemberByIdSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ['name', 'phoneNumber', 'address', 'profession', 'bloodGroup', 'nativePlace',   'maritalStatus',
                  'lookingForMatch', 'relationWithHead', 'gotra', 'dob', 'phoneNumberVisibility', 'gender', 'phoneNumberVisibility']
        model = User


class CreateNewNotificationSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ['userId', 'title', 'body', 'screen', 'type']
        model = Notification

    def create(self, validated_data):
        request = self.context.get('request')
        # print('request user==>', request.user)
        user_obj = self.context.get('user_obj')
        print('In serializer user object==> ',user_obj )
        # created_by_user = request.user if request else validated_data['userId']
        created_by_user = user_obj.userId
        validated_data['createdBy'] = created_by_user

        # Create the user instance with modified data
        user = self.Meta.model.objects.create(**validated_data)

        return user

