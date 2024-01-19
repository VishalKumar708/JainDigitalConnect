from django.contrib import admin
from .models import User, OTP


class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'headId', 'name',  'relationId', 'phoneNumber', 'cityId', 'maritalStatusId', 'lookingForMatch', 'sectId',
                  'professionId', 'bloodGroupId', 'isActive', 'isAdmin', 'dob', 'nativePlace', 'gotra', 'phoneNumberVisibility', 'gender','createdBy', 'updatedBy']


admin.site.register(User, UserAdmin)


class OTPAdmin(admin.ModelAdmin):
    list_display = ['id', 'phoneNumber', 'otp', 'status', 'count', 'timestamp']


admin.site.register(OTP, OTPAdmin)


# class NotificationAdmin(admin.ModelAdmin):
#     list_display = ['id', 'id', 'title', 'body', 'screen', 'createdBy']
#
#
# admin.site.register(Notification, NotificationAdmin)


# class NotificationHistoryAdmin(admin.ModelAdmin):
#     list_display = ['id', 'userId', 'notificationId']
#
#
# admin.site.register(NotificationHistory, NotificationHistoryAdmin)

