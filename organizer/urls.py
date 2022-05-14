from . import views
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import *

urlpatterns = [
    #  path('record-officer/', views.record_officer_view, name="record-officer"),
    #  path('director/', views.director_view, name="director"),
    #  path('human-resources/', views.hr_view, name="hr"),
     path('', views.organizerHome,name="organizer-home"),
     path('setup/', views.organizerSetup,name="organizer-setup"),
     path('profile/<username>', views.organizerProfileView,name="organizer-profile"),



]