
from django.db import models


class BaseModel(models.Model):
    isActive = models.BooleanField(default=False)
    groupId = models.CharField(max_length=40, default=1)
    createdBy = models.CharField(max_length=50, default=1)
    updatedBy = models.CharField(max_length=50, default=1)
    createdDate = models.DateTimeField(auto_now_add=True)
    updatedDate = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

# Create your models here.


class State(BaseModel, models.Model):
    stateId = models.AutoField(primary_key=True)
    stateName = models.CharField(max_length=50)
    isVerified = models.BooleanField(default=False)

    def __str__(self):
        return self.stateName


class City(BaseModel, models.Model):
    cityId = models.AutoField(primary_key=True)
    stateId = models.ForeignKey(State, on_delete=models.CASCADE, related_name='city_by_state')
    cityName = models.CharField(max_length=70)
    pincode = models.CharField(max_length=6)
    description = models.CharField(max_length=100, null=True)
    isVerified = models.BooleanField(default=False)
    isActiveForResidents = models.BooleanField(default=False)

    def __str__(self):
        return self.cityName


class Area(BaseModel, models.Model):
    areaId = models.AutoField(primary_key=True)
    cityId = models.ForeignKey(City, on_delete=models.CASCADE, related_name='GetAllAreaByCityId')
    areaName = models.CharField(max_length=70)
    areaMC = models.CharField(max_length=70, null=True)
    landmark = models.CharField(max_length=100, null=True)
    areaContactNumber = models.IntegerField(null=True)
    isVerified = models.BooleanField(default=False)

    def __str__(self):
        return self.areaName


class Literature(BaseModel, models.Model):
    literatureId = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    body = models.TextField()
    isVerified = models.BooleanField(default=False)


class Aarti(BaseModel, models.Model):
    aartiId = models.AutoField(primary_key=True)
    aartiName = models.CharField(max_length=200)
    aartiText = models.TextField()
    isVerified = models.BooleanField(default=False)


from accounts.models import User

class Business(BaseModel):
    businessId = models.AutoField(primary_key=True)
    cityId = models.ForeignKey(City, on_delete=models.CASCADE, related_name='GetAllBusinessByCityId')
    userId = models.ForeignKey(User, on_delete=models.CASCADE, related_name='GetAllBusinessByUserId')
    businessName = models.CharField(max_length=200)
    businessType = models.CharField(max_length=120)
    businessPhoneNumber = models.CharField(max_length=10, null=True, )
    email = models.EmailField(null=True)
    website = models.CharField(max_length=220, null=True)
    businessDescription = models.TextField()
    isVerified = models.BooleanField(default=False)
    gstNumber = models.CharField(max_length=20)
    address = models.CharField(max_length=120)

    def __str__(self):
        return self.businessName











