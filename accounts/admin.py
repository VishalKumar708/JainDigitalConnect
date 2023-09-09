from django.contrib import admin
from .models import CustomUser, OTP


class CustomUserAdmin(admin.ModelAdmin):
    pass


admin.site.register(CustomUser, CustomUserAdmin)


class OTPAdmin(admin.ModelAdmin):
    list_display = ['id', 'phoneNumber', 'otp', 'status', 'count', 'timestamp']


admin.site.register(OTP, OTPAdmin)