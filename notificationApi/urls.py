from django.urls import path
from .push_notification import *


urlpatterns = [
    path('POSTNewNotification/', CreateNewNotification.as_view()),
]
