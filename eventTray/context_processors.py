import re
from django.shortcuts import render
from events.models import *
from authentication.models import *


def fixed(request):
    organizer = None
    try:
        organizer = Organizer.objects.get(organizer=request.user.id)
        categories = Categories.objects.all()
        cities = Cities.objects.all()
        places = Venues.objects.all()

        context = {
            "user": user,
            "organizer": organizer,
            "categories": categories,
            "cities": cities,
            "places": places,
        }
        return context

    except Exception as e:
        context = {"organizer": organizer}

        return context




def locations(request):
    some = None
    try:
        cities = Cities.objects.all()
        venues = Venues.objects.all()
        events = Events.objects.filter(organizer=request.user.id).order_by('-date_added')

        context = {
            "cities": cities,
            "venues": venues,
            "events":events

        }
        return context

    except Exception as e:
        context = {"some": some}

        return context
