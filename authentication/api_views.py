
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



###############################################################################3
# API Views for All User Registration and Authentication


class APIOverview(GenericAPIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        api_urls = {
            "all_items": "/",
            "Search by Category": "/?category=category_name",
            "Search by Subcategory": "/?subcategory=category_name",
            "Add": "/create",
            "Update": "/update/pk",
            "Delete": "/item/pk/delete",
        }

        return Response(api_urls)





class generateKey:
    @staticmethod
    def returnValue(phone):
        return (
            str(phone) + str(datetime.date(datetime.now())) + "Some Random Secret Key"
        )



@authentication_classes([])
@permission_classes([permissions.AllowAny])
class UserRegisterView(GenericAPIView):
    serializer_class = UserRegisterSerializer

    def post(self, request):

        hashed = make_password(request.data["password"])
        request.POST._mutable = True

        request.data["password"] = hashed

        username = request.data["username"]
        phoneNumber = request.data["phoneNumber"]
        role = request.data["role"]
        request.POST._mutable = False

        serializer_class = UserRegisterSerializer(data=request.data)

        # validating for already existing data

        try:
            us = User.objects.get(username=username)
            if us:
                return Response(
                    {"status": "error", "message": "Username already exists"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
                raise serializer_class.ValidationError("This User already exists")
        except:
            pass

        try:
            pn = User.objects.get(phoneNumber=phoneNumber, role=role)

            if pn:
                return Response(
                    {"status": "error", "message": "User already exists"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
                raise serializer_class.ValidationError("This User already exists")
        except:
            pass

        if serializer_class.is_valid():
            serializer_class.save()
            return Response(
                {
                    "status": "success",
                    "message": "Account created successfully, proceed to login!",
                },
                status=status.HTTP_201_CREATED,
            )
        else:
            return Response(
                {"status": "false", "message": serializer_class.errors},
                status=status.HTTP_406_NOT_ACCEPTABLE,
            )




def increaseCounter(phoneNumber, role):
    user = User.objects.get(
                phoneNumber=phoneNumber, role=role
            )
    user.counter +=1
    user.save()



@authentication_classes([])
class SendOtp(GenericAPIView):

    def get(self, request):

        # permission_classes = [permissions.AllowAny,]
        if request.GET.get("phoneNumber"):
            phoneNumber = request.GET.get("phoneNumber")
            role = request.GET.get("role")
        else:
            return Response(
                {"status": "error", "message": "Phone Number not provided"},
                status=status.HTTP_400_BAD_REQUEST,
            )  # Just for demonstration
        try:
            user = User.objects.get(
                phoneNumber=phoneNumber, role=role
            )  # if user already exists the take this else create New One
        except ObjectDoesNotExist:
            return Response(
                {"status": "error", "message": "User doesn't exist"},
                status=status.HTTP_404_NOT_FOUND,
            )  # Just for demonstration

        user.counter += 1  # Update Counter At every Call
        user.save()  # Save the data
        keygen = generateKey()
        key = base64.b32encode(
            keygen.returnValue(phoneNumber).encode()
        )  # Key is generated
        OTP = pyotp.HOTP(key)  # HOTP Model for OTP is created


        timer = threading.Timer(300.0, increaseCounter,[phoneNumber, role])
        timer.start()

        # Change phoneNumber format from 09 to +251
        phoneNumber = list(phoneNumber)
        phoneNumber[0] = "+251"
        phoneNumber = "".join(phoneNumber)

        # send messages using hahusms


        
        messageOTP = (
            "Dear "
            + role
            + ", Your OTP is "
            + OTP.at(user.counter)
            + ". It will exprire in 5 minutes. EventTray"
        )
        url = (
            "https://sms.hahucloud.com/api/send?key="
            + settings.HAHU_API_KEY
            + "&phone="
            + phoneNumber
            + "&message="
            + messageOTP
            + "&priority=10"
        )
        # r = requests.get(url)

        # if r.status_code == 200:
        if 1:
            return Response(
                {
                    "status": "success",
                    "message": "OTP has been sent to your phone.",
                    "url": url,
                },
                status=status.HTTP_201_CREATED,
            )  # Just for demonstration
        else:
            return Response(
                {"status": "error", "message": "Error Occured! Try again in a few"},
                status=status.HTTP_400_BAD_REQUEST,
            )  # Just for demonstration



@authentication_classes([])
@permission_classes([permissions.AllowAny])

class VerifyOTP(GenericAPIView):
    serializer_class = Loginserializer

    def post(self, request):
        try:
            phoneNumber = request.data["phoneNumber"]
            role = request.data["role"]
            user = User.objects.get(phoneNumber=phoneNumber, role=role)
        except ObjectDoesNotExist:
            return Response(
                {"status": "error", "message": "User does not exist"},
                status=status.HTTP_404_NOT_FOUND,
            )  # False Call

        keygen = generateKey()
        key = base64.b32encode(
            keygen.returnValue(phoneNumber).encode()
        )  # Generating Key
        OTP = pyotp.HOTP(key)  # HOTP Model

        if OTP.verify(request.data["otp"], user.counter):  # Verifying the OTP

            user.counter += 1

            us = authenticate(username=user.username, password=user.phoneNumber)
            user.is_authenticated = True
            user.save()
            if us:
                serializer_class = Loginserializer(us)
                return Response(
                    {
                        "status": "success",
                        "message": "Successfully logged in",
                        "data": serializer_class.data,
                    },
                    status=status.HTTP_202_ACCEPTED,
                )

        return Response(
            {"status": "error", "message": "Invalid Credential!"},
            status=status.HTTP_401_UNAUTHORIZED,
        )


@authentication_classes([JWTAuthentication])
@permission_classes([permissions.IsAuthenticated])
class UserProfileView(GenericAPIView):
    serializer_class = UserProfileSerializer

    def get(self, request):
        user = request.user
        print('qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq',user)
        serializer_class = UserProfileSerializer(user)
        return Response(
            {"status": "success", "user": serializer_class.data}, status=status.HTTP_200_OK
        )

    def put(self, request):
        user = request.user

        serializer_class = UserProfileSerializer(user, data=request.data ) 

        if serializer_class.is_valid():
            serializer_class.save()
 
            return Response(
            {"status": "success","message":"Profile Updated successfully!", "details": serializer_class.data}, status=status.HTTP_200_OK
            )
        else:
            return Response({"status":"error", "message": serializer_class.errors},status=status.HTTP_400_BAD_REQUEST)


@authentication_classes([JWTAuthentication])
@permission_classes([permissions.IsAuthenticated])
class UserOrganizerProfileView(GenericAPIView):
    serializer_class = OrganizerProfileSerializer

    def get(self, request):
        username = request.GET.get('username')
        user = request.user
        try:
            organizer = User.objects.get(username=username)
            serializer_class = OrganizerProfileSerializer(organizer)
            return Response(
                {"status": "success", "user": serializer_class.data}, status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {"status": "error", "message": "Organizer not found!"}, status=status.HTTP_404_NOT_FOUND

            )



@authentication_classes([JWTAuthentication])
@permission_classes([permissions.IsAuthenticated])

class UserOrganizerListView(GenericAPIView):
    serializer_class = OrganizerProfileSerializer

    def get(self, request):
        user = request.user
        try:
            organizers = User.objects.filter(is_active=True)

            serializer_class = OrganizerProfileSerializer(organizers, many=True)
            return Response(
                {"status": "success", "users": serializer_class.data}, status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {"status": "error", "message": "Organizers not found!"}, status=status.HTTP_404_NOT_FOUND

            )



@authentication_classes([JWTAuthentication])
@permission_classes([permissions.IsAuthenticated])

class OrganizerProfileView(GenericAPIView):
    parser_classes = (MultiPartParser, FormParser)
    serializer_class = OrganizerProfileSerializer

    def get(self, request):
        user = request.user
        serializer_class = OrganizerProfileSerializer(user)
        return Response(
            {"status": "success", "user": serializer_class.data}, status=status.HTTP_200_OK
        )


    def put(self, request):
        user = request.user
        serializer_class = OrganizerProfileSerializer(user, data=request.data ) 

        if serializer_class.is_valid():
            serializer_class.save()

            return Response(
            {"status": "success","message":"Profile Updated successfully!", "user": serializer_class.data}, status=status.HTTP_200_OK
            )
        else:
            return Response({"status":"error", "message": serializer_class.errors},status=status.HTTP_400_BAD_REQUEST)





@authentication_classes([JWTAuthentication])
@permission_classes([permissions.IsAuthenticated])
class OrganizerDetailView(GenericAPIView):
    serializer_class = OrganizerDetailSerializer

    def post(self, request):
        user = request.user
        organizer = request.data['organizer']
        # details = Organizer.objects.get(organizer=organizer)

        serializer_class = OrganizerDetailSerializer(data=request.data)
        if serializer_class.is_valid():
            serializer_class.save()
            return Response(
                {"status": "success", "message":"Details Saved successfully!","user": serializer_class.data}, status=status.HTTP_201_CREATED

            )
        else:
            return Response(
                {"status": "error", "message": serializer_class.errors}, status=status.HTTP_400_BAD_REQUEST
            )   

    def put(self, request):
        user = request.user
        organizer = request.data['organizer']
        details = Organizer.objects.get(organizer=organizer)

        serializer_class = OrganizerDetailSerializer(details, data=request.data ) 

        if serializer_class.is_valid():
            serializer_class.save()
            return Response(
            {"status": "success","message":"Details Updated successfully!", "details": serializer_class.data}, status=status.HTTP_200_OK
            )
        else:
            return Response({"status":"error", "message": serializer_class.errors},status=status.HTTP_400_BAD_REQUEST)
