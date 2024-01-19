from django.urls import path
from .user_views import RegisterHead, RegisterMember, GETFamilyByHeadId, IsNumberExist, DeleteMemberById, UpdateUserById, GetAllResidents, GETUserDetailsById
from .auth_view import SendOTPWithNumber, VerifyOTP
# from .push_notification import CreateNewNotification

from .custom_filter import filter_queryset
from .tokens import obtain_token
# from .auth import get_payload_data_from_refresh_token

urlpatterns = [

    # to send OTP (POST)
    path('sendOTP/', SendOTPWithNumber.as_view()),

    # to verify otp (POST)
    path('verifyOTP/', VerifyOTP.as_view()),

    # to create a new 'Head' (POST)
    path('registerHead/', RegisterHead.as_view()),  # correct

    # to create a new 'member' (POST)
    path('registerMember/', RegisterMember.as_view()),  # correct

    # to get all members by headId (GET)
    path('GETFamilyByHeadId/<slug:head_id>/', GETFamilyByHeadId.as_view()),  # correct

    # to check Number exist or not (POST)
    path('checkNumberExist/', IsNumberExist.as_view()),  # correct --

    # to delete member by 'id'
    path('DELETEMemberById/<slug:user_id>/', DeleteMemberById.as_view()),  # correct

    # to update member by 'id' (PUT)
    path('UPDATEUserById/<slug:user_id>/', UpdateUserById.as_view()),  # correct

    # to get all residents (GET)
    path('GETAllResidents/', GetAllResidents.as_view()),  # correct

    # to get data by 'id' (GET)
    path('GETUserDetailsById/<slug:user_id>/', GETUserDetailsById.as_view()),  # correct

    # to create new notification (POST)
    # path('POSTNewNotification/', CreateNewNotification.as_view()),

    # (12) generate new tokens both "access" and "refresh" (POST)
    path('obtainToken/', obtain_token),

    path('filterResidentData/', filter_queryset),

    # path('GETUserId/', get_payload_data_from_refresh_token)

]
