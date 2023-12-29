from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
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
    name = models.CharField(max_length=50)
    phoneNumber = models.CharField(max_length=12)
    # cityId = models.CharField(max_length=10, default=1)
    cityId = models.IntegerField()
    # areaId = models.CharField(max_length=10, default=1, null=True)
    areaId = models.IntegerField()
    # sect = models.CharField(max_length=20)
    sectId = models.IntegerField()
    phoneNumberVisibility = models.BooleanField(default=True)
    gender = models.CharField(max_length=10)
    headId = models.IntegerField(null=True, default=None, blank=True)

    gotra = models.CharField(max_length=30, null=True, blank=True)
    # bloodGroup = models.CharField(max_length=5, null=True, blank=True)
    bloodGroupId = models.IntegerField(null=True, blank=True)
    nativePlace = models.CharField(max_length=30, null=True, blank=True)
    currentAddress = models.CharField(max_length=200, null=True, blank=True)
    fatherName = models.CharField(max_length=50, null=True, blank=True)
    permanentAddress = models.CharField(max_length=200, null=True, blank=True)
    # maritalStatus = models.CharField(max_length=15, null=True)
    maritalStatusId = models.IntegerField(null=True, blank=True)
    lookingForMatch = models.BooleanField(default=False)
    dob = models.DateField(null=True, blank=True)
    # profession = models.CharField(max_length=20, null=True, blank=True)
    professionId = models.IntegerField(null=True, blank=True)
    # relationWithHead = models.CharField(max_length=50, blank=True)
    relationId = models.IntegerField(null=True, blank=True)

    email = models.CharField(max_length=120, null=True, blank=True)
    isAdmin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = "id"
    REQUIRED_FIELDS = ['name', 'phoneNumber', 'dob', 'currentAddress']
    objects = UserManager()

    # def has_module_perms(self):
    #     return True

    def __str__(self):
        return str(self.id)

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


