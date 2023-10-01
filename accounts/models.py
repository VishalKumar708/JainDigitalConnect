from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.db import models
from .manager import UserManager


class BaseModel(models.Model):
    isActive = models.BooleanField(default=True)
    groupId = models.CharField(max_length=40, default=1)
    createdBy = models.CharField(max_length=50, default=1)
    updatedBy = models.CharField(max_length=50, default=1)
    createdDate = models.DateTimeField(auto_now_add=True)
    updatedDate = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class User(BaseModel, AbstractBaseUser, PermissionsMixin):
    id = models.BigAutoField(primary_key=True)
    dob = models.DateField()
    address = models.CharField(max_length=200)
    areaId = models.CharField(max_length=10, default=1, null=True)
    bloodGroup = models.CharField(max_length=5, null=True, blank=True)
    cityId = models.CharField(max_length=10, default=1)
    currentAddress = models.CharField(max_length=200, null=True, blank=True)
    emailId = models.CharField(max_length=120, null=True, blank=True)
    fatherName = models.CharField(max_length=50)
    # fcmToken = models.TextField(null=True, blank=True)
    gender = models.CharField(max_length=10)
    gotra = models.CharField(max_length=30, null=True, blank=True)
    # headId = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL)
    headId = models.IntegerField(null=True, default=None, blank=True)
    lookingForMatch = models.BooleanField(default=False)
    maritalStatus = models.CharField(max_length=15)
    name = models.CharField(max_length=50)
    nativePlace = models.CharField(max_length=30, null=True, blank=True)
    phoneNumber = models.CharField(max_length=12)
    phoneNumberVisibility = models.BooleanField(default=True)
    profession = models.CharField(max_length=20, null=True, blank=True)
    relationWithHead = models.CharField(max_length=50)
    sect = models.CharField(max_length=20)
    isAdmin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = "id"
    REQUIRED_FIELDS = ['name', 'phoneNumber', 'dob', 'address']
    objects = UserManager()

    # def has_module_perms(self):
    #     return True

    def __str__(self):
        return str(self.phoneNumber)

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True


class OTP(models.Model):
    phoneNumber = models.CharField(max_length=10)
    otp = models.CharField(max_length=6)
    status = models.CharField(default='active', max_length=10)
    count = models.IntegerField(default=0)
    timestamp = models.DateTimeField(auto_now_add=True, null=True)


class Notification(BaseModel):
    userId = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notification')
    title = models.CharField(max_length=100)
    body = models.TextField()
    screen = models.CharField(max_length=100)
    type = models.CharField(max_length=100)

    def __str__(self):
        return str(self.id)


class NotificationHistory(BaseModel):
    userId = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
    notificationId = models.ForeignKey(Notification, on_delete=models.CASCADE, related_name='notification')


