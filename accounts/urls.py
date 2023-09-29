from django.urls import path
from .user_views import RegisterHead, RegisterMember, GETFamilyByHeadId, IsUserExist, DeleteMember, UpdateUserById, GetAllResidents, GETUserById
from .auth_view import SendOTPWithNumber, VerifyOTP
from .push_notification import CreateNewNotification

from .custom_filter import filter_queryset
from .tokens import obtain_token
# from .auth import get_payload_data_from_refresh_token
urlpatterns = [

    # to send OTP (POST)
    path('sendOTP/', SendOTPWithNumber.as_view()),

    # to verify otp (POST)
    path('verifyOTP/', VerifyOTP.as_view()),

    # to create a new 'Head' (POST)
    path('registerHead/', RegisterHead.as_view()),

    # to create a new 'member' (POST)
    path('registerMember/', RegisterMember.as_view()),

    # to get all members by headId (GET)
    path('GETFamilyByHeadId/<slug:head_id>/', GETFamilyByHeadId.as_view()),

    # to check Number exist or not (POST)
    path('checkNumberExist/', IsUserExist.as_view()),

    # to delete member by 'id' (GET)
    path('DELETEMember/<slug:member_id>/', DeleteMember.as_view()),

    # to update member by 'id' (GET)
    path('UPDATEUserById/<slug:member_id>/', UpdateUserById.as_view()),

    # to get all residents (GET)
    path('GETAllResidents/', GetAllResidents.as_view()),

    # to get data by 'id' (GET)
    path('GETUserById/<slug:user_id>/', GETUserById.as_view()),

    # to create new notification (POST)
    path('POSTNewNotification/', CreateNewNotification.as_view()),

    # (12) generate new tokens both "access" and "refresh" (POST)
    path('obtainToken/', obtain_token),

    path('filterResidentData/', filter_queryset),

    # path('GETUserId/', get_payload_data_from_refresh_token)

]
