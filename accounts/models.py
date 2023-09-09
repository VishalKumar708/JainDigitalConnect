from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from .manager import CustomUserManager


class BaseModel(models.Model):
    isActive = models.BooleanField(default=False)
    groupId = models.CharField(max_length=40, default=1)
    createdBy = models.CharField(max_length=50, default=1)
    updatedBy = models.CharField(max_length=50, default=1)
    createdDate = models.DateTimeField(auto_now_add=True)
    updatedDate = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class CustomUser(AbstractBaseUser, BaseModel):
    userId = models.BigAutoField(primary_key=True)
    dob = models.DateField()
    address = models.CharField(max_length=200)
    areaId = models.CharField(max_length=10, default=1, null=True)
    bloodGroup = models.CharField(max_length=5, null=True, blank=True)
    cityId = models.CharField(max_length=10, default=1)
    currentAddress = models.CharField(max_length=200, null=True)
    emailId = models.CharField(max_length=120, null=True, blank=True)
    fatherName = models.CharField(max_length=50)
    fmcToken = models.TextField(null=True)
    gender = models.CharField(max_length=10)
    gotra = models.CharField(max_length=30, null=True, blank=True)
    headId = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL)
    lookingForMatch = models.BooleanField(default=False)
    maritalStatus = models.CharField(max_length=15)
    name = models.CharField(max_length=50, null=True)
    nativePlace = models.CharField(max_length=30, null=True, blank=True)
    phoneNumber = models.CharField(max_length=12, unique=True)
    phoneNumberVisibility = models.BooleanField(default=True)
    profession = models.CharField(max_length=20, null=True)
    relationWithHead = models.CharField(max_length=50)
    sect = models.CharField(max_length=20)

    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'phoneNumber'
    REQUIRED_FIELDS = ['dob', 'address']

    def __str__(self):
        return str(self.phoneNumber)

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True


class OTP(models.Model):
    phoneNumber = models.CharField(max_length=10)
    otp = models.CharField(max_length=6)
    status = models.CharField(default='active', max_length=10)
    count = models.IntegerField(default=0)
    timestamp = models.DateTimeField(auto_now_add=True, null=True)
