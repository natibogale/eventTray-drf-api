from . import views
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import *

urlpatterns = [
    #  path('record-officer/', views.record_officer_view, name="record-officer"),
    #  path('director/', views.director_view, name="director"),
    #  path('human-resources/', views.hr_view, name="hr"),
    
     path('create-event/', views.createEventView,name="create-event"),
     path('events-list/', views.eventsListView,name="events-list"),
     path('event-details/<id>', views.eventsDetailView,name="event-details"),
     path('event-preview/<id>', views.eventPreview,name="event-preview"),

    #  path('add-events-images/<str>', views.addImages,name="add-event-images"),

]