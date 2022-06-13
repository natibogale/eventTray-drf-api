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
from django.forms.models import model_to_dict

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
from tickets.models import *
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
class OrganizerEventsView(GenericAPIView):
    serializer_class = EventSerializer

    def post(self, request):
        user = request.user
        serializer_class = EventSerializer(data=request.data)
        if serializer_class.is_valid():
            serializer_class.save()
            return Response(
                {"status": "success", "message":"Event Created successfully!","event":serializer_class.data}, status=status.HTTP_201_CREATED

            )
        else:
            return Response(
                {"status": "error", "message": serializer_class.errors}, status=status.HTTP_400_BAD_REQUEST
            ) 


    def put(self, request):
        user = request.user
        eventId = request.data['id']
        event = Events.objects.get(id=eventId)
        serializer_class = EventSerializer(event, data=request.data)
        if serializer_class.is_valid():
            serializer_class.save()
            return Response(
                {"status": "success", "message":"Event Updated successfully!","event":serializer_class.data}, status=status.HTTP_201_CREATED
            )
        else:
            return Response(
                {"status": "error", "message": serializer_class.errors}, status=status.HTTP_400_BAD_REQUEST
            ) 


    def get(self, request):
        user = request.user
        try:
            eventId = request.GET.get('id')
            event = Events.objects.get(id=eventId,organizer=user)
            serializer_class = EventSerializer(event)
       
            withoutImage = serializer_class.data
            try:
                image = Images.objects.get(event=eventId)
                image = str(image.image)
            except Exception as e:
                image=""
            withoutImage['image'] = "/media/"+image
           
            return Response(
                {"status": "success","event": withoutImage}, status=status.HTTP_200_OK
            )
        except Exception as e:
            event = Events.objects.filter(organizer=user)
            for ev in event:
                
                try:
                    image = Images.objects.get(event=ev.id)
                    image = str(image.image)

                except Exception as e:
                    image=""
                if image:
                    ev.image = "/media/"+image
                    ev.save()
                else:
                    ev.image = image
                    
                  

                
            serializer_class = EventSerializer(event,many=True)

            return Response(
                {"status": "success","event":serializer_class.data}, status=status.HTTP_200_OK
            )
        
        return Response(
            {"status": "error", "message": "Events Not Found"}, status=status.HTTP_404_NOT_FOUND
        )  



    def patch(self, request):
        user = request.user
        eventId = request.data['id']
        organizer = request.data['organizer']
        event = Events.objects.get(id=eventId)
        images = Images.objects.filter(event=eventId)

        organizerHosted = Organizer.objects.get(organizer=organizer)
        organizerHosted.totalEvents += 1
        organizerHosted.save()

        serializer_class = EventSerializer(event, data=request.data,partial=True)
        if serializer_class.is_valid():
            if images:
                serializer_class.save()
                return Response(
                    {"status": "success", "message":"Event published successfully!","event":serializer_class.data}, status=status.HTTP_201_CREATED
                )
            else:
                return Response(
                    {"status": "error", "message":"Atleast One Image needed to publish Event!","event":serializer_class.data}, status=status.HTTP_201_CREATED
                )
        else:
            return Response(
                {"status": "error", "message": serializer_class.errors}, status=status.HTTP_400_BAD_REQUEST
            ) 





@authentication_classes([])
@permission_classes([permissions.AllowAny])
class CitiesListView(GenericAPIView):
    serializer_class = CitiesSerializer

    def get(self, request):
        user = request.user
        serializer_class = CitiesSerializer
        cities = Cities.objects.all()
        if cities:
            serializer_class = CitiesSerializer(cities, many=True)
            return Response(
                {"status": "success", "cities":serializer_class.data}, status=status.HTTP_202_ACCEPTED

            )
        else:
            return Response(
                {"status": "error", "message": "No Cities Found"}, status=status.HTTP_404_NOT_FOUND
            )  





@authentication_classes([JWTAuthentication])
@permission_classes([permissions.IsAuthenticated])
class OrganizerEventImagesView(GenericAPIView):
    serializer_class = eventImagesSerializer
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request):
        user = request.user

        serializer_class = eventImagesSerializer(data=request.data)
        if serializer_class.is_valid():
            serializer_class.save()
            return Response(
                {"status": "success", "message":"Image added successfully!","image":serializer_class.data}, status=status.HTTP_201_CREATED

            )
        else:
            return Response(
                {"status": "error", "message": serializer_class.errors}, status=status.HTTP_400_BAD_REQUEST
            ) 


    def put(self, request):
        user = request.user
        id = request.data['id']
        image = Images.objects.get(id=id)
        serializer_class = eventImagesSerializer(image, data=request.data)
        if serializer_class.is_valid():
            serializer_class.save()
            return Response(
                {"status": "success", "message":"Image updated successfully!","image":serializer_class.data}, status=status.HTTP_201_CREATED

            )
        else:
            return Response(
                {"status": "error", "message": serializer_class.errors}, status=status.HTTP_400_BAD_REQUEST
            ) 






    def put(self, request):
        user = request.user
        eventId = request.data['id']
        event = Events.objects.get(id=eventId)
        serializer_class = EventSerializer(event, data=request.data)
        if serializer_class.is_valid():
            serializer_class.save()
            return Response(
                {"status": "success", "message":"Event Updated successfully!","event":serializer_class.data}, status=status.HTTP_201_CREATED
            )
        else:
            return Response(
                {"status": "error", "message": serializer_class.errors}, status=status.HTTP_400_BAD_REQUEST
            ) 