from django.urls import path
from .user_views import RegisterHead, RegisterMember, GETFamilyByHeadId, IsUserExist, DeleteMember, UpdateUserById, GetAllResidents, GETUserById
from .auth_view import SendOTPWithNumber, VerifyOTP
urlpatterns = [

    path('sendOTP/', SendOTPWithNumber.as_view()),
    path('verifyOTP/', VerifyOTP.as_view()),
    path('registerHead/', RegisterHead.as_view()),
    path('registerMember/', RegisterMember.as_view()),
    path('GETFamilyByHeadId/<slug:head_id>/', GETFamilyByHeadId.as_view()),
    path('checkNumberExist/', IsUserExist.as_view()),
    path('DELETEMember/<slug:member_id>/', DeleteMember.as_view()),
    path('UPDATEUserById/<slug:user_id>/', UpdateUserById.as_view()),
    path('GETAllResidents/', GetAllResidents.as_view()),
    path('GETUserById/<slug:user_id>/', GETUserById.as_view())



]