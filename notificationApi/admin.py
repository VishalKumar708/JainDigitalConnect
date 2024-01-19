from django.contrib import admin
from .models import *


class NotificationAdmin(admin.ModelAdmin):
    list_display = ['id', 'id', 'title', 'body', 'screen', 'createdBy']


admin.site.register(Notification, NotificationAdmin)


class NotificationHistoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'userId', 'notificationId']


admin.site.register(NotificationHistory, NotificationHistoryAdmin)

# Register your models here.
