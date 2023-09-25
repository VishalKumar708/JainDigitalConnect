

from firebase_admin.messaging import Message, Notification
import logging


from rest_framework.views import APIView

from .models import User, NotificationHistory
from fcm_django.models import FCMDevice
from .serializers import CreateNewNotificationSerializer
from rest_framework.response import Response
from django.http import HttpResponse
error_logger = logging.getLogger('error')
info_logger = logging.getLogger('info')


def send_notification(title, body):
    """ To send push notification to "admin" it needs fcm_token, title, body """
    filtered_user_obj = User.objects.filter(isAdmin=True)
    if len(filtered_user_obj) > 0:
        fcm_objects = FCMDevice.objects.filter(user_id__in=filtered_user_obj)
        if len(fcm_objects) > 0:
            try:
                fcm_objects.send_message(Message(notification=Notification(title=title, body=body)))
                info_logger.info('Notification has sent successfully.')

                return True
            except Exception as e:
                error_logger.error('failed to send Notification %s', str(e))

                return False
    else:
        error_logger.error('userId not found to send Notification ')


def send_notification_to_admin(notification_obj):

    # filter user data
    filtered_user_obj = User.objects.filter(isAdmin=True)

    if len(filtered_user_obj) > 0:
        info_logger.info('User id found to get fcm_token.')

        fcm_device_obj = FCMDevice.objects.filter(user_id__in=filtered_user_obj)
        print("your fcm tokens ==> ", fcm_device_obj)

        # help to insert bulk record in "NotificationHistory" tabel
        data_to_insert = []
        for i in filtered_user_obj:
            data_to_insert.append({'userId': i, 'notificationId': notification_obj})
        # Use bulk_create to insert the data in a single query
        NotificationHistory.objects.bulk_create([NotificationHistory(**data) for data in data_to_insert])

        # check fcm_token is not None to send Notification.
        if len(fcm_device_obj) > 0:
            #  help to send "notification" to admin who has registered in database.
            try:
                fcm_device_obj.send_message(Message(notification=Notification(title=notification_obj.title, body=notification_obj.body)))
                info_logger.info('Notification has sent to all admins.')
            except Exception as e:
                error_logger.error('An error occurred while sending notification to admins %s', str(e))

        else:
            error_logger.error('FCM Device token not found to send notification.')
    else:
        error_logger.error('User not found to get fcm_token.')


class CreateNewNotification(APIView):
    def post(self, request, *args, **kwargs):
        data = request.data
        print('user_id to save notification==> ', data.get('userId'))
        user_id = data.get('userId')
        if user_id is None:
            json_data = {
                'statusCode': 400,
                'status': 'Failed',
                'data': 'Please provide userId to create Notification.'
            }
            return Response(json_data, status=400)
        else:
            try:
                user_obj = User.objects.get(userId=user_id)
            except User.DoesNotExist:
                json_data = {
                    'statusCode': 404,
                    'status': 'Failed',
                    'data': 'Please provide valid userId.'
                }
                return Response(json_data, status=404)
            serializer = CreateNewNotificationSerializer(data=data, context={'user_obj': user_obj})
            if serializer.is_valid():
                # save record
                obj = serializer.save()
                send_notification_to_admin(obj)
                json_data = {
                    'statusCode': 200,
                    'status': 'Success',
                    'data': {'msg': 'Notification Created Successfully.'}

                }
                info_logger.info('Notification Added Successfully.')

                return Response(json_data)

        # serializer error
        json_data = {
            'statusCode': 400,
            'status': 'failed',
            'data': serializer.errors
        }

        return Response(json_data, status=400)
