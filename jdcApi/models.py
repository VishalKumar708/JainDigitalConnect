
from django.db import models
from django.utils import timezone


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
    stateId = models.ForeignKey(State, on_delete=models.CASCADE, related_name='cities')
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
    areaMC = models.CharField(max_length=70, null=True, blank=True)
    landmark = models.CharField(max_length=100, null=True, blank=True)
    areaContactNumber = models.IntegerField(null=True, blank=True)
    isVerified = models.BooleanField(default=False)

    def __str__(self):
        return self.areaName





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
    businessPhoneNumber = models.CharField(max_length=10, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    website = models.CharField(max_length=220, null=True, blank=True)
    businessDescription = models.TextField()
    isVerified = models.BooleanField(default=False)
    gstNumber = models.CharField(max_length=20, null=True, blank=True)
    address = models.CharField(max_length=120, null=True, blank=True)

    def __str__(self):
        return self.businessName


class MstSect(BaseModel):
    id = models.AutoField(primary_key=True)
    sectName = models.CharField(max_length=20, unique=True)
    order = models.IntegerField()

    def __str__(self):
        return self.sectName


class Literature(BaseModel):
    id = models.AutoField(primary_key=True)
    sectId = models.ForeignKey(MstSect, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    body = models.TextField()
    order = models.IntegerField()
    isVerified = models.BooleanField(default=False)


class Saint(BaseModel):
    GENDER_CHOICES = [
        ('Male', 'male'),
        ('Female', 'female')
    ]
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=30)
    sectId = models.ForeignKey(MstSect, on_delete=models.CASCADE, related_name='select_sect')
    fatherName = models.CharField(max_length=30)
    motherName = models.CharField(max_length=30)
    birthPlace = models.CharField(max_length=30)
    dikshaPlace = models.CharField(max_length=30)
    guruName = models.CharField(max_length=30)
    dob = models.DateField()
    dobTime = models.TimeField(null=True, blank=True)
    dikshaDate = models.DateField()
    devlokDate = models.DateField(null=True, blank=True)
    devlokTime = models.TimeField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    description = models.TextField(null=True, blank=True)
    isVerified = models.BooleanField(default=False)

    # def save(self, *args, **kwargs):
    #     # Set the time zone here before saving
    #     # self.dobTime = timezone.now()
    #     # self.devlokTime = timezone.now()
    #     super().save(*args, **kwargs)

# class SaintFamily(BaseModel):
#     id = models.BigAutoField(primary_key=True)
#     saintId = models.ForeignKey(Saint, on_delete=models.CASCADE, related_name='saintFamilyMembers')
#     name = models.CharField(max_length=50)


class Emergency(BaseModel):
    id = models.BigAutoField(primary_key=True)
    cityId = models.ForeignKey(City, on_delete=models.CASCADE, related_name='cities')
    departmentName = models.CharField(max_length=30)
    phoneNumber = models.CharField(max_length=15, null=True)
    email = models.EmailField(null=True, blank=True)
    website = models.CharField(max_length=255, null=True, blank=True)
    isVerified = models.BooleanField(default=False)


#  Master tables
class MstBloodGroup(BaseModel):
    id = models.BigAutoField(primary_key=True)
    bloodGroupName = models.CharField(max_length=7, unique=True)
    order = models.IntegerField()


class MstMaritalStatus(BaseModel):
    id = models.BigAutoField(primary_key=True)
    maritalStatusName = models.CharField(max_length=20, unique=True)
    order = models.IntegerField()


class MstRelation(BaseModel):
    id = models.BigAutoField(primary_key=True)
    description = models.CharField(max_length=40, unique=True)
    order = models.IntegerField()


class MstProfession(BaseModel):
    id = models.BigAutoField(primary_key=True)
    description = models.CharField(max_length=50, unique=True)
    order = models.IntegerField()






