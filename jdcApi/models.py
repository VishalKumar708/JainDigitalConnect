from django.core.validators import MaxValueValidator
from django.db import models
from django.utils import timezone
from django.core.validators import FileExtensionValidator
from masterApi.models import MstSect, MstFeedbackTitle
from phonenumber_field.modelfields import PhoneNumberField


class BaseModel(models.Model):
    isActive = models.BooleanField(default=False)
    groupId = models.CharField(max_length=40, default=1)
    # createdBy = models.CharField(max_length=50, default=1)
    # updatedBy = models.CharField(max_length=50, default=1)
    createdDate = models.DateTimeField(auto_now_add=True)
    updatedDate = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

# Create your models here.


class State(BaseModel, models.Model):
    stateId = models.AutoField(primary_key=True)
    stateName = models.CharField(max_length=50)
    isVerified = models.BooleanField(default=False)
    createdBy = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, related_name='created_state',
                                  null=True)
    updatedBy = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, related_name='updated_state',
                                  null=True)

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
    createdBy = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, related_name='created_city',
                                  null=True)
    updatedBy = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, related_name='updated_city',
                                  null=True)

    def __str__(self):
        return self.cityName


class Area(BaseModel, models.Model):
    areaId = models.AutoField(primary_key=True)
    cityId = models.ForeignKey(City, on_delete=models.CASCADE, related_name='GetAllAreaByCityId')
    areaName = models.CharField(max_length=70)
    areaMC = models.CharField(max_length=70, null=True, blank=True)
    landmark = models.CharField(max_length=100, null=True, blank=True)
    areaContactNumber = PhoneNumberField(null=True, blank=True)
    isVerified = models.BooleanField(default=False)
    createdBy = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, related_name='created_area',
                                  null=True)
    updatedBy = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, related_name='updated_area',
                                  null=True)

    def __str__(self):
        return self.areaName


from accounts.models import User


class Business(BaseModel):
    businessId = models.AutoField(primary_key=True)
    cityId = models.ForeignKey(City, on_delete=models.CASCADE, related_name='GetAllBusinessByCityId')
    userId = models.ForeignKey(User, on_delete=models.CASCADE, related_name='GetAllBusinessByUserId')
    businessName = models.CharField(max_length=200)
    businessType = models.CharField(max_length=120)
    businessPhoneNumber = PhoneNumberField(null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    website = models.CharField(max_length=220, null=True, blank=True)
    businessDescription = models.TextField()
    isVerified = models.BooleanField(default=False)
    gstNumber = models.CharField(max_length=20, null=True, blank=True)
    address = models.CharField(max_length=120, null=True, blank=True)
    createdBy = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='created_business',
                                  null=True)
    updatedBy = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='updated_business',
                                  null=True)

    def __str__(self):
        return self.businessName


class Aarti(BaseModel, models.Model):
    id = models.AutoField(primary_key=True)
    aartiName = models.CharField(max_length=200)
    sectId = models.ForeignKey(MstSect, on_delete=models.CASCADE)
    order = models.IntegerField()
    aartiText = models.TextField()
    isVerified = models.BooleanField(default=False)

    createdBy = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, related_name='created_aarti', null=True)
    updatedBy = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, related_name='updated_aarti', null=True)

    def __str__(self):
        return str(self.id)


class DharamSthan(BaseModel):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=200)
    cityId = models.ForeignKey(City, on_delete=models.CASCADE)
    sectId = models.ForeignKey(MstSect, on_delete=models.CASCADE)
    address = models.CharField(max_length=200)
    locationLink = models.TextField(blank=True, null=True)
    postalCode = models.CharField(max_length=10)
    foundationDate = models.DateField(null=True, blank=True)
    accountNumber = models.CharField(max_length=30, null=True, blank=True)
    ifscCode = models.CharField(max_length=30, null=True, blank=True)
    upiId = models.CharField(max_length=50, null=True, blank=True)
    isVerified = models.BooleanField(default=False)
    createdBy = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, related_name='created_dharam_sthan',
                                  null=True)
    updatedBy = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, related_name='updated_dharam_sthan',
                                  null=True)

    def __str__(self):
        return str(self.id)+str(self.name)


class DharamSthanMember(BaseModel):
    id = models.BigAutoField(primary_key=True)
    dharamSthanId = models.ForeignKey(DharamSthan, on_delete=models.CASCADE)
    name= models.CharField(max_length=50, null=True)
    position = models.CharField(max_length=50)
    phoneNumber = PhoneNumberField()
    isVerified = models.BooleanField(default=False)
    createdBy = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, related_name='created_dharam_sthan_member',
                                  null=True)
    updatedBy = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, related_name='updated_dharam_sthan_member',
                                  null=True)


class DharamSthanHistory(BaseModel):
    id = models.BigAutoField(primary_key=True)
    dharamSthanId = models.ForeignKey(DharamSthan, on_delete=models.CASCADE)
    year = models.IntegerField(validators=[MaxValueValidator(9999)])  # Setting a maximum value for the year field
    startDate = models.DateField()
    endDate = models.DateField()
    title = models.CharField(max_length=50)
    body = models.TextField()
    # isVerified = models.BooleanField(default=False)
    createdBy = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, related_name='created_dharam_sthan_history', null=True)
    updatedBy = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, related_name='updated_dharam_sthan_history', null=True)


class LiveLocation(BaseModel):
    id = models.BigAutoField(primary_key=True)
    sectId = models.ForeignKey(MstSect, on_delete=models.CASCADE)
    title = models.CharField(max_length=70)
    person1Name = models.CharField(max_length=50)
    phoneNumber1 = PhoneNumberField()
    person2Name = models.CharField(max_length=50, null=True, blank=True)
    phoneNumber2 = PhoneNumberField(null=True, blank=True)
    startDate = models.DateField()
    endDate = models.DateField()
    locationLink = models.TextField()
    address = models.CharField(max_length=100)
    description = models.TextField()
    isVerified = models.BooleanField(default=False)
    createdBy = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, related_name='created_live_location', null=True)
    updatedBy = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, related_name='updated_live_location', null=True)


class Literature(BaseModel):
    id = models.AutoField(primary_key=True)
    sectId = models.ForeignKey(MstSect, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    body = models.TextField()
    order = models.IntegerField()
    isVerified = models.BooleanField(default=False)
    createdBy = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, related_name='created_literature', null=True)
    updatedBy = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, related_name='updated_literature', null=True)


class Saint(BaseModel):
    GENDER_CHOICES = [
        ('Male', 'male'),
        ('Female', 'female')
    ]
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=30)
    sectId = models.ForeignKey(MstSect, on_delete=models.CASCADE, related_name='all_saint')
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
    createdBy = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='created_saint', null=True)
    updatedBy = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='updated_saint', null=True)


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
    createdBy = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, related_name='created_emergency', null=True)
    updatedBy = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, related_name='updated_emergency', null=True)


class Event(BaseModel):
    id = models.BigAutoField(primary_key=True)
    cityId = models.ForeignKey(City, on_delete=models.CASCADE)
    sectId = models.ForeignKey(MstSect, on_delete=models.CASCADE)
    startDate = models.DateField()
    endDate = models.DateField()
    title = models.CharField(max_length=100)
    body = models.TextField()
    isVerified = models.BooleanField(default=False)
    createdBy = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, related_name='created_event', null=True)
    updatedBy = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, related_name='updated_event', null=True)


class AppConfigurations(models.Model):
    id = models.BigAutoField(primary_key=True)
    configurationKey = models.CharField(max_length=50, unique=True)
    configurationValue = models.BooleanField()
    createdBy = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, related_name='created_app_configuration', null=True)
    updatedBy = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, related_name='updated_app_configuration', null=True)
    createdDate = models.DateTimeField(auto_now_add=True)
    updatedDate = models.DateTimeField(auto_now=True)


class LiteratureDocument(BaseModel):
    id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=100, null=True)
    sectId = models.ForeignKey(MstSect, on_delete=models.CASCADE)
    order = models.IntegerField()
    link = models.TextField(null=True, blank=True)
    file = models.FileField(upload_to='literature_Documents', null=True,
                            validators=[FileExtensionValidator(allowed_extensions=['txt', 'pdf', 'jpeg', 'png'])], blank = True)
    isVerified = models.BooleanField(default=False)
    createdBy = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, related_name='created_literature_document', null=True)
    updatedBy = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, related_name='updated_literature_document', null=True)


class Feedback(models.Model):
    id = models.BigAutoField(primary_key=True)
    feedbackTitleId = models.ForeignKey(MstFeedbackTitle, on_delete=models.CASCADE, related_name='feedbackTitles')
    body = models.TextField()
    createdBy = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='created_feedback', null=True)
    updatedBy = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='updated_feedback', null=True)
    createdDate = models.DateTimeField(auto_now_add=True)
    updatedDate = models.DateTimeField(auto_now=True)



