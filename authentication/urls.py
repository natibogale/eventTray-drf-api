from django.urls import path
from . import views
from .views import *

urlpatterns = [
    path('', APIOverview.as_view(), name='home'),
    path('auth/create/', UserRegisterView.as_view(), name='add-user'),
    # path('profile/', view_profile, name='view-profile'),
    path('auth/otp/', sendOtp, name='send-otp'),
    path('auth/verify/', verifyOtp, name='verify-otp'),

]