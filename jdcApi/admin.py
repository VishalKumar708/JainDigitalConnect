from django.contrib import admin
from .models import *


class CityAdmin(admin.ModelAdmin):
    list_display = ['cityId', 'stateId', 'cityName', 'pincode', 'description', 'isVerified','isActive', 'isActiveForResidents', 'groupId', 'createdBy', 'updatedBy', 'createdDate','updatedDate']


admin.site.register(City, CityAdmin)


class StateAdmin(admin.ModelAdmin):
    list_display = ['stateId', 'stateName', 'isVerified', 'isActive', 'groupId', 'createdBy', 'updatedBy', 'createdDate', 'updatedDate']


admin.site.register(State,StateAdmin)


class AreaAdmin(admin.ModelAdmin):
    list_display = ['areaId', 'cityId', 'areaName', 'isVerified', 'isActive', 'areaMC', 'landmark', 'areaContactNumber','groupId', 'createdBy', 'updatedBy', 'createdDate', 'updatedDate']


admin.site.register(Area, AreaAdmin)


class LiteratureAdmin(admin.ModelAdmin):
    list_display = ['literatureId', 'title', 'body', 'isVerified', 'isActive', 'groupId', 'createdBy', 'updatedBy', 'createdDate','updatedDate']


admin.site.register(Literature,LiteratureAdmin)


class AartiAdmin(admin.ModelAdmin):
    list_display = ['aartiId', 'aartiName', 'aartiText', 'isVerified', 'isActive', 'groupId', 'createdBy', 'updatedBy', 'createdDate','updatedDate']


admin.site.register(Aarti, AartiAdmin)


class BusinessAdmin(admin.ModelAdmin):
    list_display = ['businessId', 'userId', 'cityId', 'businessName','businessType','businessPhoneNumber', 'email', 'website', 'businessDescription', 'isVerified', 'isActive', 'groupId', 'createdBy', 'updatedBy', 'createdDate', 'updatedDate']


admin.site.register(Business, BusinessAdmin)


class MstSectAdmin(admin.ModelAdmin):
    list_display = ['id', 'sectName', 'isActive']


admin.site.register(MstSect, MstSectAdmin)


class SaintAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'sectId', 'fatherName', 'motherName', 'birthPlace', 'dikshaPlace', 'guruName','dob', 'devlokDate', 'gender', 'description', 'isVerified']


admin.site.register(Saint, SaintAdmin)


class MstBloodGroupAdmin(admin.ModelAdmin):
    list_display = ['id', 'bloodGroupName', 'order', 'isActive']


admin.site.register(MstBloodGroup, MstBloodGroupAdmin)


class MstMaritalStatusAdmin(admin.ModelAdmin):
    list_display = ['id', 'maritalStatusName',  'order', 'isActive']


admin.site.register(MstMaritalStatus, MstMaritalStatusAdmin)


class MstRelationAdmin(admin.ModelAdmin):
    list_display = ['id', 'description', 'order', 'isActive']


admin.site.register(MstRelation,MstRelationAdmin)


class MstProfessionAdmin(admin.ModelAdmin):
    list_display = ['id', 'description', 'order', 'isActive']


admin.site.register(MstProfession, MstProfessionAdmin)