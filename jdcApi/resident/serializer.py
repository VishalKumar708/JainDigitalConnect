from rest_framework import serializers
from masterApi.models import MstSect, MstProfession
from jdcApi.models import City, Area
from accounts.models import User

from datetime import datetime


class GETCitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ['cityId', 'cityName']


class GETCityWithCountSerializer(serializers.ModelSerializer):
    # count = serializers.SerializerMethodField()
    count = serializers.IntegerField()

    class Meta:
        model = City
        fields = ['cityId', 'cityName', 'count']

    # def get_count(self, instance):
    #     if self.context.get('sect_wise'):
    #         total_members = User.objects.filter(cityId=instance.cityId, sectId=self.context.get('sect_id')).count()
    #         return total_members
    #     else:
    #         total_members = User.objects.filter(cityId=instance.cityId).count()
    #         return total_members


class GETAreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Area
        fields = ['areaId', 'areaName']


class GETAreaWithCountSerializer(serializers.ModelSerializer):
    count = serializers.IntegerField()
    memberCount = serializers.IntegerField()
    familyCount = serializers.IntegerField()

    class Meta:
        model = Area
        fields = ['areaId', 'areaName', 'count', 'memberCount', 'familyCount']


class SearchResidentByCityIdSerializer(serializers.ModelSerializer):
    areaName = serializers.CharField(source="areaId.areaName", default="")
    profession = serializers.CharField(source="professionId.description", default="")
    phoneNumber = serializers.SerializerMethodField()
    age = serializers.CharField()

    class Meta:
        model = User
        fields = ['id', 'name', 'nativePlace', 'areaName', 'permanentAddress', 'phoneNumber', 'gotra', 'profession', 'phoneNumber', 'age']

    def get_phoneNumber(self, instance):
        is_number_visible = instance.phoneNumberVisibility
        if not is_number_visible:
            return 'xx-xxxx-xxxx'
        return str(instance.phoneNumber)


class GETSectWithCountSerializer(serializers.ModelSerializer):
    count = serializers.IntegerField()

    class Meta:
        model = MstSect
        fields = ['id', 'sectName', 'count']



