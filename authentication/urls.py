from django.urls import path
from . import views
from .views import *

urlpatterns = [
    path('', views.ApiOverview, name='home'),
    path('create/', views.user_register, name='add-user'),
    path('profile/', views.view_profile, name='view-profile'),
    path('otp/', sendOtp, name='send-otp'),
    path('verify/', verifyOtp, name='verify-otp'),

]