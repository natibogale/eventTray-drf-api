from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import *
from .organizer_api_views import *


urlpatterns = [
    path("create-ticket/", createTicketView, name="create-ticket"),





    # Api URL paths for ticket app
    path("", OrganizerEventImagesView.as_view(), name="create-ticket-api"),
]
