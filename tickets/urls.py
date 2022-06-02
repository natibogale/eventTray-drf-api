from . import views
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import *


urlpatterns = [
     path('create-ticket/', views.createTicketView,name="create-ticket"),
 
]