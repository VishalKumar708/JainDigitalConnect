from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from .manager import UserManager
from phonenumber_field.modelfields import PhoneNumberField
# from utils.base_model import BaseModel


class BaseModel(models.Model):
    isActive = models.BooleanField(default=True)
    groupId = models.CharField(max_length=40, default=1)
    createdBy = models.ForeignKey('User', on_delete=models.SET_NULL, related_name='created_by_me', null=True)
    updatedBy = models.ForeignKey('User', on_delete=models.SET_NULL, related_name='updated_by_me', null=True)
    # createdBy = models.CharField(max_length=50, default=1)
    # updatedBy = models.CharField(max_length=50, default=1)
    createdDate = models.DateTimeField(auto_now_add=True)
    updatedDate = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class User(BaseModel, AbstractBaseUser, PermissionsMixin):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=50)
    # phoneNumber = models.CharField(max_length=12)
    phoneNumber = PhoneNumberField()
    # cityId = models.IntegerField()
    cityId = models.ForeignKey('jdcApi.City', models.CASCADE, null=True)
    # areaId = models.IntegerField()
    areaId = models.ForeignKey('jdcApi.Area', models.CASCADE, null=True)

    # sectId = models.IntegerField()
    sectId = models.ForeignKey('masterApi.MstSect', models.CASCADE, null=True)

    phoneNumberVisibility = models.BooleanField(default=True)
    gender = models.CharField(max_length=10)
    # headId = models.IntegerField(null=True, default=None, blank=True)
    headId = models.ForeignKey('self', on_delete=models.SET_NULL, related_name='family_members', null=True, blank=True)

    gotra = models.CharField(max_length=30, null=True, blank=True)

    # bloodGroupId = models.IntegerField(null=True, blank=True)
    bloodGroupId = models.ForeignKey('masterApi.MstBloodGroup', on_delete= models.SET_NULL, null=True, blank=True)

    nativePlace = models.CharField(max_length=30, null=True, blank=True)
    currentAddress = models.CharField(max_length=200, null=True, blank=True)
    fatherName = models.CharField(max_length=50, null=True, blank=True)
    permanentAddress = models.CharField(max_length=200, null=True, blank=True)

    # maritalStatusId = models.IntegerField(null=True, blank=True)
    maritalStatusId = models.ForeignKey('masterApi.MstMaritalStatus', on_delete= models.SET_NULL, null=True, blank=True)

    lookingForMatch = models.BooleanField(default=False)
    dob = models.DateField(null=True, blank=True)

    # professionId = models.IntegerField(null=True, blank=True)
    professionId = models.ForeignKey('masterApi.MstProfession', on_delete=models.SET_NULL, null=True, blank=True)

    # relationId = models.IntegerField(null=True, blank=True)
    relationId = models.ForeignKey('masterApi.MstRelation',on_delete= models.SET_NULL, null=True)
    isVerified = models.BooleanField(default=False)
    # email = models.CharField(max_length=120, null=True, blank=True)
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



