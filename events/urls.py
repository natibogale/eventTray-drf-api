from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from events.views import *
from events.organizer_api_views import *
from events.user_api_views import *


urlpatterns = [
    path("create/", OrganizerEventsView.as_view(), name="event-api-view"),





     path('create-event/', createEventView,name="create-event"),
     path('events-list/', eventsListView,name="events-list"),
     path('event-details/<id>', eventsDetailView,name="event-details"),
     path('event-preview/<id>', eventPreview,name="event-preview"),

    #  path('add-events-images/<str>', views.addImages,name="add-event-images"),

]