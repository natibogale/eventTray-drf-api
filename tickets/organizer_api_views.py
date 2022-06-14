from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from authentication.models import User
from .serializers import *
from icecream import ic
from django.contrib.auth import *
from collections import namedtuple
import json
from rest_framework.parsers import MultiPartParser, FormParser

# from rest_framework.serializers import *
# from rest_framework import serializers
from rest_framework.decorators import authentication_classes, permission_classes

from rest_framework import status, permissions, response

from datetime import datetime
from django.core.exceptions import ObjectDoesNotExist
import pyotp
from rest_framework.views import APIView
import base64
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from django.db.models import Q
from rest_framework.generics import *
from django.conf import settings
import requests
from authentication.jwt import *
from authentication.permissions import IsEventOrganizer
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test

from .forms import *

from django.shortcuts import (
    HttpResponseRedirect,
    get_object_or_404,
    get_list_or_404,
    redirect,
    render,
)

from datetime import timedelta, datetime
from rest_framework.parsers import JSONParser

from json import JSONEncoder
import threading



 




@authentication_classes([JWTAuthentication])
@permission_classes([permissions.IsAuthenticated])
class OrganizerEventTicketsView(GenericAPIView):
    serializer_class = eventTicketSerializer
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request):
        user = request.user

        serializer_class = eventTicketSerializer(data=request.data)
        if serializer_class.is_valid():
            serializer_class.save()
            return Response(
                {"status": "success", "message":"Ticket added successfully!","ticket":serializer_class.data}, status=status.HTTP_201_CREATED

            )
        else:
            return Response(
                {"status": "error", "message": serializer_class.errors}, status=status.HTTP_400_BAD_REQUEST
            ) 


    def put(self, request):
        user = request.user
        eventid = request.data['id']

        ticket = Tickets.objects.get(id=eventid)

        serializer_class = eventTicketSerializer(ticket, data=request.data)
        if serializer_class.is_valid():
            serializer_class.save()
            return Response(
                {"status": "success", "message":"Ticket updated successfully!","image":serializer_class.data}, status=status.HTTP_201_CREATED

            )
        else:
            return Response(
                {"status": "error", "message": serializer_class.errors}, status=status.HTTP_400_BAD_REQUEST
            ) 

    def get(self, request):
        user = request.user
        try:
            ticketId = request.GET.get('id')
            ticket = Tickets.objects.get(id=ticketId, ticketOwner=user)
            evenet = Events.objects.get(id=ticket.event.id)
            ticket.eventName = evenet.eventName
            ticket.save()
            serializer_class = eventTicketSerializer(ticket)

            return Response(
                {"status": "success","ticket":serializer_class.data}, status=status.HTTP_200_OK
            )
        except Exception as e:
            ticket = Tickets.objects.filter(ticketOwner=user)
            for tk in ticket:
                evenet = Events.objects.get(id=tk.event.id)
                tk.eventName = evenet.eventName
                tk.save()
        
            serializer_class = eventTicketSerializer(ticket,many=True)
            return Response(
                {"status": "success","ticket":serializer_class.data}, status=status.HTTP_200_OK
            )
        
        return Response(
            {"status": "error", "message": "Events Not Found"}, status=status.HTTP_404_NOT_FOUND
        )  







@authentication_classes([JWTAuthentication])
@permission_classes([permissions.IsAuthenticated])
class OrganizerEventsTicketsView(GenericAPIView):
    serializer_class = eventTicketSerializer

    def post(self, request):
        user = request.user

        serializer_class = eventTicketSerializer(data=request.data)
        if serializer_class.is_valid():
            serializer_class.save()
            return Response(
                {"status": "success", "message":"Ticket added successfully!","ticket":serializer_class.data}, status=status.HTTP_201_CREATED

            )
        else:
            return Response(
                {"status": "error", "message": serializer_class.errors}, status=status.HTTP_400_BAD_REQUEST
            ) 


    def put(self, request):
        user = request.user
        eventid = request.data['id']

        ticket = Tickets.objects.get(id=eventid)

        serializer_class = eventTicketSerializer(ticket, data=request.data)
        if serializer_class.is_valid():
            serializer_class.save()
            return Response(
                {"status": "success", "message":"Ticket updated successfully!","image":serializer_class.data}, status=status.HTTP_201_CREATED

            )
        else:
            return Response(
                {"status": "error", "message": serializer_class.errors}, status=status.HTTP_400_BAD_REQUEST
            ) 

    def get(self, request):
        user = request.user
        try:
            ticketId = request.GET.get('id')
            ticket = Tickets.objects.get(id=ticketId, ticketOwner=user)
            evenet = Events.objects.get(id=ticket.event.id)
            ticket.eventName = evenet.eventName
            ticket.save()
            serializer_class = eventTicketSerializer(ticket)

            return Response(
                {"status": "success","ticket":serializer_class.data}, status=status.HTTP_200_OK
            )
        except Exception as e:
            ticket = Tickets.objects.filter(ticketOwner=user)
            for tk in ticket:
                evenet = Events.objects.get(id=tk.event.id)
                tk.eventName = evenet.eventName
                tk.save()
        
            serializer_class = eventTicketSerializer(ticket,many=True)
            return Response(
                {"status": "success","ticket":serializer_class.data}, status=status.HTTP_200_OK
            )
        
        return Response(
            {"status": "error", "message": "Events Not Found"}, status=status.HTTP_404_NOT_FOUND
        )  
