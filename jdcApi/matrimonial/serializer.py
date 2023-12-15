from rest_framework import serializers
from jdcApi.models import City, Area, MstSect, MstMaritalStatus, MstProfession
from accounts.models import User
from datetime import datetime


class GETCityWithCountSerializer(serializers.ModelSerializer):
    count = serializers.SerializerMethodField()

    class Meta:
        model = City
        fields = ['cityId', 'cityName', 'count']

    def get_count(self, instance):
        return User.objects.filter(cityId=instance.cityId, lookingForMatch=True).count()


class GETAllResidentsForMatrimonialSerializer(serializers.ModelSerializer):
    maritalStatus = serializers.SerializerMethodField()
    profession = serializers.SerializerMethodField()
    sect = serializers.SerializerMethodField()
    age = serializers.SerializerMethodField()
    dob = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'headId', 'name', 'maritalStatus', 'gotra', 'nativePlace', 'profession', 'sect', 'age', 'dob', 'currentAddress']

    def get_maritalStatus(self,instance):
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

    def get_age(self, instance):
        dob = instance.dob
        #  to find the age by using 'dob'
        birthdate = datetime.strptime(str(dob), '%Y-%m-%d')
        current_date = datetime.now()
        # Calculate the age
        age = current_date.year - birthdate.year - (
                (current_date.month, current_date.day) < (birthdate.month, birthdate.day))

        return age

    def get_dob(self, instance):
        return instance.dob.strftime("%d %B, %Y")