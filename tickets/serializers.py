
from django.db.models import fields
from rest_framework import serializers
from .models import *


class eventTicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tickets
        fields = "__all__"
