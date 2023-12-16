from rest_framework import serializers
from jdcApi.models import City, Area, MstSect
from accounts.models import User


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

    class Meta:
        model = User
        fields = ['id', 'name', 'nativePlace', 'areaName', 'permanentAddress', 'phoneNumber']

    def get_areaName(self, instance):
        try:
            obj = Area.objects.get(areaId=instance.areaId)
            return obj.areaName
        except Area.DoesNotExist:
            return ""


class GETSectWithCountSerializer(serializers.ModelSerializer):
    count = serializers.SerializerMethodField()

    class Meta:
        model = MstSect
        fields = ['id', 'sectName', 'count']

    def get_count(self, instance):
        total_members = User.objects.filter(sectId=instance.id).count()
        return total_members

