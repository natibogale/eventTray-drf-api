from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import User
from .serializers import UserSerializer
# from rest_framework.serializers import *
from rest_framework import serializers
from rest_framework import status


from datetime import datetime
from django.core.exceptions import ObjectDoesNotExist
import pyotp
from rest_framework.views import APIView
import base64


@api_view(['GET'])
def ApiOverview(request):
    api_urls = {
        'all_items': '/',
        'Search by Category': '/?category=category_name',
        'Search by Subcategory': '/?subcategory=category_name',
        'Add': '/create',
        'Update': '/update/pk',
        'Delete': '/item/pk/delete'
    }
  
    return Response(api_urls)




@api_view(['POST'])
def user_register(request):
    user = UserSerializer(data=request.data)
  
    # validating for already existing data
    if User.objects.filter(**request.data).exists():
        raise serializers.ValidationError('This User already exists')
  
    if user.is_valid():
        user.save()
        return Response(user.data)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)




@api_view(['GET'])
def view_profile(request):
    
    # checking for the parameters from the URL

    if request.GET.get('username', None):
        try:
            user = User.objects.get (**request.GET.dict())
            data = UserSerializer(user)
            print(data.data)
            return Response(data.data)
        except:
            return Response( "User Doesn't Exist", status=status.HTTP_404_NOT_FOUND,)

    else:
        return Response(status=status.HTTP_404_NOT_FOUND)





# This class returns the string needed to generate the key
class generateKey:
    @staticmethod
    def returnValue(phone):
        return str(phone) + str(datetime.date(datetime.now())) + "Some Random Secret Key"




@api_view(['GET'])
def sendOtp(request):
    if request.GET.get('phoneNumber', None):
        phoneNumber = request.GET.get('phoneNumber', None)
    else:
        return Response({"message": "Phone Number not provided"}, status=404)  # Just for demonstration
    try:
        user = User.objects.get(phoneNumber=phoneNumber)  # if user already exists the take this else create New One
    except ObjectDoesNotExist:
        return Response({"message": "User doesn't exist"}, status=404)  # Just for demonstration
    
    user.counter += 1  # Update Counter At every Call
    user.save()  # Save the data
    keygen = generateKey()
    key = base64.b32encode(keygen.returnValue(phoneNumber).encode())  # Key is generated
    OTP = pyotp.HOTP(key)  # HOTP Model for OTP is created
    print(OTP.at(user.counter))
    # Using Multi-Threading send the OTP Using Messaging Services like Twilio or Fast2sms
    return Response({"OTP": OTP.at(user.counter)}, status=200)  # Just for demonstration



@api_view(['POST'])
def verifyOtp(request):
    try:
        phoneNumber = request.data["phoneNumber"]
        user = User.objects.get(phoneNumber=phoneNumber)
    except ObjectDoesNotExist:
        return Response("User does not exist", status=404)  # False Call

    keygen = generateKey()
    key = base64.b32encode(keygen.returnValue(phoneNumber).encode())  # Generating Key
    OTP = pyotp.HOTP(key)  # HOTP Model
    if OTP.verify(request.data["otp"], user.counter):  # Verifying the OTP
        user.isVerified = True
        user.counter += 1 
        user.save()

        user = authenticate()

        return Response("You are authorised", status=200)
    return Response("OTP is wrong", status=400)