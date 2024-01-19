from django.db import models
from masterApi.models import BaseModel


class Notification(BaseModel):
    userId = models.ForeignKey('accounts.User', on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    body = models.TextField()
    screen = models.CharField(max_length=100)
    type = models.CharField(max_length=100)

    createdBy = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='created_notifications')
    updatedBy = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='updated_notifications')

    def __str__(self):
        return str(self.id)


class NotificationHistory(BaseModel):
    userId = models.ForeignKey('accounts.User', on_delete=models.CASCADE)
    notificationId = models.ForeignKey(Notification, on_delete=models.CASCADE)

    createdBy = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='created_notification_histories')
    updatedBy = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='updated_notification_histories')


# Create your models here.
