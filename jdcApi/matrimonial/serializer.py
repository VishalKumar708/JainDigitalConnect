from rest_framework import serializers
from jdcApi.models import City, Area

from accounts.models import User


class GETCityWithCountSerializer(serializers.ModelSerializer):
    count = serializers.IntegerField()

    class Meta:
        model = City
        fields = ['cityId', 'cityName', 'count']


class GETAllResidentsForMatrimonialSerializer(serializers.ModelSerializer):
    maritalStatus = serializers.CharField(source='maritalStatus.maritalStatusName', default="")
    profession = serializers.CharField(source='professionId.description', default="")
    sect = serializers.CharField(source='sectId.sectName', default="")
    age = serializers.IntegerField()
    dob = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'headId', 'name', 'maritalStatus', 'gotra', 'nativePlace', 'profession', 'sect', 'age', 'dob', 'currentAddress']

    def get_dob(self, instance):
        if instance.dob:
            return instance.dob.strftime("%d %B, %Y")
        return ""

