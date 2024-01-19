from django.db import models


class BaseModel(models.Model):
    isActive = models.BooleanField(default=True)
    groupId = models.CharField(max_length=40, default=1)
    createdDate = models.DateTimeField(auto_now_add=True)
    updatedDate = models.DateTimeField(auto_now=True)

    # createdBy = models.ForeignKey(
    #     'User',
    #     on_delete=models.CASCADE,
    #     related_name='created_by_%(class)s',
    #     null=True
    # )
    #
    # updatedBy = models.ForeignKey(
    #     'User',
    #     on_delete=models.CASCADE,
    #     related_name='updated_by_%(class)s',
    #     null=True
    # )

    # class Meta:
    #     abstract = True

