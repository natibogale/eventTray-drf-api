import re
from django.shortcuts import render
from events.models import *
from authentication.models import *


def fixed(request):
    organizer = None
    try:
        organizer = Organizer.objects.get(organizer=request.user.id)
        categories = Categories.objects.all()
        context = {
            "user": user,
            "organizer": organizer,
            "categories": categories,
        }
        return context

    except Exception as e:
        context = {"organizer": organizer}

        return context
