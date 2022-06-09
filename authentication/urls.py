from django.urls import path, include
from .views import *
from .api_views import *

urlpatterns = [

    #All authentication urls api
    path("api/auth/create/", UserRegisterView.as_view(), name="add-user"),
    path("api/user/profile/", UserProfileView.as_view(), name="view-profile"),
    path("api/auth/otp/", SendOtp.as_view(), name="send-otp"),
    path("api/auth/verify/", VerifyOTP.as_view(), name="verify-otp"),


    path("api/organizer/profile/", OrganizerProfileView.as_view(), name="view-profile-org"),
    path("api/organizer/organizer-details/", OrganizerDetailView.as_view(), name="view-details-org"),





    # Organizer no api urls

    path("", home, name="home"),
    path("verify/otp", verifyOtp, name="verify-otp"),
    path('organizer/', include('organizer.urls')),
]
