from rest_framework import serializers
from jdcApi.models import City, Area, MstSect, MstMaritalStatus, MstProfession
from accounts.models import User
from datetime import datetime


class GETCityWithCountSerializer(serializers.ModelSerializer):
    count = serializers.IntegerField()

    class Meta:
        model = City
        fields = ['cityId', 'cityName', 'count']


class GETAllResidentsForMatrimonialSerializer(serializers.ModelSerializer):
    maritalStatus = serializers.SerializerMethodField()
    profession = serializers.SerializerMethodField()
    sect = serializers.SerializerMethodField()
    age = serializers.IntegerField()
    dob = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'headId', 'name', 'maritalStatus', 'gotra', 'nativePlace', 'profession', 'sect', 'age', 'dob', 'currentAddress']

    def get_maritalStatus(self, instance):
        try:
            obj = MstMaritalStatus.objects.get(id=instance.maritalStatusId)
            return obj.maritalStatusName
        except MstMaritalStatus.DoesNotExist:
            return ""

    def get_profession(self,instance):
        try:
            obj = MstProfession.objects.get(id=instance.professionId)
            return obj.description
        except MstProfession.DoesNotExist:
            return ""

    def get_sect(self, instance):
        try:
            obj = MstSect.objects.get(id=instance.sectId)
            return obj.sectName
        except MstSect.DoesNotExist:
            return ""

    def get_dob(self, instance):
        if instance.dob:
            return instance.dob.strftime("%d %B, %Y")
        return ""

