from django.db import models


class BaseModel(models.Model):
    isActive = models.BooleanField(default=True)
    groupId = models.CharField(max_length=40, default=1)
    createdBy = models.CharField(max_length=50, default=1)
    updatedBy = models.CharField(max_length=50, default=1)
    createdDate = models.DateTimeField(auto_now_add=True)
    updatedDate = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class CustomUser(BaseModel, models.Model):
    userId = models.BigAutoField(primary_key=True)
    dob = models.CharField(max_length=30)
    address = models.CharField(max_length=200)
    areaId = models.CharField(max_length=10, default=1, null=True)
    bloodGroup = models.CharField(max_length=5, null=True, blank=True)
    cityId = models.CharField(max_length=10, default=1)
    currentAddress = models.CharField(max_length=200, null=True, blank=True)
    emailId = models.CharField(max_length=120, null=True, blank=True)
    fatherName = models.CharField(max_length=50)
    fmcToken = models.TextField(null=True, blank=True)
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
    relationWithHead = models.CharField(max_length=50, blank=True)
    sect = models.CharField(max_length=20)


class OTP(models.Model):
    phoneNumber = models.CharField(max_length=10)
    otp = models.CharField(max_length=6)
    status = models.CharField(default='active', max_length=10)
    count = models.IntegerField(default=0)
    timestamp = models.DateTimeField(auto_now_add=True, null=True)
