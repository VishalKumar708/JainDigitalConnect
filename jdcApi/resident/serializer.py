from rest_framework import serializers
from jdcApi.models import City, Area, MstSect, MstProfession
from accounts.models import User

from datetime import datetime


class GETCitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ['cityId', 'cityName']


class GETCityWithCountSerializer(serializers.ModelSerializer):
    count = serializers.SerializerMethodField()

    class Meta:
        model = City
        fields = ['cityId', 'cityName', 'count']

    def get_count(self, instance):
        if self.context.get('sect_wise'):
            total_members = User.objects.filter(cityId=instance.cityId, sectId=self.context.get('sect_id')).count()
            return total_members
        else:
            total_members = User.objects.filter(cityId=instance.cityId).count()
            return total_members


class GETAreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Area
        fields = ['areaId', 'areaName']


class GETAreaWithCountSerializer(serializers.ModelSerializer):
    count = serializers.SerializerMethodField()
    memberCount = serializers.SerializerMethodField()
    familyCount = serializers.SerializerMethodField()

    class Meta:
        model = Area
        fields = ['areaId', 'areaName', 'count', 'memberCount', 'familyCount']

    def get_count(self, instance):
        if self.context.get('sect_wise'):
            total_members = User.objects.filter(areaId=instance.areaId, sectId=self.context.get('sect_id')).count()
            return total_members
        else:
            total_members = User.objects.filter(areaId=instance.areaId).count()
            return total_members

    def get_memberCount(self, instance):
            return User.objects.filter(areaId=instance.areaId).count()

    def get_familyCount(self, instance):
            return User.objects.filter(areaId=instance.areaId, headId=None).count()


class SearchResidentByCityIdSerializer(serializers.ModelSerializer):
    areaName = serializers.SerializerMethodField()
    profession = serializers.SerializerMethodField()
    phoneNumber = serializers.SerializerMethodField()
    age = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'name', 'nativePlace', 'areaName', 'permanentAddress', 'phoneNumber', 'gotra', 'profession', 'phoneNumber', 'age']

    def get_areaName(self, instance):
        try:
            obj = Area.objects.get(areaId=instance.areaId)
            return obj.areaName
        except Area.DoesNotExist:
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


class GETSectWithCountSerializer(serializers.ModelSerializer):
    count = serializers.SerializerMethodField()

    class Meta:
        model = MstSect
        fields = ['id', 'sectName', 'count']

    def get_count(self, instance):
        total_members = User.objects.filter(sectId=instance.id).count()
        return total_members

