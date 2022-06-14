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
from rest_framework.permissions import AllowAny    

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

from notifications.models import *
from threading import Timer


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



@permission_classes([permissions.AllowAny])
class EventsListView(GenericAPIView):
    serializer_class = EventSerializer
    permission_classes = (AllowAny,)

    def get(self, request):
        try:
            user = request.user
            id=request.GET.get("id")
            events = Events.objects.get(id=id)
            images = Images.objects.filter(event=id).first()
            events.image=images.image
            events.save()
            serializer_class = EventSerializer(events)
            return Response(
                {"status": "success", "events":serializer_class.data}, status=status.HTTP_202_ACCEPTED

            )

        except Exception as e:
            try:
                user = request.user
                searchBy=request.GET.get("searchBy")
                events = Events.objects.filter((Q(is_published=True) & Q(is_cancelled = False)) & Q(eventDescription__icontains=searchBy) | Q(eventCategories__icontains=searchBy)| Q(venue__icontains=searchBy) )
                for ev in events:
                    images = Images.objects.filter(event=ev.id).first()
                    ev.image=images.image
                    ev.save()
                serializer_class = EventSerializer(events, many=True)
                return Response(
                    {"status": "success", "events":serializer_class.data}, status=status.HTTP_202_ACCEPTED

                )
            except Exception as e:
                user = request.user
                events = Events.objects.filter(is_published=True, is_cancelled = False)
                for ev in events:
                    images = Images.objects.filter(event=ev.id).first()
                    ev.image=images.image
                    ev.save()
                serializer_class = EventSerializer(events, many=True)
                return Response(
                    {"status": "success", "events":serializer_class.data}, status=status.HTTP_202_ACCEPTED

                )

        return Response(
            {"status": "error", "message": "No Events Found"}, status=status.HTTP_404_NOT_FOUND
        )  






@permission_classes([permissions.AllowAny])
class EventsSearchView(GenericAPIView):
    serializer_class = EventSerializer

    def get(self, request):
        try:
            user = request.user
            searchBy=request.GET.get("searchBy")
            events = Events.objects.filter(is_published=True, is_cancelled = False, eventDescription__icontains=searchBy, eventCategories__icontains=searchBy, venue__icontains=searchBy )
            serializer_class = EventSerializer(events, many=True)
            return Response(
                {"status": "success", "events":serializer_class.data}, status=status.HTTP_202_ACCEPTED

            )

        except Exception as e:
            user = request.user
            events = Events.objects.filter(is_published=True, is_cancelled = False)
            serializer_class = EventSerializer(events, many=True)
            return Response(
                {"status": "success", "events":serializer_class.data}, status=status.HTTP_202_ACCEPTED

            )


        return Response(
            {"status": "error", "message": "No Events Found"}, status=status.HTTP_404_NOT_FOUND
        )  
