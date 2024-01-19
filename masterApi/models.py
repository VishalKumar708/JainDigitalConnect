from django.db import models


class BaseModel(models.Model):
    isActive = models.BooleanField(default=True)
    groupId = models.CharField(max_length=40, default=1)
    createdDate = models.DateTimeField(auto_now_add=True)
    updatedDate = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


#  Sect
class MstSect(BaseModel):
    id = models.AutoField(primary_key=True)
    sectName = models.CharField(max_length=20, unique=True)
    order = models.IntegerField()

    createdBy = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, related_name='created_sects', null=True)
    updatedBy = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, related_name='updated_sects', null=True)

    def __str__(self):
        return self.sectName


#  BloodGroup
class MstBloodGroup(BaseModel):
    id = models.BigAutoField(primary_key=True)
    bloodGroupName = models.CharField(max_length=7, unique=True)
    order = models.IntegerField()

    createdBy = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, related_name='created_blood_groups', null=True)
    updatedBy = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, related_name='updated_blood_groups', null=True)


#  MaritalStatus
class MstMaritalStatus(BaseModel):
    id = models.BigAutoField(primary_key=True)
    maritalStatusName = models.CharField(max_length=20, unique=True)
    order = models.IntegerField()

    createdBy = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, related_name='created_marital_status', null=True)
    updatedBy = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, related_name='updated_marital_status', null=True)


# Relation
class MstRelation(BaseModel):
    id = models.BigAutoField(primary_key=True)
    description = models.CharField(max_length=40, unique=True)
    order = models.IntegerField()

    createdBy = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, related_name='created_relations', null=True)
    updatedBy = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, related_name='updated_relations', null=True)


#  Profession
class MstProfession(BaseModel):
    id = models.BigAutoField(primary_key=True)
    description = models.CharField(max_length=50, unique=True)
    order = models.IntegerField()

    createdBy = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, related_name='created_professions', null=True)
    updatedBy = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, related_name='updated_professions', null=True)


#  feedback title
class MstFeedbackTitle(BaseModel):
    id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=100)
    order = models.IntegerField()

    createdBy = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, related_name='created_feedback_titles', null=True)
    updatedBy = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, related_name='updated_feedback_titles', null=True)
# Create your models here.

