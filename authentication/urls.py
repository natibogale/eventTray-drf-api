from django.urls import path
from . import views
from .views import *

urlpatterns = [
    path("", APIOverview.as_view(), name="home"),
    path("auth/create/", UserRegisterView.as_view(), name="add-user"),
    path("profile/", UserProfileView.as_view(), name="view-profile"),
    path("auth/otp/", sendOtp, name="send-otp"),
    path("auth/verify/", VerifyOTP.as_view(), name="verify-otp"),
]
