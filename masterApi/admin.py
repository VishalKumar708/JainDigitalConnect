from django.contrib import admin
from .models import *


class MstSectAdmin(admin.ModelAdmin):
    list_display = ['id', 'sectName', 'isActive', 'createdBy', 'updatedBy']


admin.site.register(MstSect, MstSectAdmin)


class MstBloodGroupAdmin(admin.ModelAdmin):
    list_display = ['id', 'bloodGroupName', 'order', 'isActive', 'createdBy', 'updatedBy']


admin.site.register(MstBloodGroup, MstBloodGroupAdmin)


class MstMaritalStatusAdmin(admin.ModelAdmin):
    list_display = ['id', 'maritalStatusName',  'order', 'isActive', 'createdBy', 'updatedBy']


admin.site.register(MstMaritalStatus, MstMaritalStatusAdmin)


class MstRelationAdmin(admin.ModelAdmin):
    list_display = ['id', 'description', 'order', 'isActive', 'createdBy', 'updatedBy']


admin.site.register(MstRelation,MstRelationAdmin)


class MstProfessionAdmin(admin.ModelAdmin):
    list_display = ['id', 'description', 'order', 'isActive', 'createdBy', 'updatedBy']


admin.site.register(MstProfession, MstProfessionAdmin)


class FeedbackTitleAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'order', 'isActive', 'createdBy', 'updatedBy']


admin.site.register(MstFeedbackTitle, FeedbackTitleAdmin)
# Register your models here.
