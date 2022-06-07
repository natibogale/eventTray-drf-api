from django.urls import path, include
from .api_views import *

urlpatterns = [
    # path("", APIOverview.as_view(), name="home"),
    path("api/auth/create/", UserRegisterView.as_view(), name="add-user"),
    path("api/profile/", UserProfileView.as_view(), name="view-profile"),
    path("api/auth/otp/", SendOtp.as_view(), name="send-otp"),
    path("api/auth/verify/", VerifyOTP.as_view(), name="verify-otp"),

]
