
from django.db.models import fields
from rest_framework import serializers
from .models import *


class eventTicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tickets
        fields = "__all__"

class BuyTicketsListSerializer(serializers.ListSerializer):
    def create(self, validated_data):
        tickets = [TicketsBought(**item) for item in validated_data]
        return TicketsBought.objects.bulk_create(tickets)


class BuyEventTicketsSerializer(serializers.ModelSerializer):

    class Meta:
        list_serializer_class = BuyTicketsListSerializer
        model = TicketsBought
        fields = "__all__"


class ScanTicketsSerializer(serializers.ModelSerializer):

    class Meta:
        model = TicketsBought
        fields = "__all__"


class MyTicketsSerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketsBought
        fields = "__all__"