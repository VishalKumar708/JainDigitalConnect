from django.contrib import admin
from .models import CustomUser, OTP


class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['userId', 'headId', 'name',  'relationWithHead', 'phoneNumber', 'maritalStatus', 'lookingForMatch', 'sect',
                  'profession', 'bloodGroup', 'dob', 'nativePlace', 'gotra', 'phoneNumberVisibility', 'gender','createdBy']


admin.site.register(CustomUser, CustomUserAdmin)


class OTPAdmin(admin.ModelAdmin):
    list_display = ['id', 'phoneNumber', 'otp', 'status', 'count', 'timestamp']


admin.site.register(OTP, OTPAdmin)