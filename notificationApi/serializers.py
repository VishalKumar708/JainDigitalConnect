
from rest_framework import serializers
from .models import Notification


class CreateNewNotificationSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ['userId', 'title', 'body', 'screen', 'type']
        model = Notification

    def create(self, validated_data):
        user_obj = self.context.get('user_obj')
        print('In serializer user object==> ', user_obj)
        # created_by_user = request.user if request else validated_data['userId']
        print("user_obj.id==> ", user_obj.id)
        created_by_user = user_obj.id
        validated_data['createdBy'] = created_by_user

        # Create the user instance with modified data
        user = self.Meta.model.objects.create(**validated_data)

        return user

