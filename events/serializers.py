
from django.db.models import fields
from rest_framework import serializers
from .models import *

CATEGORIES = (
    ("Activities", "Activities"),
    ("Art", "Art"),
    ("Bazar", "Bazar"),
    ("Business", "Business"),
    ("Concert", "Concert"),
    ("Conference", "Conference"),
    ("Dance", "Dance"),
    ("Education", "Education"),
    ("Exhibition", "Exhibition"),
    ("Expo", "Expo"),
    ("Fashion", "Fashion"),
    ("Festival", "Festival"),
    ("Film", "Film"),
    ("Food", "Food"),
    ("Fundraiser", "Fundraiser"),
    ("Music", "Music"),
    ("Online Webinar", "Online Webinar"),
    ("Night Life", "Night Life"),
    ("Sports", "Sports"),
    ("Technology", "Technology"),
    ("Travel", "Travel"),
    ("Training", "Training"),
)


class eventImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Images
        fields = "__all__"

class EventSerializer(serializers.ModelSerializer):
    eventCategories = serializers.ChoiceField(choices=CATEGORIES)
    images = eventImagesSerializer(many=True, read_only=True)

    class Meta:
        model = Events
        fields = "__all__"



class CitiesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cities
        fields = "__all__"





