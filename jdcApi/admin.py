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
    list_display = ['id', 'title', 'body', 'isVerified', 'isActive', 'groupId', 'createdBy', 'updatedBy', 'createdDate','updatedDate']


admin.site.register(Literature,LiteratureAdmin)


class AartiAdmin(admin.ModelAdmin):
    list_display = ['id', 'aartiName', 'sectId', 'aartiText', 'isVerified', 'isActive', 'groupId', 'createdBy', 'updatedBy', 'createdDate','updatedDate']


admin.site.register(Aarti, AartiAdmin)


class BusinessAdmin(admin.ModelAdmin):
    list_display = ['businessId', 'userId', 'cityId', 'businessName','businessType','businessPhoneNumber', 'email', 'website', 'businessDescription', 'isVerified', 'isActive', 'groupId', 'createdBy', 'updatedBy', 'createdDate', 'updatedDate']


admin.site.register(Business, BusinessAdmin)


# class MstSectAdmin(admin.ModelAdmin):
#     list_display = ['id', 'sectName', 'isActive']
#
#
# admin.site.register(MstSect, MstSectAdmin)


class SaintAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'sectId', 'fatherName', 'motherName', 'birthPlace', 'dikshaPlace', 'guruName','dob','dobTime', 'devlokDate','devlokTime', 'gender', 'description', 'isVerified']


admin.site.register(Saint, SaintAdmin)


# class MstBloodGroupAdmin(admin.ModelAdmin):
#     list_display = ['id', 'bloodGroupName', 'order', 'isActive']
#
#
# admin.site.register(MstBloodGroup, MstBloodGroupAdmin)
#
#
# class MstMaritalStatusAdmin(admin.ModelAdmin):
#     list_display = ['id', 'maritalStatusName',  'order', 'isActive']
#
#
# admin.site.register(MstMaritalStatus, MstMaritalStatusAdmin)
#
#
# class MstRelationAdmin(admin.ModelAdmin):
#     list_display = ['id', 'description', 'order', 'isActive']
#
#
# admin.site.register(MstRelation,MstRelationAdmin)
#
#
# class MstProfessionAdmin(admin.ModelAdmin):
#     list_display = ['id', 'description', 'order', 'isActive']
#
#
# admin.site.register(MstProfession, MstProfessionAdmin)
#

class EmergencyAdmin(admin.ModelAdmin):
    list_display = ['id', 'departmentName', 'phoneNumber', 'email', 'website', 'isVerified', 'isActive']


admin.site.register(Emergency, EmergencyAdmin)


class DharamSthanAdmin(admin.ModelAdmin):
    list_display = ['id','name', 'cityId', 'sectId', 'address', 'locationLink', 'postalCode', 'foundationDate', 'accountNumber', 'ifscCode', 'upiId', 'isActive', 'isVerified']


admin.site.register(DharamSthan, DharamSthanAdmin)


class DharamSthanMemberAdmin(admin.ModelAdmin):
    list_display = ['id', 'dharamSthanId', 'position', 'phoneNumber', 'isVerified', 'isActive']


admin.site.register(DharamSthanMember, DharamSthanMemberAdmin)


class EventAdmin(admin.ModelAdmin):
    list_display = ['id', 'cityId', 'sectId', 'startDate', 'endDate', 'title', 'body', 'isVerified', 'isActive', 'createdDate']


admin.site.register(Event, EventAdmin)


class DharamSthanHistoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'dharamSthanId', "year", 'startDate', 'endDate', 'title', 'body', 'isActive']


admin.site.register(DharamSthanHistory, DharamSthanHistoryAdmin)


class LiveLocationAdmin(admin.ModelAdmin):
    list_display = ['id', 'sectId', 'title', 'person1Name', 'phoneNumber1', 'person2Name', 'phoneNumber2', 'startDate',
                    'endDate', 'locationLink', 'address', 'description', 'isVerified']


admin.site.register(LiveLocation, LiveLocationAdmin)


class LiteratureDocumentAdmin(admin.ModelAdmin):
    list_display = ['id', 'sectId', 'title', 'order', 'link', 'file', 'isVerified', 'isActive']


admin.site.register(LiteratureDocument, LiteratureDocumentAdmin)


class AppConfigurationsAdmin(admin.ModelAdmin):
    list_display = ['id', 'configurationKey', 'configurationValue', 'createdBy', 'updatedBy', 'createdDate', 'updatedDate']


admin.site.register(AppConfigurations, AppConfigurationsAdmin)


# class FeedbackTitleAdmin(admin.ModelAdmin):
#     list_display = ['id', 'title', 'order', 'isActive', 'createdBy', 'updatedBy']
#
#
# admin.site.register(MstFeedbackTitle, FeedbackTitleAdmin)


class FeedbackAdmin(admin.ModelAdmin):
    list_display = ['id', 'feedbackTitleId', 'body', 'createdBy', 'updatedBy']


admin.site.register(Feedback, FeedbackAdmin)