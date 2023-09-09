from django.urls import path
from .views import SendOTPWithNumber, VerifyOTP
urlpatterns = [
    path('sendOTP/', SendOTPWithNumber.as_view()),
    path('verifyOTP/', VerifyOTP.as_view())
]